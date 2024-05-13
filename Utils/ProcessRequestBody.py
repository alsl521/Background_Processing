import json

from DatabasContent.DatabaseTable import update_project_setting, get_project_setting, \
    get_total_time_from_surfacerive_point_observation, set_time_into_table, get_table_from_project, \
    get_data_from_project
from DatabasContent.ShpToDatabaseTable import create_table_from_request_shp, create_table_from_request_sheet
from MapService.PublishMapService import publish_Shp, publish_Tiff
from ProcessFiles.HandlingCompressedFiles.HandlingCompressedFiles import handling_compressed_files
from ProcessFiles.HandlingSpreadsheetFiles.HandlingSpreadsheetFiles import handling_spreadsheet_files


# def get_same_attributes_from_request_body(request_body):
#     # 解码请求的原始数据
#     body_unicode = request_body.decode('utf-8')
#     # 将数据解析为 JSON 对象
#     body_data = json.loads(body_unicode)
#
#     # 分类数据
#     shp_data = {}
#     observation_data = {}
#
#     for key, value in body_data.items():
#         if key.startswith("shp_"):
#             shp_key = key.replace("shp_", "")
#             shp_data[shp_key] = value
#         elif key.startswith("observation_"):
#             observation_key = key.replace("observation_", "")
#             observation_data[observation_key] = value
#
#     return shp_data, observation_data


# def get_field_attributes(request, file_name, path, shpName):
#     file = request.FILES.get("file")
#     # 处理压缩文件
#     handling_compressed_files(file_name, file)
#
#     # 获取字段属性
#     field_attributes = get_shp_field_attributes(path, shpName)
#
#     return field_attributes
#
#
# def get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName):
#     field_attributes = None
#     xlsx_attributes = None
#
#     file1 = request.FILES.get("file1")
#
#     if (file1.name.endswith(".xlsx")
#             or file1.name.endswith(".txt")
#             or file1.name.endswith(".xls")):
#         handling_spreadsheet_files(file_name, file1)
#         xlsx_attributes = get_xlsx_files_attributes(path, shpName)
#     elif (file1.name.endswith(".zip")
#           or file1.name.endswith(".rar")
#           or file1.name.endswith(".7z")):
#         handling_compressed_files(file_name, file1)
#         # 获取字段属性
#         field_attributes = get_shp_field_attributes(path, shpName)
#
#     file2 = request.FILES.get("file2")
#
#     if (file2.name.endswith(".xlsx")
#             or file2.name.endswith(".txt")
#             or file2.name.endswith(".xls")):
#         handling_spreadsheet_files(file_name, file2)
#         xlsx_attributes = get_xlsx_files_attributes(path, shpName)
#     elif (file2.name.endswith(".zip")
#           or file2.name.endswith(".rar")
#           or file2.name.endswith(".7z")):
#         handling_compressed_files(file_name, file2)
#         # 获取字段属性
#         field_attributes = get_shp_field_attributes(path, shpName)
#
#     return field_attributes, xlsx_attributes


def create_and_publish_shp_table_from_request(request, file_name, path, shpName):
    file = request.FILES.get("file")
    # 处理压缩文件
    handling_compressed_files(file_name, file, shpName)

    create_table_from_request_shp(path, shpName)

    publish_Shp(path, shpName)

    update_project_setting(shpName, 1)

    tableName = get_project_setting(shpName)
    return tableName


def create_and_publish_tif_request(request, file_name, path, shpName):
    file = request.FILES.get("file")
    # 处理压缩文件
    handling_compressed_files(file_name, file, shpName)

    publish_Tiff(path, shpName)

    update_project_setting(shpName, 1)

    tableName = get_project_setting(shpName)

    return tableName


def create_and_publish_spreadsheet_request(request, file_name, path, shpName):
    file = request.FILES.get("file")

    # 处理观测记录文件
    handling_spreadsheet_files(file_name, file, shpName)

    create_table_from_request_sheet(path, shpName)

    query_name = shpName + "_Observation"
    update_project_setting(query_name, 1)


def create_and_publish_from_request(request, file_name, path, shpName):
    file1 = request.FILES.get("file1")
    file2 = request.FILES.get("file2")
    # 处理压缩文件
    handling_compressed_files(file_name, file2, shpName)

    create_table_from_request_shp(path, shpName)

    publish_Shp(path, shpName)

    # 处理观测记录文件
    handling_spreadsheet_files(file_name, file1, shpName)

    create_table_from_request_sheet(path, shpName)

    update_project_setting(shpName, 2)

    tableName = get_project_setting(shpName)

    return tableName


def get_total_time_from_table():
    start_time, end_time = get_total_time_from_surfacerive_point_observation()
    return start_time, end_time


def set_time(data_dict):
    set_time_into_table(data_dict)


def get_data(shpName):
    table_name = get_table_from_project(shpName)
    data_list = get_data_from_project(table_name)
    # 解码请求的原始数据
    return data_list

