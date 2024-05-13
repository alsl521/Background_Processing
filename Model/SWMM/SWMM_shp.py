import geopandas as gpd
import pandas as pd
from django.db import connection

# 建立与数据库的连接

conn = connection
# 定义SWMM存放路径
# filename = 'control.txt'


# 定义查询语句
polygon_key = '[Polygons]'
junction_key = '[COORDINATES]'
raingage_key = '[SYMBOLS]'
end_key = '['


# 打印读取的数据


# 读取多边形
def write_subshp(filename):
    query = f"SELECT name,geometry FROM admin_swmmspatialdiscretedata"
    # 使用geopandas的read_postgis函数读取数据
    gdf = gpd.read_postgis(query, conn, geom_col='geometry')

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if polygon_key in line:
                delete_lines = True
                file.write(line)
                file.write('Subcatchment   X-Coord            Y-Coord          \n')
                file.write(';;-------------- ---------------- ---------------- \n')
                continue

            if end_key in line and delete_lines:
                delete_lines = False
                for index, row in gdf.iterrows():
                    name = row['name']
                    geometry = row['geometry']
                    # 处理MultiPolygon
                    if geometry.geom_type == 'MultiPolygon':
                        polygons = geometry.geoms  # 获取多个Polygon对象
                        for polygon in polygons:
                            coordinates = list(polygon.exterior.coords)
                            # 输出name和点坐标
                            for point in coordinates:
                                file.write(f"{name}          {point[0]}          {point[1]}\n")

                    # 处理单个Polygon
                    elif geometry.geom_type == 'Polygon':
                        coordinates = list(geometry.exterior.coords)
                        # 输出name和点坐标
                        for point in coordinates:
                            file.write(f"{name}          {point[0]}          {point[1]}\n")
                continue
            if not delete_lines:
                file.write(line)


# 读取点
def write_junctionshp(filename):
    query = f"SELECT name,geometry FROM admin_junction"
    # 使用geopandas的read_postgis函数读取数据
    gdf = gpd.read_postgis(query, conn, geom_col='geometry')

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if junction_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Node1           X-Coord            Y-Coord            \n')
                file.write(';;-------------- ---------------- ---------------- \n')
                continue

            if end_key in line and delete_lines:
                delete_lines = False
                for index, row in gdf.iterrows():
                    name = row['name']
                    geometry = row['geometry']
                    # 提取点坐标
                    if geometry.geom_type == 'Point':
                        coordinates = geometry.coords[0]
                        # 写入name和坐标
                        file.write(f"{name}          {coordinates[0]}          {coordinates[1]}\n")
                file.write('\n')
                file.write(line)
                continue
            if not delete_lines:
                file.write(line)


def write_raingageshp(filename):
    query = f"SELECT name,geometry FROM admin_raingauge"
    # 使用geopandas的read_postgis函数读取数据
    gdf = gpd.read_postgis(query, conn, geom_col='geometry')

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if raingage_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Gage           X-Coord            Y-Coord            \n')
                file.write(';;-------------- ---------------- ---------------- \n')
                for index, row in gdf.iterrows():
                    name = row['name']
                    geometry = row['geometry']
                    # 提取点坐标
                    if geometry.geom_type == 'Point':
                        coordinates = geometry.coords[0]
                        # 写入name和坐标
                        file.write(f"{name}          {coordinates[0]}          {coordinates[1]}\n")
                file.write('\n')
                continue
            if not delete_lines:
                file.write(line)
