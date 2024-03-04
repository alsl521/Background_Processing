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

    path('UpLoadFiles/BasicDataService/BasicGeographicData/StudyAreaScope',
         PublicServicesViews.upLoad_BasicDataService_BasicGeographicData_StudyAreaScope),

    path('creat/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
         PublicServicesViews.creat_BasicDataService_BasicGeographicData_StudyAreaScope_Table),

    path('update/BasicDataService/BasicGeographicData/StudyAreaScope/Table',
         PublicServicesViews.update_BasicDataService_BasicGeographicData_StudyAreaScope_Table),

    path('publish/BasicDataService/BasicGeographicData/StudyAreaScope',
         PublicServicesViews.publish_BasicDataService_BasicGeographicData_StudyAreaScope),

    path('upLoad/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
         PublicServicesViews.upLoad_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),

    path('creat/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
         PublicServicesViews.creat_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),

    path('update/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate/Table',
         PublicServicesViews.update_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate_Table),

    path('publish/BasicDataService/MonitoringData/RiverMonitoringStation/FlowRate',
         PublicServicesViews.publish_BasicDataService_MonitoringData_RiverMonitoringStation_FlowRate),
]
