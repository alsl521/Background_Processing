from django.http import JsonResponse

# 自定义方法
from Utils.Result import Result
from ProcessFiles.HandlingCompressedFiles.HandlingCompressedFiles import handling_compressed_files
from DatabasContent.ShpToDatabaseTable import create_table_from_form, create_table_from_data
from ProcessFiles.HandlingShapeFiles.ShpProcess import get_shp_field_attributes
from DatabasContent.DatabaseTable import update_table_from_form_shp
from MapService.PublishMapService import publish_Shp
from ProcessFiles.HandlingSpreadsheetFiles.HandlingSpreadsheetFiles import handling_spreadsheet_files
from ProcessFiles.HandlingSpreadsheetFiles.HandlingXlsxFiles import get_xlsx_files_attributes
from Utils.ProcessRequestBody import get_same_attributes_from_request_body


# 用于操作基础数据服务//基础地理数据//研究区范围
def upLoad_BasicDataService_BasicGeographicData_StudyAreaScope(request):
    if request.method == 'POST':

        file_name = "BasicDataService_BasicGeographicData_StudyAreaScope"
        path = "BasicDataService\\BasicGeographicData\\StudyAreaScope"
        shpName = "StudyAreaScope"

        file = request.FILES.get("file")
        # 处理压缩文件
        handling_compressed_files(file_name, file)

        # 获取字段属性
        field_attributes = get_shp_field_attributes(path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        # 获取默认数据
        data = {'type': 1, 'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': "StudyAreaScope"}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_BasicGeographicData_StudyAreaScope_Table(request):
    path = "BasicDataService\\BasicGeographicData\\StudyAreaScope"
    shpName = "StudyAreaScope"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_BasicGeographicData_StudyAreaScope_Table(request):
    shpName = "StudyAreaScope"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_BasicGeographicData_StudyAreaScope(request):
    path = "BasicDataService\\BasicGeographicData\\StudyAreaScope"
    shpName = "StudyAreaScope"
    tableName = publish_Shp(path, shpName)
    data = {'type': 1, 'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# 用于操作基础数据服务//监测数据//河流监测站点//流量
def upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate(request):
    if request.method == 'POST':
        field_attributes = None
        xlsx_attributes = None

        file_name = "BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate"
        path = "BasicDataService\\MonitoringData\\RiverMonitoringStation\\FlowRate"
        shpName = "FlowRate"

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
        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        # 获取默认数据
        data = {'type': 1, 'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': "StudyAreaScope"}
        return JsonResponse(Result.success().to_dict())


def creat_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table(request):
    path = "BasicDataService\\MonitoringData\\RiverMonitoringStation\\FlowRate"
    shpName = "FlowRate"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table(request):
    shpName = "FlowRate"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate(request):
    shpName = "FlowRate"
    path = "BasicDataService\\MonitoringData\\RiverMonitoringStation\\FlowRate"
    tableName = publish_Shp(path, shpName)
    data = {'type': 1, 'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())
