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

    # 用于操作基础数据服务//基础地理数据//研究区范围
    path('UpLoadFiles/BasicDataService/BasicGeographicData/StudyAreaScope',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_StudyAreaScope),

    path('creat/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
         PublicServicesViews.creat_BasicDataService_BasicGeographicData_StudyAreaScope_Table),

    path('update/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
         PublicServicesViews.update_BasicDataService_BasicGeographicData_StudyAreaScope_Table),

    path('publish/BasicDataService/BasicGeographicData/StudyAreaScope',
         PublicServicesViews.publish_BasicDataService_BasicGeographicData_StudyAreaScope),

    # 用于操作基础数据服务//监测数据//河流监测站点//流量
    path('upLoad/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),

    path('creat/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),

    path('update/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),

    path('publish/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
         PublicServicesViews.publish_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),

    # 用于操作基础数据服务//监测数据/气象监测站点//水温
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Temperature',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Temperature),

    # 用于操作基础数据服务//监测数据//气象监测站点//大气压强
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/AtmosphericPressure',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_AtmosphericPressure),

    # 用于操作基础数据服务//监测数据//气象监测站点//蒸发量
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Evaporation',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Evaporation),

    # 用于操作基础数据服务//监测数据//气象监测站点//降雨量
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/Rainfall',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_Rainfall),

    # 用于操作基础数据服务//监测数据//气象监测站点//太阳辐射
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/SolarRadiation',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_SolarRadiation),

    # 用于操作基础数据服务//监测数据//气象监测站点//云量
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/CloudCover',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_CloudCover),

    # 用于操作基础数据服务//监测数据//气象监测站点//风速风向
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WindSpeedAndDirection',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WindSpeedAndDirection),

    # 用于操作基础数据服务//监测数据/气象监测站点//水温
    path('upLoad/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature),

    path('creat/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table),

    path('update/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature_Table),

    path('publish/BasicDataService/MonitoringData/MeteorologicalMonitoringStation/WaterTemperature',
         PublicServicesViews.publish_BasicDataService_MonitoringData_MeteorologicalMonitoringStation_WaterTemperature),

    # 用于操作模型数据//MODFLOW//渗透（水力传导）
    path('upLoad/ModelData/MODFLOW/Infiltration',
         PublicServicesViews.upLoad_ModelData_MODFLOW_Infiltration),

    path('creat/ModelData/MODFLOW/Infiltration/Table',
         PublicServicesViews.creat_ModelData_MODFLOW_Infiltration_Table),

    path('update/ModelData/MODFLOW/Infiltration/Table',
         PublicServicesViews.update_ModelData_MODFLOW_Infiltration_Table),

    path('publish/ModelData/MODFLOW/Infiltration',
         PublicServicesViews.publish_ModelData_MODFLOW_Infiltration),
]
