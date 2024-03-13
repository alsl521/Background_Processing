import json

from ProcessFiles.HandlingCompressedFiles.HandlingCompressedFiles import handling_compressed_files
from ProcessFiles.HandlingShapeFiles.ShpProcess import get_shp_field_attributes
from ProcessFiles.HandlingSpreadsheetFiles.HandlingSpreadsheetFiles import handling_spreadsheet_files
from ProcessFiles.HandlingSpreadsheetFiles.HandlingXlsxFiles import get_xlsx_files_attributes


def get_same_attributes_from_request_body(request_body):
    # 解码请求的原始数据
    body_unicode = request_body.decode('utf-8')
    # 将数据解析为 JSON 对象
    body_data = json.loads(body_unicode)

    # 分类数据
    shp_data = {}
    observation_data = {}

    for key, value in body_data.items():
        if key.startswith("shp_"):
            shp_key = key.replace("shp_", "")
            shp_data[shp_key] = value
        elif key.startswith("observation_"):
            observation_key = key.replace("observation_", "")
            observation_data[observation_key] = value

    return shp_data, observation_data


def get_field_attributes(request, file_name, path, shpName):
    file = request.FILES.get("file")
    # 处理压缩文件
    handling_compressed_files(file_name, file)

    # 获取字段属性
    field_attributes = get_shp_field_attributes(path, shpName)

    return field_attributes


def get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName):
    field_attributes = None
    xlsx_attributes = None

    file1 = request.FILES.get("file1")

    if (file1.name.endswith(".xlsx")
            or file1.name.endswith(".txt")
            or file1.name.endswith(".xls")):
        handling_spreadsheet_files(file_name, file1)
        xlsx_attributes = get_xlsx_files_attributes(path, shpName)
    elif (file1.name.endswith(".zip")
          or file1.name.endswith(".rar")
          or file1.name.endswith(".7z")):
        handling_compressed_files(file_name, file1)
        # 获取字段属性
        field_attributes = get_shp_field_attributes(path, shpName)

    file2 = request.FILES.get("file2")

    if (file2.name.endswith(".xlsx")
            or file2.name.endswith(".txt")
            or file2.name.endswith(".xls")):
        handling_spreadsheet_files(file_name, file2)
        xlsx_attributes = get_xlsx_files_attributes(path, shpName)
    elif (file2.name.endswith(".zip")
          or file2.name.endswith(".rar")
          or file2.name.endswith(".7z")):
        handling_compressed_files(file_name, file2)
        # 获取字段属性
        field_attributes = get_shp_field_attributes(path, shpName)

    return field_attributes, xlsx_attributes
