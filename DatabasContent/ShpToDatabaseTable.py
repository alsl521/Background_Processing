import os
from django.db import connection  # Importing connection for interacting with the database
from osgeo import ogr

from MapService.PublishMapService import publish_Shp
from DatabasContent.DatabaseTable import drop_table_if_exists
# 自建方法
from Utils.DynamicSQL import generate_create_table_sql, map_chinese_to_english
from ProcessFiles.HandlingShapeFiles.ShpProcess import get_Shp_Field_Attributes, get_epsg_from_prj


def get_shapefile_names_in_folder(folder_path):
    """
    获取文件夹中所有.shp文件的文件名（不包含扩展名）。

    Args:
        folder_path (str): 文件夹路径。

    Returns:
        list: .shp文件的文件名列表。

    """

    # 获取文件夹下所有.shp文件的文件名（不包含扩展名）
    shapefile_names = [os.path.splitext(file)[0] for file in os.listdir(folder_path) if file.lower().endswith('.shp')]
    return shapefile_names[0]


def shp_to_database_table(path):
    """
    处理Shapefile，创建表并插入数据。

    Args:
        path (str): Shapefile所在文件夹的路径。

    Returns:
        str: 创建的表名。

    """

    # ==============================
    # 定义函数内变量
    layer = None
    epsg_code = None
    attribute_info_list = []  # 用于存储属性字段信息的列表

    # 创建表逻辑处理
    shpName = get_shapefile_names_in_folder(path)

    # 获取Shapefile的驱动程序
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile_path = os.path.join(path, shpName + ".shp")

    # 打开Shapefile
    dataset = driver.Open(shapefile_path)

    # 检查是否成功打开Shapefile
    if dataset is None:
        print('Error: Could not open the Shapefile')
    else:
        print('Shapefile opened successfully')

    # 创建数据库连接的游标
    cursor = connection.cursor()

    # 将数据库表转为标准格式的名称
    table_name = map_chinese_to_english(shpName)

    # 如果表已经存在则将其删除掉
    drop_table_if_exists(table_name)

    # 打开Shapefile
    shapefile = ogr.Open(shapefile_path)

    if shapefile:
        # 获取第一个图层（Assuming there is only one layer in the Shapefile）
        layer = shapefile.GetLayer(0)
        attribute_info_list = get_Shp_Field_Attributes(layer)

    else:
        print("Failed to open the Shapefile.")

    # 获取动态sql语句
    dynamicSql = generate_create_table_sql(table_name, attribute_info_list)
    # 执行sql语句
    cursor.execute(dynamicSql)
    # 执行sql语句
    connection.commit()
    # ==============================

    # ==============================
    # 提交表中数据
    prj_file_path = os.path.join(path, shpName + ".prj")
    epsg_code = get_epsg_from_prj(prj_file_path)

    if epsg_code is not None:
        print(f"The EPSG code is: {epsg_code}")
    else:
        print("Failed to retrieve EPSG code.")

    # 获取字段名
    field_names = [field_info['name'] for field_info in attribute_info_list]

    # 执行sql语句
    for feature in layer:
        # 获取几何信息
        geometry = feature.GetGeometryRef()
        wkt_geometry = geometry.ExportToWkt()

        # 构建动态的INSERT语句
        field_values = [feature.GetField(field_name) for field_name in field_names]
        placeholders = ', '.join(['%s' for _ in field_values])

        sql = f"INSERT INTO {table_name} ({', '.join(field_names)}, geometry) VALUES ({placeholders}, ST_GeomFromText(%s, %s));"

        # 插入数据到PostGIS表
        cursor.execute(sql, tuple(field_values + [wkt_geometry, epsg_code]))

    # 执行sql语句
    connection.commit()

    # 关闭游标
    cursor.close()
    # ==============================
    # 关闭Shapefile
    shapefile = None

    publish_Shp(epsg_code, table_name)

    return table_name
