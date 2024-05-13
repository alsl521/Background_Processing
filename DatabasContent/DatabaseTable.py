import json
import os
from osgeo import ogr
from django.db import connection  # Importing connection for interacting with the database

from ProcessFiles.HandlingShapeFiles.ShpProcess import get_Shp_Field_Attributes, get_epsg_from_prj
from ProcessFiles.HandlingSpreadsheetFiles.HandlingXlsxFiles import get_xlsx_files_data
from Utils.DynamicSQL import insert_into_table_from_shp_sql, generate_create_table_sql_from_shp, \
    get_create_spreadsheet_sql, insert_into_table_from_spreadsheet_sql, \
    get_relationship_between_attribute_and_fields_from_spreadsheet, update_into_table_from_body_sql


# def create_table_from_SpreadsheetFiles_data(body_data, path, shpName):
#     table_name = "Admin_" + shpName + "_Observation"
#     table_name = table_name.lower()
#     # 删除已存在的表
#     drop_table_if_exists(table_name)
#     sql = get_create_spreadsheet_sql(shpName, table_name)
#     # 创建数据库连接的游标
#     cursor = connection.cursor()
#     # 执行 SQL 语句创建表
#     cursor.execute(sql)
#     connection.commit()
#
#     # 从表单数据中获取非空字段
#     field_from_form = []
#     for key, value in body_data.items():
#         if value is not None:
#             field_from_form.append({key: value})
#     data, attribute = get_xlsx_files_data(path, shpName)
#     values = get_relationship_between_data_and_fields_from_spreadsheet(field_from_form, attribute, data)
#
#     fields = get_table_fields_and_info(table_name)
#     for row in values:
#         sql = insert_into_table_from_spreadsheet_sql(row, table_name, fields)
#         cursor.execute(sql)
#         connection.commit()
#
#     # ==============================
#     # 执行查询语句
#     cursor.execute(f"SELECT * FROM {table_name} ORDER BY fid;")
#
#     # 获取查询结果的列名
#     columns = [desc[0] for desc in cursor.description]
#
#     # 获取所有查询结果
#     rows = cursor.fetchall()
#
#     # 构建数据结构
#     table_data = []
#     for row in rows:
#         data = {}
#         for i in range(len(columns)):
#             data[columns[i]] = str(row[i])
#         table_data.append(data)
#
#     return table_data
#
#
# def create_table_from_shp_data(body_data, path, shpName):
#     # 构建表名
#     table_name = "Admin" + "_" + shpName
#     table_name = table_name.lower()
#     # 删除已存在的表
#     drop_table_if_exists(table_name)
#
#     # 从表单数据中获取非空字段
#     field_from_form = []
#     for key, value in body_data.items():
#         if value is not None:
#             field_from_form.append({key: value})
#     # ==============================
#     shapefile = None
#     layer = None
#     # 用于存储属性字段信息的列表
#     attribute_info_list = []
#
#     # 创建数据库连接的游标
#     cursor = connection.cursor()
#
#     # 获取 Shapefile 的驱动程序
#     shapefile_path = os.path.join("Data", "Admin", path, shpName + ".shp")
#
#     # 打开 Shapefile
#     shapefile = ogr.Open(shapefile_path)
#     if shapefile:
#         # 获取第一个图层（假设 Shapefile 中只有一个图层）
#         layer = shapefile.GetLayer(0)
#         attribute_info_list = get_Shp_Field_Attributes(layer)
#     # 生成动态的创建表的 SQL 语句
#     dynamicSql = generate_create_table_sql_from_shp(table_name, attribute_info_list, field_from_form)
#     # 执行 SQL 语句创建表
#     cursor.execute(dynamicSql)
#     connection.commit()
#     # ==============================
#     # 提交表中数据
#     prj_file_path = os.path.join("Data", "Admin", path, shpName + ".prj")
#     epsg_code = get_epsg_from_prj(prj_file_path)
#
#     # 插入数据到 PostGIS 表
#     for feature in layer:
#         # 获取几何信息
#         geometry = feature.GetGeometryRef()
#         wkt_geometry = geometry.ExportToWkt()
#         sql = insert_into_table_from_shp_sql(table_name, field_from_form, feature, attribute_info_list)
#         cursor.execute(sql, (wkt_geometry, epsg_code))
#         connection.commit()
#
#     # ==============================
#     # 执行查询语句
#     cursor.execute(f"SELECT * FROM {table_name} ORDER BY fid;")
#
#     # 获取查询结果的列名
#     columns = [desc[0] for desc in cursor.description]
#
#     # 获取所有查询结果
#     rows = cursor.fetchall()
#
#     # 构建数据结构
#     table_data = []
#     for row in rows:
#         data = {}
#         for i in range(len(columns) - 1):
#             data[columns[i]] = str(row[i])
#         table_data.append(data)
#
#     # 关闭游标
#     cursor.close()
#     # 关闭 Shapefile
#     shapefile = None
#     layer = None
#
#     return table_data


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


# def get_table_fields_and_info(table_name):
#     """
#     获取表中的所有字段。
#
#     Args:
#         table_name (str): 表名。
#
#     Returns:
#         list: 字段列表。
#
#     """
#     # 获取表中的所有字段
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
#     results = cursor.fetchall()
#
#     # 关闭数据库连接
#     cursor.close()
#
#     # 转换为字典
#     field_dict = {}
#     for row in results:
#         column_name, data_type = row
#         field_dict[column_name] = data_type
#
#     # 返回字段列表
#     return field_dict


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


# def update_table_from_form_shp(param, table_names):
#     # 解码请求的原始数据
#     body_unicode = param.decode('utf-8')
#     # 将数据解析为 JSON 对象
#     body_data = json.loads(body_unicode)
#
#     if "FormName" in body_data:
#         if body_data["FormName"] == 'Monitoring_Point_Attribute':
#             table_name = "Admin" + "_" + table_names
#         elif body_data["FormName"] == 'Observation_Data':
#             table_name = "Admin_" + table_names + "_Observation"
#     else:
#         # 执行 SQL 查询
#         table_name = "Admin" + "_" + table_names
#
#     cursor = connection.cursor()
#
#     table_name = table_name.lower()
#
#     query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';"
#
#     cursor.execute(query)
#
#     # 提取查询结果
#     results = cursor.fetchall()
#     dynamicSql = update_table_from_form_shp_sql(results, table_name, body_data)
#
#     print(dynamicSql)
#
#     cursor.execute(dynamicSql)
#     connection.commit()
#     cursor.close()

def get_table_from_project(table_name):
    cursor = connection.cursor()
    query = f"SELECT table_name FROM admin_project_setting WHERE name like concat('%','{table_name}','%');"
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def get_project_setting(shpName):
    cursor = connection.cursor()
    query = f"SELECT table_name FROM admin_project_setting WHERE name = '{shpName}';"
    cursor.execute(query)

    # 提取查询结果
    results = cursor.fetchall()
    result = results[0][0]
    cursor.close()
    return result


def update_project_setting(shpName, number):
    cursor = connection.cursor()
    if number == 1:

        query = f"SELECT table_name FROM admin_project_setting WHERE name = '{shpName}';"
        cursor.execute(query)

        # 提取查询结果
        results = cursor.fetchall()

        if len(results) == 0:

            table_name = "Admin_" + shpName

            query = f"INSERT INTO admin_project_setting (name, table_name) VALUES ('{shpName}', '{table_name}');"

            cursor.execute(query)

            connection.commit()
        else:
            table_name = "Admin_" + shpName

            query = f"UPDATE admin_project_setting SET  table_name = '{table_name}' WHERE name = '{shpName}';"

            cursor.execute(query)

            connection.commit()

    elif number == 2:

        query = f"SELECT table_name FROM admin_project_setting WHERE name = '{shpName}';"
        cursor.execute(query)

        # 提取查询结果
        results = cursor.fetchall()

        if len(results) == 0:

            table_name = "Admin_" + shpName

            query = f"INSERT INTO admin_project_setting (name, table_name) VALUES ('{shpName}', '{table_name}');"

            cursor.execute(query)

            connection.commit()

            table_name = "Admin_" + shpName + "_Observation"
            query_name = shpName + "_Observation"

            query = f"INSERT INTO admin_project_setting (name, table_name) VALUES ('{query_name}', '{table_name}');"

            cursor.execute(query)

            connection.commit()

        else:
            table_name = "Admin_" + shpName

            query = f"UPDATE admin_project_setting SET  table_name = '{table_name}' WHERE name = '{shpName}';"

            cursor.execute(query)

            connection.commit()

            query_name = shpName + "_Observation"

            table_name = "Admin_" + shpName + "_Observation"

            query = f"UPDATE admin_project_setting SET  table_name = '{table_name}' WHERE name = '{query_name}';"

            cursor.execute(query)

            connection.commit()

    cursor.close()


def create_table_from_shp(path, shpName):
    # 构建表名
    table_name = "Admin" + "_" + shpName
    table_name = table_name.lower()

    # 删除已存在的表
    drop_table_if_exists(table_name)

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
    dynamicSql = generate_create_table_sql_from_shp(table_name, attribute_info_list)
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
        sql = insert_into_table_from_shp_sql(table_name, feature, attribute_info_list)
        print("插入数据到 PostGIS 表:" + sql)
        cursor.execute(sql, (wkt_geometry, epsg_code))
        connection.commit()


def create_table_from_sheet(path, shpName):
    table_name = "Admin_" + shpName + "_Observation"
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
    data, attribute = get_xlsx_files_data(path, shpName)

    values = get_relationship_between_attribute_and_fields_from_spreadsheet(sql)

    for row in data:
        sql = insert_into_table_from_spreadsheet_sql(row, table_name, values)
        print("%s：%s" % (table_name, sql))
        cursor.execute(sql)
        connection.commit()


def get_total_time_from_surfacerive_point_observation():
    # 创建数据库连接的游标
    cursor = connection.cursor()
    table_name = "admin_" + "surfacerive_point"
    sql = "select name from {}".format(table_name)

    cursor.execute(sql)
    # 提取查询结果
    name = cursor.fetchone()[0]

    table_name = "admin_" + "surfacerive_point_observation"

    sql = "select time from {} where name = '{}'".format(table_name, name)
    cursor.execute(sql)
    # 提取查询结果
    results = cursor.fetchall()
    return results[0][0], results[-1][0]


def set_time_into_table(data_dict):
    # 创建数据库连接的游标
    cursor = connection.cursor()
    table_name = "admin_" + "time_dispersion"

    sql = "CREATE TABLE IF NOT EXISTS {} (Fid serial PRIMARY KEY,name VARCHAR,time VARCHAR)".format(table_name)

    cursor.execute(sql)
    connection.commit()

    for key, value in data_dict.items():
        if select_from_table_sql(table_name, key, value):
            sql = "UPDATE {} SET time='{}' WHERE name='{}'".format(table_name, value, key)
            cursor.execute(sql)
        else:
            sql = "INSERT INTO {}(name, time) values ('{}','{}')".format(table_name, key, value)
            cursor.execute(sql)
    connection.commit()


def select_from_table_sql(table_name, key, value):
    sql = "select * from {} where name = '{}'".format(table_name, key)

    cursor = connection.cursor()
    cursor.execute(sql)

    results = cursor.fetchall()

    if len(results) > 0:
        return True
    else:
        return False


def get_modflow_time_from_table():
    table_name = "admin_" + "time_dispersion"
    sql = "SELECT time from {} where name = 'modflow_calculate_time'".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    results = cursor.fetchone()[0]
    arr = results.split(" ")
    seconds = 0
    if arr[1] == "second":
        seconds = int(arr[0]) * 1
    elif arr[1] == "minute":
        seconds = int(arr[0]) * 60
    elif arr[1] == "hour":
        seconds = int(arr[0]) * 60 * 60
    elif arr[1] == "day":
        seconds = int(arr[0]) * 24 * 60 * 60
    elif arr[1] == "month":
        seconds = int(arr[0]) * 24 * 60 * 60 * 30
    elif arr[1] == "year":
        seconds = int(arr[0]) * 24 * 60 * 60 * 30 * 12
    return seconds


column_mapping = {
    'StudyAreaScope': '研究区域范围',
    'FlowRate': '流量',
    'FlowRate_Observation': '流量观测数据',
    'Temperature': '温度',
    'Temperature_Observation': '温度观测数据',
    'AtmosphericPressure': '大气压力',
    'AtmosphericPressure_Observation': '大气压力观测数据',
    'Evaporation': '蒸发',
    'Evaporation_Observation': '蒸发观测数据',
    'Rainfall': '降雨',
    'Rainfall_Observation': '降雨观测数据',
    'SolarRadiation': '太阳辐射',
    'SolarRadiation_Observation': '太阳辐射观测数据',
    'CloudCover': '云量',
    'CloudCover_Observation': '云量观测数据',
    'WindSpeedAndDirection': '风速和风向',
    'WindSpeedAndDirection_Observation': '风速和风向观测数据',
    'WaterTemperature': '水温',
    'WaterTemperature_Observation': '水温观测数据',
    'SWMMSpatialDiscreteData': 'SWMM空间离散数据',
    'EFDCSpatialDiscreteData': 'EFDC空间离散数据',
    'MODFLOWSpatialDiscreteData': 'MODFLOW空间离散数据',
    'SWMMandEFDCInteractiveUnit': 'SWMM—EFDC空间交互单元',
    'SWMMandMODFLOWInteractiveUnit': 'SWMM—MODFLOW空间交互单元',
    'EFDCandMODFLOWInteractiveUnit': 'EFDC—MODFLOW空间交互单元',
    'RainGauge': '雨量计',
    'GeologicalBody': '地质体',
    'GeologicalBody_Observation': '地质体观测数据',
    'Infiltration': '渗透',
    'StoreWater': '储存水',
    'Junction': '交汇点',
    'DEM': 'DEM',
    'LandUse': '土地利用',
    'UnderwaterRelief': '水下地形',
    'HydrogeologicalMap': '水文地质图',
    'EFDC_InitialWaterLevel': 'EFDC初始水位',
    'HRU': 'HRU',
    'EFDC_Parameter': 'EFDC参数',
    'MODFLOW_InitialWaterLevel': 'MODFLOW初始水位',
    'MODFLOW_InitialWaterLevel_Observation': 'MODFLOW初始水位观测数据',
    'SurfaceRive_Point': '地表河流点',
    'SurfaceRive_Point_Observation': '地表河流点观测数据',
    'HRU_Observation': 'HRU参数',
    'Junction_Observation': 'Junction参数',
    'RainGauge_Observation': 'RainGauge参数',
    'AdministrativeDivision': '行政区划',
    'River': '水系数据',
}


def get_all_upload_files_from_table():
    table_name = "admin_" + "project_setting"
    sql = "select * from {} order by fid".format(table_name)
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    translated_results = []

    for row in results:
        if "Observation" not in row[1]:
            column_name = column_mapping[row[1]]
            translated_results.append(column_name)

    return translated_results


def get_all_layers_from_table():
    table_name = "admin_" + "project_setting"
    sql = "select * from {} order by fid".format(table_name)
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    translated_results = []

    for row in results:
        if "Parameter" in row[2] or "Observation" in row[2] or "HRU" in row[2] or "Junction" in row[2]:
            continue
        else:
            data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': row[2]}
            translated_results.append(data)
            print(data)
    print(len(translated_results))
    return translated_results


def get_data_from_project(table_names):
    data_list = []
    for table_name in table_names:
        sql = "SELECT * FROM {} ORDER BY fid".format(table_name[0])
        with connection.cursor() as cursor:
            cursor.execute(sql)
            cursor.description = cursor.description  # 设置游标的description属性
            results = cursor.fetchall()

        columns = [col[0] for col in cursor.description]

        columns = map_fields_to_chinese(columns, table_name[0])

        data = []
        for row in results:
            row_dict = dict(zip(columns, row))
            data.append(row_dict)
        data_list.append({table_name[0]: data})

    return data_list


def map_fields_to_chinese(english_fields, mapping_key):
    # 创建映射字典
    field_mappings = {
        'MODFLOW_InitialWaterLevel_Observation': {
            'fid': '编号',
            'name': '监测点名称',
            'layer': '地下水分层',
            'initialhead': '观测水位'
        }
    }

    tables = mapping_key.split("_", 1)[1]
    print(tables)

    # 根据映射键选择相应的映射字典
    field_mapping = field_mappings.get(tables, {})

    # 将英文字段名转换为中文字段名
    chinese_fields_mapping = [field_mapping.get(field, field) for field in english_fields]

    return chinese_fields_mapping


def modifyData(body_data):
    table_name = ""

    table_name = "Admin_" + body_data['table']
    del body_data['table']

    sql = update_into_table_from_body_sql(table_name, body_data)

    cursor = connection.cursor()
    cursor.execute(sql)
