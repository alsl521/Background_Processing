import os

import numpy as np
from django.db import connection
from osgeo import gdal
import pandas as pd

from Model.EFDC.EFDCFileWrite import EFDCFileWrite
from Model.EFDC.MeteorologyFileWrite import WindFileWrite, TserFileWrite, AserFileWrite
from Model.EFDC.RunFileWrite import copy_file
from Model.EFDC.SWMMEFDC import SWMMFlow
from Model.EFDC.SpatialDiscretizationFileWrite import CellFileWrite, ShowFileWrite, LxlyFileWrite, DecompFileWrite, \
    DxdyFileWrite
from Utils.execute_command import CommonProcess


def validate_EFDC(swmmefdccol, swmmefdcrow, SWMMValue, VerLay, Isboundary):
    CurrentTime = 1
    NowTimeWritePath = os.getcwd() + r"\Data\Admin\Run\File\EFDC\第" + str(CurrentTime) + "应力期"
    os.makedirs(NowTimeWritePath, exist_ok=True)
    NowTimeRunPath = os.getcwd() + r"\Data\Admin\Run\validate\EFDC"
    os.makedirs(NowTimeRunPath, exist_ok=True)

    # 水均衡设置
    SWMMToEFDC = 0
    for i in range(len(SWMMValue)):
        SWMMToEFDC += SWMMValue[i]
    # 水下地形栅格数据读取
    gdal.AllRegister()

    filePath = os.getcwd() + r"\Data\Admin\BasicDataService\MonitoringData\RiverMonitoringStation\UnderwaterRelief\UnderwaterRelief.tif"

    dataset = gdal.Open(filePath)
    adfGeoTransform = dataset.GetGeoTransform()
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
    originX = adfGeoTransform[0]
    originY = adfGeoTransform[3]
    print(nXSize, nYSize)
    band = dataset.GetRasterBand(1)
    Underwatertopography_cell = np.zeros((nYSize + 4, nXSize + 4))
    values = []
    cols = []
    values_all = []
    max_j = 0
    for j in range(nXSize):
        for i in range(nYSize):
            col = []
            value = band.ReadAsArray(j, i, 1, 1)
            values_all.append(value)
            col.append(i)
            col.append(j)
            cols.append(col)
            if value is not None:
                value = value[0][0]
                Underwatertopography_cell[i + 2, j + 2] = value
                if value != -9999:
                    if j > max_j:
                        max_j = j
                    values.append(value)
    print(len(values))
    print(max_j)
    print(Underwatertopography_cell[2, 818])

    gongsi_conn = connection

    data = pd.read_sql("select * from public.admin_efdc_initialwaterlevel;", con=gongsi_conn)

    WaterLevel_cell = np.zeros((nYSize + 4, nXSize + 4))
    efdc_waterlevel_row = data["efdcrow"].tolist()
    efdc_waterlevel_col = data["efdccol"].tolist()
    waterlevel_value = data["efdcwater"].tolist()
    for i in range(len(efdc_waterlevel_row)):
        WaterLevel_cell[efdc_waterlevel_row[i] + 1, efdc_waterlevel_col[i] + 1] = waterlevel_value[i]
    print(WaterLevel_cell[2, 818])

    # 数据库网格数据读取
    data = pd.read_sql("select * from public.admin_efdcspatialdiscretedata;", con=gongsi_conn)
    Cell = np.zeros((nYSize + 4, nXSize + 4))
    cell_row = data["efdcrow"].tolist()
    cell_col = data["efdccol"].tolist()
    cell_value = data["isdry"].tolist()
    efdc_row_lon = data["efdcrowlon"].tolist()[0]
    efdc_col_lon = data["efdccollon"].tolist()[0]
    originX -= 2 * efdc_col_lon
    originY -= 2 * efdc_row_lon
    print(efdc_col_lon)
    IsActivite = 0
    IsHumid = 0
    for i in range(len(efdc_waterlevel_row)):
        Cell[cell_row[i] + 1, cell_col[i] + 1] = cell_value[i]
        IsActivite += 1
        if cell_value[i] == 1:
            IsHumid += 1
    print(Cell[2, 818])

    backFilePath = os.getcwd() + "\\Model\\backFile\\EFDC"

    CellFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    ShowFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    LxlyFileWrite(Cell, efdc_col_lon, efdc_row_lon, originX, originY, backpath=backFilePath,
                  runingpath=NowTimeWritePath)
    DecompFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    DxdyFileWrite(Cell, WaterLevel_cell, Underwatertopography_cell, efdc_col_lon, efdc_row_lon, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    # 时间离散设定
    TimeDiscretization = pd.read_sql("select * from admin_time_dispersion;", con=gongsi_conn)
    time_names = TimeDiscretization["name"].tolist()
    time_value = TimeDiscretization["time"].tolist()
    time_flag_output = True
    time_flag_step = True
    time_i = 0
    TimeEvery = 86400
    TimeStep = 1
    while time_i < len(time_value) and (time_flag_output or time_flag_step):
        if str(time_names[time_i]).find("efdc_calculate_step") != -1:
            TimeStep = int(str(time_value[time_i]).rstrip('s'))
            time_flag_step = False
        if str(time_names[time_i]).find("efdc_output_step") != -1:
            TimeEvery = int(str(time_value[time_i]).rstrip('s'))
            time_flag_output = False
        time_i += 1

    # 站点高度
    StationHeight = 10

    data_wind = pd.read_sql("select * from public.admin_windspeedanddirection_observation;", con=gongsi_conn)
    WindSpeed = data_wind["windspeed"].tolist()
    WindDirection = data_wind["winddirection"].tolist()

    WindFileWrite(WindSpeed, TimeEvery, StationHeight, WindDirection, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    data_watertemperature = pd.read_sql("select * from public.admin_watertemperature_observation;", con=gongsi_conn)
    WaterTemperature = data_watertemperature["watertemperature"].tolist()
    TserFileWrite(WaterTemperature, TimeEvery, VerLay, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    data_atm = pd.read_sql("select * from public.admin_atmosphericpressure_observation;", con=gongsi_conn)
    Atmosphere = data_atm["atmosphericpressure"].tolist()

    data_rain = pd.read_sql("select * from public.admin_rainfall_observation;", con=gongsi_conn)
    Rain = data_rain["rainfall"].tolist()

    data_eva = pd.read_sql("select * from public.admin_evaporation_observation;", con=gongsi_conn)
    Eva = data_eva["evaporation"].tolist()

    data_solar = pd.read_sql("select * from public.admin_solarradiation_observation;", con=gongsi_conn)
    Solar = data_solar["solarradiation"].tolist()

    data_cloud = pd.read_sql("select * from public.admin_cloudcover_observation;", con=gongsi_conn)
    Cloud = data_cloud["cloudcover"].tolist()
    AserFileWrite(TimeEvery, Atmosphere, Rain, Eva, Solar, Cloud, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    # modflow与efdc拓扑交互流量
    data_modeflowandefdc = pd.read_sql("select * from public.admin_efdcandmodflowinteractiveunit;", con=gongsi_conn)
    efdcrow = data_modeflowandefdc["efdcrow"].tolist()
    efdcrow = [i + 2 for i in efdcrow]
    efdccol = data_modeflowandefdc["efdccol"].tolist()
    efdccol = [i + 2 for i in efdccol]
    efdcmodflowIsdary = data_modeflowandefdc["isdry"].tolist()
    modlflowcol = data_modeflowandefdc["modflowcol"].tolist()
    modlflowrow = data_modeflowandefdc["modflowrow"].tolist()
    # 缺modflow的入流出流
    data_modflow = pd.read_sql("select * from public.admin_modflowspatialdiscretedata;", con=gongsi_conn)
    modflowtotalcol = np.array(data_modflow["modflowcol"])
    modflowtotalrow = np.array(data_modflow["modflowrow"])
    RiverValue = np.zeros((np.max(modflowtotalrow), np.max(modflowtotalcol)))
    # 读入河流文件 E:\Project\Background_Processing\Data\Admin\Run\Run\Result\MODFLOW\第1应力期\ModflowRiverFlow.txt
    RiverFile = open(
        os.getcwd() + r"\Data\Admin\Run\Result\MODFLOW\第" + str(
            CurrentTime) + r"应力期\ModflowRiverFlow.txt",
        "r+")
    RiverFileLists = RiverFile.readlines()
    RiverFile.close()
    for i in range(1, len(RiverFileLists)):
        line = RiverFileLists[i].split('\t')
        modflowcol = int(line[0]) - 1
        modflowrow = int(line[1]) - 1
        RiverValue[modflowrow, modflowcol] = -float(line[2])
    EFDCBoundaryValue = np.zeros((len(Cell), len(Cell[0])))
    data_boundary = pd.read_sql("select * from public.admin_flowrate;", con=gongsi_conn)
    flow_name = data_boundary["name"].tolist()
    flow_function = data_boundary["function"].tolist()
    flow_boundary_name = []
    for i in range(len(flow_function)):
        if str(flow_function[i]).find("监测点") == -1:
            flow_boundary_name.append(flow_name[i])
    data_boundaryflow = pd.read_sql("select * from public.admin_flowrate_observation;", con=gongsi_conn)
    flow_value_name = data_boundaryflow["name"].tolist()
    flow_value = data_boundaryflow["flow"].tolist()
    inflow_values = []
    i = 0
    while i < len(flow_value_name):
        k_name = 0
        while k_name < len(flow_boundary_name):
            if flow_boundary_name[k_name] == flow_value_name[i]:
                break
            k_name += 1
        if k_name < len(flow_boundary_name):
            i_index = 0
            while i < len(flow_value_name) and k_name < len(flow_boundary_name) and flow_value_name[i] == \
                    flow_boundary_name[k_name]:
                if i_index == CurrentTime - 1:
                    inflow_values.append(flow_value[i])
                i_index += 1
                i += 1
        else:
            i += 1

    inflow_value = 0
    outflow_value = 0
    for i in range(len(inflow_values)):
        if inflow_values[i] > 0:
            inflow_value += inflow_values[i]
        else:
            outflow_value += inflow_values[i]
    EFDCInflow = inflow_value
    EFDCOutflow = outflow_value

    InflowCount = int(IsHumid / 2)
    OutflowCount = IsHumid - InflowCount
    cellCount = 0
    for i in range(len(Cell)):
        for j in range(len(Cell[0])):
            if Cell[i, j] == 1:
                cellCount += 1
                if cellCount <= InflowCount:
                    EFDCBoundaryValue[i, j] = round(inflow_value / InflowCount, 3)
                else:
                    EFDCBoundaryValue[i, j] = round(outflow_value / OutflowCount, 3)
    print(efdccol)
    swmmefdccol = [i + 2 for i in swmmefdccol]
    swmmefdcrow = [i + 2 for i in swmmefdcrow]
    EFDCBoundaryValue += SWMMFlow(Cell, swmmefdccol, swmmefdcrow, EFDCBoundaryValue, SWMMValue)

    # 参数输入
    data_dissparamater = pd.read_sql("select * from public.admin_efdc_parameter_observation;", con=gongsi_conn)
    paramter = []
    paramter.append(data_dissparamater["chd"].tolist()[0])
    paramter.append(data_dissparamater["smagcoef"].tolist()[0])
    paramter.append(data_dissparamater["backvisc"].tolist()[0])
    paramter.append(data_dissparamater["maxlamvisc"].tolist()[0])
    paramter.append(data_dissparamater["maxturbdiffcoef"].tolist()[0])
    paramter.append(data_dissparamater["rough"].tolist()[0])

    ModflowToEFDC, EFDCToModflow = EFDCFileWrite(paramter, Cell, RiverValue, modlflowcol, modlflowrow, efdccol, efdcrow,
                                                 EFDCBoundaryValue, VerLay, IsActivite,
                                                 IsHumid, Isboundary, TimeEvery, TimeStep, CurrentTime,
                                                 backpath=backFilePath, runingpath=NowTimeWritePath)

    copy_file(source_path=NowTimeWritePath + "\\cell.inp",
              destination_path=NowTimeWritePath + "\\celllt.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.jnp",
              destination_path=NowTimeWritePath + "\\decomp.inp")

    # 运行文件写入
    copy_file(source_path=NowTimeWritePath + "\\cell.inp",
              destination_path=NowTimeRunPath + "\\cell.inp")
    copy_file(source_path=NowTimeWritePath + "\\celllt.inp",
              destination_path=NowTimeRunPath + "\\celllt.inp")
    copy_file(source_path=NowTimeWritePath + "\\aser.inp",
              destination_path=NowTimeRunPath + "\\aser.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.inp",
              destination_path=NowTimeRunPath + "\\decomp.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.jnp",
              destination_path=NowTimeRunPath + "\\decomp.jnp")
    copy_file(source_path=NowTimeWritePath + "\\dxdy.inp",
              destination_path=NowTimeRunPath + "\\dxdy.inp")
    copy_file(source_path=NowTimeWritePath + "\\efdc.inp",
              destination_path=NowTimeRunPath + "\\efdc.inp")
    copy_file(source_path=NowTimeWritePath + "\\lxly.inp",
              destination_path=NowTimeRunPath + "\\lxly.inp")
    copy_file(source_path=NowTimeWritePath + "\\show.inp",
              destination_path=NowTimeRunPath + "\\show.inp")
    copy_file(source_path=NowTimeWritePath + "\\tser.inp",
              destination_path=NowTimeRunPath + "\\tser.inp")
    copy_file(source_path=NowTimeWritePath + "\\wser.inp",
              destination_path=NowTimeRunPath + "\\wser.inp")

    file_list = []
    for root, dirs, files in os.walk(NowTimeRunPath):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_name = os.path.basename(file_path)  # 提取文件名
            file_extension = os.path.splitext(file_name)[1]  # 提取文件扩展名
            file_list.append(file_name)

    return file_list


def EFDCRUN(swmmefdccol, swmmefdcrow, SWMMValue, VerLay, Isboundary, CurrentTime):
    NowTimeWritePath = os.getcwd() + r"\Data\Admin\Run\File\EFDC\第" + str(CurrentTime) + "应力期"
    os.makedirs(NowTimeWritePath, exist_ok=True)
    NowTimeRunPath = os.getcwd() + r"\Data\Admin\Run\run\EFDC\第" + str(CurrentTime) + "应力期"
    os.makedirs(NowTimeRunPath, exist_ok=True)
    resultPath = os.getcwd() + r"\Data\Admin\Run\result\EFDC\第" + str(CurrentTime) + "应力期"
    os.makedirs(resultPath, exist_ok=True)

    if CurrentTime > 1:
        restart_flag = False
        RestartFileFilePath = ""
        RestartFileDirFilePath = os.getcwd() + r"\Data\Admin\Run\Run\EFDC\第" + str(CurrentTime - 1) + r"应力期\#output"
        for file in os.listdir(RestartFileDirFilePath):
            if file.find("RESTART") != -1:
                RestartFileFilePath = os.path.join(RestartFileDirFilePath, file)
        restart_flag = True
        if restart_flag:
            copy_file(source_path=RestartFileFilePath, destination_path=NowTimeWritePath + "\\restart.inp")
            copy_file(source_path=RestartFileFilePath, destination_path=NowTimeRunPath + "\\restart.inp")
        else:
            print("缺少热启动文件！")

    # 水均衡设置
    SWMMToEFDC = 0
    for i in range(len(SWMMValue)):
        SWMMToEFDC += SWMMValue[i]
    # 水下地形栅格数据读取
    gdal.AllRegister()

    filePath = os.getcwd() + r"\Data\Admin\BasicDataService\MonitoringData\RiverMonitoringStation\UnderwaterRelief\UnderwaterRelief.tif"

    dataset = gdal.Open(filePath)
    adfGeoTransform = dataset.GetGeoTransform()
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
    originX = adfGeoTransform[0]
    originY = adfGeoTransform[3]
    print(nXSize, nYSize)
    band = dataset.GetRasterBand(1)
    Underwatertopography_cell = np.zeros((nYSize + 4, nXSize + 4))
    values = []
    cols = []
    values_all = []
    max_j = 0
    for j in range(nXSize):
        for i in range(nYSize):
            col = []
            value = band.ReadAsArray(j, i, 1, 1)
            values_all.append(value)
            col.append(i)
            col.append(j)
            cols.append(col)
            if value is not None:
                value = value[0][0]
                Underwatertopography_cell[i + 2, j + 2] = value
                if value != -9999:
                    if j > max_j:
                        max_j = j
                    values.append(value)
    print(len(values))
    print(max_j)
    print(Underwatertopography_cell[2, 818])

    gongsi_conn = connection

    data = pd.read_sql("select * from public.admin_efdc_initialwaterlevel;", con=gongsi_conn)

    WaterLevel_cell = np.zeros((nYSize + 4, nXSize + 4))
    efdc_waterlevel_row = data["efdcrow"].tolist()
    efdc_waterlevel_col = data["efdccol"].tolist()
    waterlevel_value = data["efdcwater"].tolist()
    for i in range(len(efdc_waterlevel_row)):
        WaterLevel_cell[efdc_waterlevel_row[i] + 1, efdc_waterlevel_col[i] + 1] = waterlevel_value[i]
    print(WaterLevel_cell[2, 818])

    # 数据库网格数据读取
    data = pd.read_sql("select * from public.admin_efdcspatialdiscretedata;", con=gongsi_conn)
    Cell = np.zeros((nYSize + 4, nXSize + 4))
    cell_row = data["efdcrow"].tolist()
    cell_col = data["efdccol"].tolist()
    cell_value = data["isdry"].tolist()
    efdc_row_lon = data["efdcrowlon"].tolist()[0]
    efdc_col_lon = data["efdccollon"].tolist()[0]
    originX -= 2 * efdc_col_lon
    originY -= 2 * efdc_row_lon
    print(efdc_col_lon)
    IsActivite = 0
    IsHumid = 0
    for i in range(len(efdc_waterlevel_row)):
        Cell[cell_row[i] + 1, cell_col[i] + 1] = cell_value[i]
        IsActivite += 1
        if cell_value[i] == 1:
            IsHumid += 1
    print(Cell[2, 818])

    backFilePath = os.getcwd() + "\\Model\\backFile\\EFDC"

    CellFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    ShowFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    LxlyFileWrite(Cell, efdc_col_lon, efdc_row_lon, originX, originY, backpath=backFilePath,
                  runingpath=NowTimeWritePath)
    DecompFileWrite(Cell, backpath=backFilePath, runingpath=NowTimeWritePath)
    DxdyFileWrite(Cell, WaterLevel_cell, Underwatertopography_cell, efdc_col_lon, efdc_row_lon, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    # 时间离散设定
    TimeDiscretization = pd.read_sql("select * from admin_time_dispersion;", con=gongsi_conn)
    time_names = TimeDiscretization["name"].tolist()
    time_value = TimeDiscretization["time"].tolist()
    time_flag_output = True
    time_flag_step = True
    time_i = 0
    TimeEvery = 86400
    TimeStep = 1
    while time_i < len(time_value) and (time_flag_output or time_flag_step):
        if str(time_names[time_i]).find("efdc_calculate_step") != -1:
            TimeStep = int(str(time_value[time_i]).rstrip('s'))
            time_flag_step = False
        if str(time_names[time_i]).find("efdc_output_step") != -1:
            TimeEvery = int(str(time_value[time_i]).rstrip('s'))
            time_flag_output = False
        time_i += 1

    # 站点高度
    StationHeight = 10

    data_wind = pd.read_sql("select * from public.admin_windspeedanddirection_observation;", con=gongsi_conn)
    WindSpeed = data_wind["windspeed"].tolist()
    WindDirection = data_wind["winddirection"].tolist()

    WindFileWrite(WindSpeed, TimeEvery, StationHeight, WindDirection, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    data_watertemperature = pd.read_sql("select * from public.admin_watertemperature_observation;", con=gongsi_conn)
    WaterTemperature = data_watertemperature["watertemperature"].tolist()
    TserFileWrite(WaterTemperature, TimeEvery, VerLay, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    data_atm = pd.read_sql("select * from public.admin_atmosphericpressure_observation;", con=gongsi_conn)
    Atmosphere = data_atm["atmosphericpressure"].tolist()

    data_rain = pd.read_sql("select * from public.admin_rainfall_observation;", con=gongsi_conn)
    Rain = data_rain["rainfall"].tolist()

    data_eva = pd.read_sql("select * from public.admin_evaporation_observation;", con=gongsi_conn)
    Eva = data_eva["evaporation"].tolist()

    data_solar = pd.read_sql("select * from public.admin_solarradiation_observation;", con=gongsi_conn)
    Solar = data_solar["solarradiation"].tolist()

    data_cloud = pd.read_sql("select * from public.admin_cloudcover_observation;", con=gongsi_conn)
    Cloud = data_cloud["cloudcover"].tolist()
    AserFileWrite(TimeEvery, Atmosphere, Rain, Eva, Solar, Cloud, backpath=backFilePath,
                  runingpath=NowTimeWritePath)

    # modflow与efdc拓扑交互流量
    data_modeflowandefdc = pd.read_sql("select * from public.admin_efdcandmodflowinteractiveunit;", con=gongsi_conn)
    efdcrow = data_modeflowandefdc["efdcrow"].tolist()
    efdcrow = [i + 2 for i in efdcrow]
    efdccol = data_modeflowandefdc["efdccol"].tolist()
    efdccol = [i + 2 for i in efdccol]
    efdcmodflowIsdary = data_modeflowandefdc["isdry"].tolist()
    modlflowcol = data_modeflowandefdc["modflowcol"].tolist()
    modlflowrow = data_modeflowandefdc["modflowrow"].tolist()
    # 缺modflow的入流出流
    data_modflow = pd.read_sql("select * from public.admin_modflowspatialdiscretedata;", con=gongsi_conn)
    modflowtotalcol = np.array(data_modflow["modflowcol"])
    modflowtotalrow = np.array(data_modflow["modflowrow"])
    RiverValue = np.zeros((np.max(modflowtotalrow), np.max(modflowtotalcol)))
    # 读入河流文件 E:\Project\Background_Processing\Data\Admin\Run\Run\Result\MODFLOW\第1应力期\ModflowRiverFlow.txt
    RiverFile = open(
        os.getcwd() + r"\Data\Admin\Run\Result\MODFLOW\第" + str(
            CurrentTime) + r"应力期\ModflowRiverFlow.txt",
        "r+")
    RiverFileLists = RiverFile.readlines()
    RiverFile.close()
    for i in range(1, len(RiverFileLists)):
        line = RiverFileLists[i].split('\t')
        modflowcol = int(line[0]) - 1
        modflowrow = int(line[1]) - 1
        RiverValue[modflowrow, modflowcol] = -float(line[2])
    EFDCBoundaryValue = np.zeros((len(Cell), len(Cell[0])))
    data_boundary = pd.read_sql("select * from public.admin_flowrate;", con=gongsi_conn)
    flow_name = data_boundary["name"].tolist()
    flow_function = data_boundary["function"].tolist()
    flow_boundary_name = []
    for i in range(len(flow_function)):
        if str(flow_function[i]).find("监测点") == -1:
            flow_boundary_name.append(flow_name[i])
    data_boundaryflow = pd.read_sql("select * from public.admin_flowrate_observation;", con=gongsi_conn)
    flow_value_name = data_boundaryflow["name"].tolist()
    flow_value = data_boundaryflow["flow"].tolist()
    inflow_values = []
    i = 0
    while i < len(flow_value_name):
        k_name = 0
        while k_name < len(flow_boundary_name):
            if flow_boundary_name[k_name] == flow_value_name[i]:
                break
            k_name += 1
        if k_name < len(flow_boundary_name):
            i_index = 0
            while i < len(flow_value_name) and k_name < len(flow_boundary_name) and flow_value_name[i] == \
                    flow_boundary_name[k_name]:
                if i_index == CurrentTime - 1:
                    inflow_values.append(flow_value[i])
                i_index += 1
                i += 1
        else:
            i += 1

    inflow_value = 0
    outflow_value = 0
    for i in range(len(inflow_values)):
        if inflow_values[i] > 0:
            inflow_value += inflow_values[i]
        else:
            outflow_value += inflow_values[i]
    EFDCInflow = inflow_value
    EFDCOutflow = outflow_value

    InflowCount = int(IsHumid / 2)
    OutflowCount = IsHumid - InflowCount
    cellCount = 0
    for i in range(len(Cell)):
        for j in range(len(Cell[0])):
            if Cell[i, j] == 1:
                cellCount += 1
                if cellCount <= InflowCount:
                    EFDCBoundaryValue[i, j] = round(inflow_value / InflowCount, 3)
                else:
                    EFDCBoundaryValue[i, j] = round(outflow_value / OutflowCount, 3)
    print(efdccol)
    swmmefdccol = [i + 2 for i in swmmefdccol]
    swmmefdcrow = [i + 2 for i in swmmefdcrow]
    EFDCBoundaryValue += SWMMFlow(Cell, swmmefdccol, swmmefdcrow, EFDCBoundaryValue, SWMMValue)

    # 参数输入
    data_dissparamater = pd.read_sql("select * from public.admin_efdc_parameter_observation;", con=gongsi_conn)
    paramter = []
    paramter.append(data_dissparamater["chd"].tolist()[0])
    paramter.append(data_dissparamater["smagcoef"].tolist()[0])
    paramter.append(data_dissparamater["backvisc"].tolist()[0])
    paramter.append(data_dissparamater["maxlamvisc"].tolist()[0])
    paramter.append(data_dissparamater["maxturbdiffcoef"].tolist()[0])
    paramter.append(data_dissparamater["rough"].tolist()[0])

    ModflowToEFDC, EFDCToModflow = EFDCFileWrite(paramter, Cell, RiverValue, modlflowcol, modlflowrow, efdccol, efdcrow,
                                                 EFDCBoundaryValue, VerLay, IsActivite,
                                                 IsHumid, Isboundary, TimeEvery, TimeStep, CurrentTime,
                                                 backpath=backFilePath, runingpath=NowTimeWritePath)

    copy_file(source_path=NowTimeWritePath + "\\cell.inp",
              destination_path=NowTimeWritePath + "\\celllt.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.jnp",
              destination_path=NowTimeWritePath + "\\decomp.inp")

    # 运行文件写入
    copy_file(source_path=NowTimeWritePath + "\\cell.inp",
              destination_path=NowTimeRunPath + "\\cell.inp")
    copy_file(source_path=NowTimeWritePath + "\\celllt.inp",
              destination_path=NowTimeRunPath + "\\celllt.inp")
    copy_file(source_path=NowTimeWritePath + "\\aser.inp",
              destination_path=NowTimeRunPath + "\\aser.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.inp",
              destination_path=NowTimeRunPath + "\\decomp.inp")
    copy_file(source_path=NowTimeWritePath + "\\decomp.jnp",
              destination_path=NowTimeRunPath + "\\decomp.jnp")
    copy_file(source_path=NowTimeWritePath + "\\dxdy.inp",
              destination_path=NowTimeRunPath + "\\dxdy.inp")
    copy_file(source_path=NowTimeWritePath + "\\efdc.inp",
              destination_path=NowTimeRunPath + "\\efdc.inp")
    copy_file(source_path=NowTimeWritePath + "\\lxly.inp",
              destination_path=NowTimeRunPath + "\\lxly.inp")
    copy_file(source_path=NowTimeWritePath + "\\show.inp",
              destination_path=NowTimeRunPath + "\\show.inp")
    copy_file(source_path=NowTimeWritePath + "\\tser.inp",
              destination_path=NowTimeRunPath + "\\tser.inp")
    copy_file(source_path=NowTimeWritePath + "\\wser.inp",
              destination_path=NowTimeRunPath + "\\wser.inp")

    # 创建一个 CommonProcess 对象
    common_process = CommonProcess()
    # 将处理函数注册到事件中
    common_process.working_directory = NowTimeRunPath
    exe_path = os.getcwd() + r"\tools\EFDCPlus_MPI_10.4.0.exe"
    common_process.run(exe_path, None, "Unknown")
    # 等待命令执行完成
    common_process.wait()

    Bal2tFile = open(NowTimeRunPath + "\\#output\BAL2T.OUT", "r+")
    Bal2tFileLists = Bal2tFile.readlines()
    Bal2tFile.close()
    BalanceFile = open(NowTimeRunPath + "\\balance.txt", "w+")
    k = 0
    evaporate = 0
    total_out = 0
    evaporate = 0
    total_out = 0
    while k < len(Bal2tFileLists):
        if str(Bal2tFileLists[k]).find("TOTAL OUT   (OUT)") != -1:
            value_string = str(Bal2tFileLists[k])[18:37].strip()
            j = value_string.find('E')
            if j != -1:
                total_out = float(value_string[:j]) * 10 ** int(value_string[j + 1:])
            else:
                total_out = float(value_string)
            evaporate = total_out + EFDCInflow * TimeEvery + ModflowToEFDC * TimeEvery + EFDCToModflow * TimeEvery + EFDCOutflow * TimeEvery + SWMMToEFDC * TimeEvery
            break
        k += 1
    BalanceFile.write("上游及各支流入流流量      " + str(EFDCInflow * TimeEvery) + "\n")
    BalanceFile.write("下游出流流量：      " + str(EFDCOutflow * TimeEvery) + "\n")
    BalanceFile.write("MODFLOW补给EFDC流量      " + str(ModflowToEFDC * TimeEvery) + "\n")
    BalanceFile.write("EFDC下渗给MODFLOW流量      " + str(EFDCToModflow * TimeEvery) + "\n")
    BalanceFile.write("SWMM补给EFDC流量      " + str(SWMMToEFDC * TimeEvery) + "\n")
    BalanceFile.write("气候值（降雨量与蒸发量）：      " + str(-evaporate) + "\n")
    BalanceFile.write("总储水量（出水量）：      " + str(-total_out) + "\n")
    BalanceFile.close()
