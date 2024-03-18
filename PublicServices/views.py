from django.http import JsonResponse

# 自定义方法
from Utils.Result import Result
from DatabasContent.ShpToDatabaseTable import create_table_from_form, create_table_from_data
from DatabasContent.DatabaseTable import update_table_from_form_shp, get_project_setting, update_project_setting
from MapService.PublishMapService import publish_Shp
from Utils.ProcessRequestBody import get_same_attributes_from_request_body, get_field_attributes_and_xlsx_attributes, \
    get_field_attributes


# region 基础数据服务//基础地理数据//研究区范围
# 用于操作基础数据服务//基础地理数据//研究区范围
def upLoad_BasicDataService_BasicGeographicData_StudyAreaScope(request):
    if request.method == 'POST':

        file_name = "BasicDataService_BasicGeographicData_StudyAreaScope"
        path = "BasicDataService\\BasicGeographicData\\StudyAreaScope"
        shpName = "StudyAreaScope"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "StudyAreaScope"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
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
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据//河流监测站点//流量
# 用于操作基础数据服务//监测数据//河流监测站点//流量
def upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate"
        path = "BasicDataService\\MonitoringData\\RiverMonitoringStation\\FlowRate"
        shpName = "FlowRate"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "FlowRate"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


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
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//气温
# 用于操作基础数据服务//监测数据/气象监测站点//气温
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Temperature"
        shpName = "Temperature"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "Temperature"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Temperature"
    shpName = "Temperature"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table(request):
    shpName = "Temperature"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Temperature"
    shpName = "Temperature"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//大气压强
# 用于操作基础数据服务//监测数据//气象监测站点//大气压强
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\AtmosphericPressure"
        shpName = "AtmosphericPressure"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "AtmosphericPressure"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\AtmosphericPressure"
    shpName = "AtmosphericPressure"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table(request):
    shpName = "AtmosphericPressure"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\AtmosphericPressure"
    shpName = "AtmosphericPressure"

    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//蒸发量
# 用于操作基础数据服务//监测数据//气象监测站点//蒸发量
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Evaporation"
        shpName = "Evaporation"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "Evaporation"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Evaporation"
    shpName = "Evaporation"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table(request):
    shpName = "Evaporation"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Evaporation"
    shpName = "Evaporation"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//降雨量
# 用于操作基础数据服务//监测数据//气象监测站点//降雨量
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Rainfall"
        shpName = "Rainfall"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "Rainfall"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Rainfall"
    shpName = "Rainfall"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table(request):
    shpName = "Rainfall"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\Rainfall"
    shpName = "Rainfall"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//太阳辐射
# 用于操作基础数据服务//监测数据//气象监测站点//太阳辐射
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\SolarRadiation"
        shpName = "SolarRadiation"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "SolarRadiation"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\SolarRadiation"
    shpName = "SolarRadiation"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table(request):
    shpName = "SolarRadiation"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\SolarRadiation"
    shpName = "SolarRadiation"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//云量
# 用于操作基础数据服务//监测数据//气象监测站点//云量
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\CloudCover"
        shpName = "CloudCover"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "CloudCover"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\CloudCover"
    shpName = "CloudCover"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table(request):
    shpName = "CloudCover"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\CloudCover"
    shpName = "CloudCover"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//风速风向
# 用于操作基础数据服务//监测数据//气象监测站点//风速风向
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WindSpeedAndDirection"
        shpName = "WindSpeedAndDirection"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "WindSpeedAndDirection"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WindSpeedAndDirection"
    shpName = "WindSpeedAndDirection"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table(request):
    shpName = "WindSpeedAndDirection"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WindSpeedAndDirection"
    shpName = "WindSpeedAndDirection"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 基础数据服务//监测数据/气象监测站点//水温
# 用于操作基础数据服务//监测数据/气象监测站点//水温
def upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature(request):
    if request.method == 'POST':

        file_name = "BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature"
        path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WaterTemperature"
        shpName = "WaterTemperature"

        field_attributes, xlsx_attributes = get_field_attributes_and_xlsx_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes, 'xlsx_attributes': xlsx_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "WaterTemperature"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WaterTemperature"
    shpName = "WaterTemperature"
    shp_attributes_list, observation_attributes_list = get_same_attributes_from_request_body(request.body)
    shp_data, observation_data = create_table_from_data(shp_attributes_list, path, shpName,
                                                        observation_attributes_list)
    data = {'shp_data': shp_data, 'observation_data': observation_data}
    return JsonResponse(Result.success(data=data).to_dict())


def update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table(request):
    shpName = "WaterTemperature"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature(request):
    path = "BasicDataService\\MonitoringData\\MeteorologicalMonitoringStation\\WaterTemperature"
    shpName = "WaterTemperature"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 2)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//SWMM空间离散
# 用于操作空间离散数据//SWMM空间离散
def upLoad_SpatialDiscreteData_SWMMSpatialDiscreteData(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_SWMMSpatialDiscreteData"
        path = "SpatialDiscreteData\\SWMMSpatialDiscreteData"
        shpName = "SWMMSpatialDiscreteData"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_SWMMSpatialDiscreteData_Table(request):
    path = "SpatialDiscreteData\\SWMMSpatialDiscreteData"
    shpName = "SWMMSpatialDiscreteData"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_SWMMSpatialDiscreteData_Table(request):
    shpName = "SWMMSpatialDiscreteData"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_SWMMSpatialDiscreteData(request):
    path = "SpatialDiscreteData\\SWMMSpatialDiscreteData"
    shpName = "SWMMSpatialDiscreteData"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//EFDC空间离散
# 用于操作空间离散数据//EFDC空间离散
def upLoad_SpatialDiscreteData_EFDCSpatialDiscreteData(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_EFDCSpatialDiscreteData"
        path = "SpatialDiscreteData\\EFDCSpatialDiscreteData"
        shpName = "EFDCSpatialDiscreteData"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_EFDCSpatialDiscreteData_Table(request):
    path = "SpatialDiscreteData\\EFDCSpatialDiscreteData"
    shpName = "EFDCSpatialDiscreteData"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_EFDCSpatialDiscreteData_Table(request):
    shpName = "EFDCSpatialDiscreteData"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_EFDCSpatialDiscreteData(request):
    path = "SpatialDiscreteData\\EFDCSpatialDiscreteData"
    shpName = "EFDCSpatialDiscreteData"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//MODFLOW空间离散
# 用于操作空间离散数据//MODFLOW空间离散
def upLoad_SpatialDiscreteData_MODFLOWSpatialDiscreteData(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_MODFLOWSpatialDiscreteData"
        path = "SpatialDiscreteData\\MODFLOWSpatialDiscreteData"
        shpName = "MODFLOWSpatialDiscreteData"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_MODFLOWSpatialDiscreteData_Table(request):
    path = "SpatialDiscreteData\\MODFLOWSpatialDiscreteData"
    shpName = "MODFLOWSpatialDiscreteData"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_MODFLOWSpatialDiscreteData_Table(request):
    shpName = "MODFLOWSpatialDiscreteData"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_MODFLOWSpatialDiscreteData(request):
    path = "SpatialDiscreteData\\MODFLOWSpatialDiscreteData"
    shpName = "MODFLOWSpatialDiscreteData"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//SWMM-EFDC交互单元
# 用于操作空间离散数据//SWMM-EFDC交互单元
def upLoad_SpatialDiscreteData_SWMMandEFDCInteractiveUnit(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_SWMMandEFDCInteractiveUnit"
        path = "SpatialDiscreteData\\SWMMandEFDCInteractiveUnit"
        shpName = "SWMMandEFDCInteractiveUnit"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_SWMMandEFDCInteractiveUnit_Table(request):
    path = "SpatialDiscreteData\\SWMMandEFDCInteractiveUnit"
    shpName = "SWMMandEFDCInteractiveUnit"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_SWMMandEFDCInteractiveUnit_Table(request):
    shpName = "SWMMandEFDCInteractiveUnit"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_SWMMandEFDCInteractiveUnit(request):
    path = "SpatialDiscreteData\\SWMMandEFDCInteractiveUnit"
    shpName = "SWMMandEFDCInteractiveUnit"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//SWMM-MODFLOW交互单元
# 用于操作空间离散数据//SWMM-MODFLOW交互单元
def upLoad_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit"
        path = "SpatialDiscreteData\\SWMMandMODFLOWInteractiveUnit"
        shpName = "SWMMandMODFLOWInteractiveUnit"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit_Table(request):
    path = "SpatialDiscreteData\\SWMMandMODFLOWInteractiveUnit"
    shpName = "SWMMandMODFLOWInteractiveUnit"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit_Table(request):
    shpName = "SWMMandMODFLOWInteractiveUnit"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit(request):
    path = "SpatialDiscreteData\\SWMMandMODFLOWInteractiveUnit"
    shpName = "SWMMandMODFLOWInteractiveUnit"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 空间离散数据//EFDC-MODFLOW交互单元
# 用于操作空间离散数据//EFDC-MODFLOW交互单元
def upLoad_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit(request):
    if request.method == 'POST':
        file_name = "SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit"
        path = "SpatialDiscreteData\\EFDCandMODFLOWInteractiveUnit"
        shpName = "EFDCandMODFLOWInteractiveUnit"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit_Table(request):
    path = "SpatialDiscreteData\\EFDCandMODFLOWInteractiveUnit"
    shpName = "EFDCandMODFLOWInteractiveUnit"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit_Table(request):
    shpName = "EFDCandMODFLOWInteractiveUnit"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit(request):
    path = "SpatialDiscreteData\\EFDCandMODFLOWInteractiveUnit"
    shpName = "EFDCandMODFLOWInteractiveUnit"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion


# region 模型数据//SWMM//空间离散//雨量计数据
# 用于操作空模型数据//SWMM//空间离散/雨量计数据
def upLoad_ModelData_SWMM_SpatialDiscrete_RainGauge(request):
    if request.method == 'POST':
        file_name = "ModelData_SWMM_SpatialDiscrete_RainGauge"
        path = "ModelData\\SWMM\\SpatialDiscrete\\RainGauge"
        shpName = "RainGauge"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_SWMM_SpatialDiscrete_RainGauge_Table(request):
    path = "ModelData\\SWMM\\SpatialDiscrete\\RainGauge"
    shpName = "RainGauge"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_SWMM_SpatialDiscrete_RainGauge_Table(request):
    shpName = "RainGauge"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_SWMM_SpatialDiscrete_RainGauge(request):
    path = "ModelData\\SWMM\\SpatialDiscrete\\RainGauge"
    shpName = "RainGauge"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 模型数据//SWMM//空间离散//铰点数据
# 用于操作空模型数据//SWMM//空间离散//铰点数据
def upLoad_ModelData_SWMM_SpatialDiscrete_Junction(request):
    if request.method == 'POST':
        file_name = "ModelData_SWMM_SpatialDiscrete_Junction"
        path = "ModelData\\SWMM\\SpatialDiscrete\\Junction"
        shpName = "Junction"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_SWMM_SpatialDiscrete_Junction_Table(request):
    path = "ModelData\\SWMM\\SpatialDiscrete\\Junction"
    shpName = "Junction"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_SWMM_SpatialDiscrete_Junction_Table(request):
    shpName = "Junction"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_SWMM_SpatialDiscrete_Junction(request):
    path = "ModelData\\SWMM\\SpatialDiscrete\\Junction"
    shpName = "Junction"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

def update_ModelData_SWMM_TimeDispersion(request):
    print("SS")


# region 模型数据//SWMM//参数设置//HRU参数
# 用于操作空模型数据//SWMM//参数设置/HRU参数
def upLoad_ModelData_SWMM_ParameterSetting_HRU(request):
    if request.method == 'POST':
        file_name = "ModelData_SWMM_ParameterSetting_HRU"
        path = "ModelData\\SWMM\\ParameterSetting\\HRU"
        shpName = "HRU"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_SWMM_ParameterSetting_HRU_Table(request):
    path = "ModelData\\SWMM\\ParameterSetting\\HRU"
    shpName = "HRU"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_SWMM_ParameterSetting_HRU_Table(request):
    shpName = "HRU"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_SWMM_ParameterSetting_HRU(request):
    path = "ModelData\\SWMM\\ParameterSetting\\HRU"
    shpName = "HRU"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 模型数据//SWMM//参数设置//雨量计参数
# 用于操作空模型数据//SWMM//参数设置//雨量计参数
def upLoad_ModelData_SWMM_ParameterSetting_RainGauge(request):
    if request.method == 'POST':
        file_name = "ModelData_SWMM_ParameterSetting_RainGauge"
        path = "ModelData\\SWMM\\ParameterSetting\\RainGauge"
        shpName = "RainGauge"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_SWMM_ParameterSetting_RainGauge_Table(request):
    path = "ModelData\\SWMM\\ParameterSetting\\RainGauge"
    shpName = "RainGauge"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_SWMM_ParameterSetting_RainGauge_Table(request):
    shpName = "RainGauge"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_SWMM_ParameterSetting_RainGauge(request):
    path = "ModelData\\SWMM\\ParameterSetting\\RainGauge"
    shpName = "RainGauge"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion

# region 模型数据//SWMM//参数设置//节点参数
# 用于操作空模型数据//SWMM//参数设置//节点参数
def upLoad_ModelData_SWMM_ParameterSetting_Junction(request):
    if request.method == 'POST':
        file_name = "ModelData_SWMM_ParameterSetting_Junction"
        path = "ModelData//SWMM//ParameterSetting//Junction"
        shpName = "Junction"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_SWMM_ParameterSetting_Junction_Table(request):
    path = "ModelData//SWMM//ParameterSetting//Junction"
    shpName = "Junction"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_SWMM_ParameterSetting_PointFile_Junction_Table(request):
    shpName = "EFDCandMODFLOWSSpatialDiscreteData"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_SWMM_ParameterSetting_JunctionJunction(request):
    path = "ModelData//SWMM//ParameterSetting//Junction"
    shpName = "Junction"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# endregion


# 用于操作模型数据//MODFLOW//渗透（水力传导）
def upLoad_ModelData_MODFLOW_Infiltration(request):
    if request.method == 'POST':

        file_name = "ModelData_MODFLOW_Infiltration"
        path = "ModelData\\MODFLOW\\Infiltration"
        shpName = "Infiltration"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "Infiltration"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_MODFLOW_Infiltration_Table(request):
    path = "ModelData\\MODFLOW\\Infiltration"
    shpName = "Infiltration"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_MODFLOW_Infiltration_Table(request):
    shpName = "Infiltration"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_MODFLOW_Infiltration(request):
    path = "ModelData\\MODFLOW\\Infiltration"
    shpName = "Infiltration"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# 用于操作模型数据//MODFLOW//贮水（给水度）
def upLoad_ModelData_MODFLOW_WaterStorage(request):
    if request.method == 'POST':

        file_name = "ModelData_MODFLOW_WaterStorage"
        path = "ModelData\\MODFLOW\\WaterStorage"
        shpName = "WaterStorage"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "WaterStorage"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_MODFLOW_WaterStorage_Table(request):
    path = "ModelData\\MODFLOW\\WaterStorage"
    shpName = "WaterStorage"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_MODFLOW_WaterStorage_Table(request):
    shpName = "WaterStorage"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_MODFLOW_WaterStorage(request):
    path = "ModelData\\MODFLOW\\WaterStorage"
    shpName = "WaterStorage"
    tableName = publish_Shp(path, shpName)
    update_project_setting(shpName, 1)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# 用于操作模型数据//MODFLOW//时间离散
def update_ModelData_MODFLOW_TimeDispersion(request):
    print("SS")


# 用于操作模型数据//MODFLOW//初始水位
def upLoad_ModelData_MODFLOW_InitialWaterLevel(request):
    if request.method == 'POST':

        file_name = "ModelData_MODFLOW_InitialWaterLevel"
        path = "ModelData\\MODFLOW\\InitialWaterLevel"
        shpName = "InitialWaterLevel"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "InitialWaterLevel"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_MODFLOW_InitialWaterLevel_Table(request):
    path = "ModelData\\MODFLOW\\InitialWaterLevel"
    shpName = "InitialWaterLevel"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_MODFLOW_InitialWaterLevel_Table(request):
    shpName = "InitialWaterLevel"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_MODFLOW_InitialWaterLevel(request):
    path = "ModelData\\MODFLOW\\InitialWaterLevel"
    shpName = "InitialWaterLevel"
    tableName = publish_Shp(path, shpName)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# 用于操作模型数据//MODFLOW//路表河流
def upLoad_ModelData_MODFLOW_River(request):
    if request.method == 'POST':

        file_name = "ModelData_MODFLOW_River"
        path = "ModelData\\MODFLOW\\River"
        shpName = "River"

        # 获取字段属性
        field_attributes = get_field_attributes(request, file_name, path, shpName)

        data = {'field_attributes': field_attributes}
        return JsonResponse(Result.success(data=data).to_dict())
    elif request.method == 'GET':
        shpName = "River"

        tableName = get_project_setting(shpName)
        # 获取默认数据
        data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
        return JsonResponse(Result.success(data=data).to_dict())


def creat_ModelData_MODFLOW_River_Table(request):
    path = "ModelData\\MODFLOW\\River"
    shpName = "River"
    value = create_table_from_form(request.body, path, shpName)
    data = {'value': value}
    return JsonResponse(Result.success(data=data).to_dict())


def update_ModelData_MODFLOW_River_Table(request):
    shpName = "River"
    update_table_from_form_shp(request.body, shpName)
    return JsonResponse(Result.success().to_dict())


def publish_ModelData_MODFLOW_River(request):
    path = "ModelData\\MODFLOW\\River"
    shpName = "River"
    tableName = publish_Shp(path, shpName)
    data = {'url': "http://localhost:8080/geoserver/ModelCoupling/wms", 'name': tableName}
    return JsonResponse(Result.success(data=data).to_dict())


# 用于操作模型数据//EFDC//时间离散
def update_ModelData_EFDC_TimeDispersion(request):
    print("SS")


# 用于操作模型数据//EFDC//边界条件

# 用于操作模型数据//EFDC//参数设置
def update_ModelData_EFDC_ParameterSetting(request):
    print("SS")
