"""
URL configuration for Web_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from PublicServices import views as PublicServicesViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # region 保留设计，按照快速开发原则，设计标准文件，只上传数据，然后入库发布。
    # # 用于操作基础数据服务//基础地理数据//研究区范围
    # path('UpLoadFiles/BasicDataService/BasicGeographicData/StudyAreaScope',
    #      PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_StudyAreaScope),
    #
    # path('creat/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
    #      PublicServicesViews.creat_BasicDataService_BasicGeographicData_StudyAreaScope_Table),
    #
    # path('update/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
    #      PublicServicesViews.update_BasicDataService_BasicGeographicData_StudyAreaScope_Table),
    #
    # path('publish/BasicDataService/BasicGeographicData/StudyAreaScope',
    #      PublicServicesViews.publish_BasicDataService_BasicGeographicData_StudyAreaScope),
    #
    # # 用于操作基础数据服务//监测数据//河流监测站点//流量
    # path('upLoad/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),
    #
    # path('creat/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),
    #
    # path('update/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),
    #
    # path('publish/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),
    #
    # # 用于操作基础数据服务//监测数据/气象监测站点//水温
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//大气压强
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//蒸发量
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//降雨量
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//太阳辐射
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//云量
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover),
    #
    # # 用于操作基础数据服务//监测数据//气象监测站点//风速风向
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection),
    #
    # # 用于操作基础数据服务//监测数据/气象监测站点//水温
    # path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature',
    #      PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature),
    #
    # path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature/Table',
    #      PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table),
    #
    # path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature/Table',
    #      PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table),
    #
    # path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature',
    #      PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature),
    #
    # # 用于操作空间离散数据//SWMM空间离散
    # path('upLoad/SpatialDiscreteData/SWMMSpatialDiscreteData',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_SWMMSpatialDiscreteData),
    #
    # path('creat/SpatialDiscreteData/SWMMSpatialDiscreteData/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_SWMMSpatialDiscreteData_Table),
    #
    # path('update/SpatialDiscreteData/SWMMSpatialDiscreteData/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_SWMMSpatialDiscreteData_Table),
    #
    # path('publish/SpatialDiscreteData/SWMMSpatialDiscreteData',
    #      PublicServicesViews.publish_SpatialDiscreteData_SWMMSpatialDiscreteData),
    #
    # # 用于操作空间离散数据//EFDC空间离散
    # path('upLoad/SpatialDiscreteData/EFDCSpatialDiscreteData',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_EFDCSpatialDiscreteData),
    #
    # path('creat/SpatialDiscreteData/EFDCSpatialDiscreteData/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_EFDCSpatialDiscreteData_Table),
    #
    # path('update/SpatialDiscreteData/EFDCSpatialDiscreteData/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_EFDCSpatialDiscreteData_Table),
    #
    # path('publish/SpatialDiscreteData/EFDCSpatialDiscreteData',
    #      PublicServicesViews.publish_SpatialDiscreteData_EFDCSpatialDiscreteData),
    #
    # # 用于操作空间离散数据//MODFLOW空间离散
    # path('upLoad/SpatialDiscreteData/MODFLOWSpatialDiscreteData',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_MODFLOWSpatialDiscreteData),
    #
    # path('creat/SpatialDiscreteData/MODFLOWSpatialDiscreteData/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_MODFLOWSpatialDiscreteData_Table),
    #
    # path('update/SpatialDiscreteData/MODFLOWSpatialDiscreteData/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_MODFLOWSpatialDiscreteData_Table),
    #
    # path('publish/SpatialDiscreteData/MODFLOWSpatialDiscreteData',
    #      PublicServicesViews.publish_SpatialDiscreteData_MODFLOWSpatialDiscreteData),
    #
    # # 用于操作空间离散数据//SWMM-EFDC空间离散
    # path('upLoad/SpatialDiscreteData/SWMMandEFDCInteractiveUnit',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_SWMMandEFDCInteractiveUnit),
    #
    # path('creat/SpatialDiscreteData/SWMMandEFDCInteractiveUnit/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_SWMMandEFDCInteractiveUnit_Table),
    #
    # path('update/SpatialDiscreteData/SWMMandEFDCInteractiveUnit/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_SWMMandEFDCInteractiveUnit_Table),
    #
    # path('publish/SpatialDiscreteData/SWMMandEFDCInteractiveUnit',
    #      PublicServicesViews.publish_SpatialDiscreteData_SWMMandEFDCInteractiveUnit),
    #
    # # 用于操作空间离散数据//SWMM-MODFLOW空间离散
    # path('upLoad/SpatialDiscreteData/SWMMandMODFLOWInteractiveUnit',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit),
    #
    # path('creat/SpatialDiscreteData/SWMMandMODFLOWInteractiveUnit/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit_Table),
    #
    # path('update/SpatialDiscreteData/SWMMandMODFLOWInteractiveUnit/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit_Table),
    #
    # path('publish/SpatialDiscreteData/SWMMandMODFLOWInteractiveUnit',
    #      PublicServicesViews.publish_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit),
    #
    # # 用于操作空间离散数据//EFDC-MODFLOW空间离散
    # path('upLoad/SpatialDiscreteData/EFDCandMODFLOWInteractiveUnit',
    #      PublicServicesViews.upLoad_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit),
    #
    # path('creat/SpatialDiscreteData/EFDCandMODFLOWInteractiveUnit/Table',
    #      PublicServicesViews.creat_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit_Table),
    #
    # path('update/SpatialDiscreteData/EFDCandMODFLOWInteractiveUnit/Table',
    #      PublicServicesViews.update_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit_Table),
    #
    # path('publish/SpatialDiscreteData/EFDCandMODFLOWInteractiveUnit',
    #      PublicServicesViews.publish_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit),
    #
    # # 用于操作模型数据//SWMM//空间离散//雨量计
    # path('upLoad/ModelData/SWMM/SpatialDiscrete/RainGauge',
    #      PublicServicesViews.upLoad_ModelData_SWMM_SpatialDiscrete_RainGauge),
    #
    # path('creat/ModelData/SWMM/SpatialDiscrete/RainGauge/Table',
    #      PublicServicesViews.creat_ModelData_SWMM_SpatialDiscrete_RainGauge_Table),
    #
    # path('update/ModelData/SWMM/SpatialDiscrete/RainGauge/Table',
    #      PublicServicesViews.update_ModelData_SWMM_SpatialDiscrete_RainGauge_Table),
    #
    # path('publish/ModelData/SWMM/SpatialDiscrete/RainGauge/',
    #      PublicServicesViews.publish_ModelData_SWMM_SpatialDiscrete_RainGauge),
    #
    # # 用于操作模型数据//MODFLOW//渗透（水力传导）
    # path('upLoad/ModelData/MODFLOW/Infiltration',
    #      PublicServicesViews.upLoad_ModelData_MODFLOW_Infiltration),
    #
    # path('creat/ModelData/MODFLOW/Infiltration/Table',
    #      PublicServicesViews.creat_ModelData_MODFLOW_Infiltration_Table),
    #
    # path('update/ModelData/MODFLOW/Infiltration/Table',
    #      PublicServicesViews.update_ModelData_MODFLOW_Infiltration_Table),
    #
    # path('publish/ModelData/MODFLOW/Infiltration',
    #      PublicServicesViews.publish_ModelData_MODFLOW_Infiltration),
    # endregion

    path('upLoadFiles/BasicDataService/BasicGeographicData/StudyAreaScope',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_StudyAreaScope),

    path('upLoad/BasicDataService/BasicGeographicData/River',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_River),

    path('upLoad/BasicDataService/BasicGeographicData/AdministrativeDivision',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_AdministrativeDivision),

    path('upLoad/BasicDataService/BasicGeographicData/LandUse',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_LandUse),

    path('upLoad/BasicDataService/BasicGeographicData/HydrogeologicalMap',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_HydrogeologicalMap),

    path('upLoad/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),

    path('upLoad/BasicDataService/MonitoringData/RiverMonitoringStation/UnderwaterRelief',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_UnderwaterRelief),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection),

    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature),

    path('upLoad/BasicDataService/GeologicalData/GeologicalBody',
         PublicServicesViews.upLoad_BasicDataService_GeologicalData_GeologicalBody),

    path('upLoad/BasicDataService/TopographicData/DEM',
         PublicServicesViews.upLoad_BasicDataService_TopographicData_DEM),

    path('upLoad/SpatialDiscreteData/SWMMSpatialDiscreteData',
         PublicServicesViews.upLoad_SpatialDiscreteData_SWMMSpatialDiscreteData),

    path('upLoad/SpatialDiscreteData/EFDCSpatialDiscreteData',
         PublicServicesViews.upLoad_SpatialDiscreteData_EFDCSpatialDiscreteData),

    path('upLoad/SpatialDiscreteData/MODFLOWSpatialDiscreteData',
         PublicServicesViews.upLoad_SpatialDiscreteData_MODFLOWSpatialDiscreteData),

    path('upLoad/SpatialDiscreteData/SWMMandEFDCInteractiveUnit',
         PublicServicesViews.upLoad_SpatialDiscreteData_SWMMandEFDCInteractiveUnit),

    path('upLoad/SpatialDiscreteData/SWMMandMODFLOWInteractiveUnit',
         PublicServicesViews.upLoad_SpatialDiscreteData_SWMMandMODFLOWInteractiveUnit),

    path('upLoad/SpatialDiscreteData/EFDCandMODFLOWInteractiveUnit',
         PublicServicesViews.upLoad_SpatialDiscreteData_EFDCandMODFLOWInteractiveUnit),

    path('upLoad/ModelData/SWMM/SpatialDiscrete/RainGauge',
         PublicServicesViews.upLoad_ModelData_SWMM_SpatialDiscrete_RainGauge),

    path('upLoad/ModelData/SWMM/SpatialDiscrete/Junction',
         PublicServicesViews.upLoad_ModelData_SWMM_SpatialDiscrete_Junction),

    path('upLoad/ModelData/SWMM/ParameterDiscrete/HRU',
         PublicServicesViews.upLoad_ModelData_SWMM_ParameterDiscrete_HRU),

    path('upLoad/ModelData/SWMM/ParameterDiscrete/RainGauge',
         PublicServicesViews.upLoad_ModelData_SWMM_ParameterDiscrete_RainGauge),

    path('upLoad/ModelData/SWMM/ParameterDiscrete/Junction',
         PublicServicesViews.upLoad_ModelData_SWMM_ParameterDiscrete_Junction),

    path('upLoad/ModelData/MODFLOW/Infiltration',
         PublicServicesViews.upLoad_ModelData_MODFLOW_Infiltration),

    path('upLoad/ModelData/MODFLOW/StoreWater',
         PublicServicesViews.upLoad_ModelData_MODFLOW_StoreWater),

    path('upLoad/ModelData/MODFLOW/InitialWaterLevel',
         PublicServicesViews.upLoad_ModelData_MODFLOW_InitialWaterLevel),

    path('upLoad/ModelData/MODFLOW/SurfaceRive',
         PublicServicesViews.upLoad_ModelData_MODFLOW_SurfaceRive),

    path('upLoad/ModelData/EFDC/InitialWaterLevel',
         PublicServicesViews.upLoad_ModelData_EFDC_InitialWaterLevel),

    path('upLoad/ModelData/EFDC/Parameter',
         PublicServicesViews.upLoad_ModelData_EFDC_Parameter),

    path('get/total/time',
         PublicServicesViews.get_total_time),

    path('set/swmm/time',
         PublicServicesViews.set_swmm_time),

    path('set/modflow/time',
         PublicServicesViews.set_modflow_time),

    path('set/efdc/time',
         PublicServicesViews.set_efdc_time),

    path('get/all/upload/files', PublicServicesViews.get_all_upload_files),

    path('get/all/layers', PublicServicesViews.get_all_layers),

    path('run/file', PublicServicesViews.run_file),

    path('modify/data', PublicServicesViews.modify_data)
]
