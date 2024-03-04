import json
import os
from osgeo import ogr
from django.db import connection  # Importing connection for interacting with the database

from ProcessFiles.HandlingShapeFiles.ShpProcess import get_Shp_Field_Attributes, get_epsg_from_prj
from ProcessFiles.HandlingSpreadsheetFiles.HandlingXlsxFiles import get_xlsx_files_data
from Utils.DynamicSQL import update_table_from_form_shp_sql, insert_into_table_from_shp_sql, \
    generate_create_table_sql_from_shp, get_create_spreadsheet_sql, insert_into_table_from_spreadsheet_sql, \
    get_relationship_between_data_and_fields_from_spreadsheet


def create_table_from_SpreadsheetFiles_data(body_data, path, shpName):
    table_name = "Admin" + "_Observation_" + shpName
    table_name = table_name.lower()
    # 删除已存在的表
    drop_table_if_exists(table_name)
    sql = get_create_spreadsheet_sql(shpName, table_name)
    # 创建数据库连接的游标
    cursor = connection.cursor()
    # 执行 SQL 语句创建表
    cursor.execute(sql)
    connection.commit()

    # 从表单数据中获取非空字段
    field_from_form = []
    for key, value in body_data.items():
        if value is not None:
            field_from_form.append({key: value})
    data, attribute = get_xlsx_files_data(path, shpName)

    values = get_relationship_between_data_and_fields_from_spreadsheet(field_from_form, attribute, data)

    fields = get_table_fields_and_info(table_name)
    for row in values:
        sql = insert_into_table_from_spreadsheet_sql(row, table_name, fields)
        cursor.execute(sql)
        connection.commit()

    # ==============================
    # 执行查询语句
    cursor.execute(f"SELECT * FROM {table_name};")

    # 获取查询结果的列名
    columns = [desc[0] for desc in cursor.description]

    # 获取所有查询结果
    rows = cursor.fetchall()

    # 构建数据结构
    table_data = []
    for row in rows:
        data = {}
        for i in range(len(columns)):
            data[columns[i]] = str(row[i])
        table_data.append(data)

    return table_data


def create_table_from_shp_data(body_data, path, shpName):
    # 构建表名
    table_name = "Admin" + "_" + shpName
    table_name = table_name.lower()
    # 删除已存在的表
    drop_table_if_exists(table_name)

    # 从表单数据中获取非空字段
    field_from_form = []
    for key, value in body_data.items():
        if value is not None:
            field_from_form.append({key: value})
    # ==============================
    shapefile = None
    layer = None
    # 用于存储属性字段信息的列表
    attribute_info_list = []

    # 创建数据库连接的游标
    cursor = connection.cursor()

    # 获取 Shapefile 的驱动程序
    shapefile_path = os.path.join("Data", "Admin", path, shpName + ".shp")

    # 打开 Shapefile
    shapefile = ogr.Open(shapefile_path)
    if shapefile:
        # 获取第一个图层（假设 Shapefile 中只有一个图层）
        layer = shapefile.GetLayer(0)
        attribute_info_list = get_Shp_Field_Attributes(layer)
    # 生成动态的创建表的 SQL 语句
    dynamicSql = generate_create_table_sql_from_shp(table_name, attribute_info_list, field_from_form)
    # 执行 SQL 语句创建表
    cursor.execute(dynamicSql)
    connection.commit()
    # ==============================
    # 提交表中数据
    prj_file_path = os.path.join("Data", "Admin", path, shpName + ".prj")
    epsg_code = get_epsg_from_prj(prj_file_path)

    # 插入数据到 PostGIS 表
    for feature in layer:
        # 获取几何信息
        geometry = feature.GetGeometryRef()
        wkt_geometry = geometry.ExportToWkt()
        sql = insert_into_table_from_shp_sql(table_name, field_from_form, feature, attribute_info_list)
        cursor.execute(sql, (wkt_geometry, epsg_code))
        connection.commit()

    # ==============================
    # 执行查询语句
    cursor.execute(f"SELECT * FROM {table_name};")

    # 获取查询结果的列名
    columns = [desc[0] for desc in cursor.description]

    # 获取所有查询结果
    rows = cursor.fetchall()

    # 构建数据结构
    table_data = []
    for row in rows:
        data = {}
        for i in range(len(columns) - 1):
            data[columns[i]] = str(row[i])
        table_data.append(data)

    # 关闭游标
    cursor.close()
    # 关闭 Shapefile
    shapefile = None
    layer = None

    return table_data


def get_table_fields(table_name):
    """
    获取表中的所有字段。

    Args:
        table_name (str): 表名。

    Returns:
        list: 字段列表。

    """
    # 获取表中的所有字段
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")

    # 获取字段名称
    fields = [row[0] for row in cursor.fetchall()]

    # 关闭数据库连接
    cursor.close()

    # 返回字段列表
    return fields


def get_table_fields_and_info(table_name):
    """
    获取表中的所有字段。

    Args:
        table_name (str): 表名。

    Returns:
        list: 字段列表。

    """
    # 获取表中的所有字段
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
    results = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()

    # 转换为字典
    field_dict = {}
    for row in results:
        column_name, data_type = row
        field_dict[column_name] = data_type

    # 返回字段列表
    return field_dict


def drop_table_if_exists(table_name):
    """
        如果表存在，则删除表。

        Args:
            table_name (str): 表名。

        """
    cursor = connection.cursor()

    # 检查表是否存在
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
    exists = cursor.fetchone()[0]
    if exists:
        # 删除表
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

    connection.commit()
    cursor.close()


def update_table_from_form_shp(param, table_names):
    # 解码请求的原始数据
    body_unicode = param.decode('utf-8')
    # 将数据解析为 JSON 对象
    body_data = json.loads(body_unicode)

    if "FormName" in body_data:
        if body_data["FormName"] == 'Monitoring_Point_Attribute':
            table_name = "Admin" + "_" + table_names
        elif body_data["FormName"] == 'Observation_Data':
            table_name = "Admin" + "_" + "Observation" + "_" + table_names
    else:
        # 执行 SQL 查询
        table_name = "Admin" + "_" + table_names

    cursor = connection.cursor()

    table_name = table_name.lower()

    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
    cursor.execute(query)

    # 提取查询结果
    results = cursor.fetchall()
    dynamicSql = update_table_from_form_shp_sql(results, table_name, body_data)
    cursor.execute(dynamicSql)
    connection.commit()
    cursor.close()
