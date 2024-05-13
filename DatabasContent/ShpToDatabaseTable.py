import json
import os

# 自建方法
from DatabasContent.DatabaseTable import create_table_from_shp, create_table_from_sheet


# def get_shapefile_names_in_folder(folder_path):
#     """
#     获取文件夹中所有.shp文件的文件名（不包含扩展名）。
#
#     Args:
#         folder_path (str): 文件夹路径。
#
#     Returns:
#         list: .shp文件的文件名列表。
#
#     """
#
#     # 获取文件夹下所有.shp文件的文件名（不包含扩展名）
#     shapefile_names = [os.path.splitext(file)[0] for file in os.listdir(folder_path) if file.lower().endswith('.shp')]
#     return shapefile_names[0]
#
#
# def create_table_from_form(request_body, path, shpName):
#     # 解码请求的原始数据
#     body_unicode = request_body.decode('utf-8')
#     # 将数据解析为 JSON 对象
#     body_data = json.loads(body_unicode)
#
#     table_data = create_table_from_shp_data(body_data, path, shpName)
#
#     return table_data
#
#
# def create_table_from_data(shp_attributes_list, path, shpName, observation_attributes_list):
#     shp_data = create_table_from_shp_data(shp_attributes_list, path, shpName)
#     observation_data = create_table_from_SpreadsheetFiles_data(observation_attributes_list, path, shpName)
#     return shp_data, observation_data


def create_table_from_request_shp(path, shpName):
    create_table_from_shp(path, shpName)


def create_table_from_request_sheet(path, shpName):
    create_table_from_sheet(path, shpName)

