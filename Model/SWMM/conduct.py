import os
import shutil

from Model.SWMM import SWMM_table, SWMM_shp, SWMM_time, SWMM_wether, hotstart
from Model.SWMM.hotstart import write_hotstart, writedate
from Utils.execute_command import CommonProcess


def validate_SWMM(routing_step, dry_step_key, wet_step_key):
    if not os.path.exists(os.getcwd() + '\\data\\admin\\run\\validate\\SWMM'):
        os.makedirs(os.getcwd() + '\\data\\admin\\run\\validate\\SWMM')

    targetFilePathtxt = os.getcwd() + '\\data\\admin\\run\\validate\\SWMM\\control.inp'

    backupFilePathtxt = os.getcwd() + '\\Model\\backFile\\SWMM\\control.txt'
    shutil.copy(backupFilePathtxt, targetFilePathtxt)

    # 写入节点和子汇水区的参数文件
    SWMM_table.write_subcatchments(targetFilePathtxt)
    SWMM_table.write_junction(targetFilePathtxt)
    SWMM_table.write_raingage(targetFilePathtxt)
    SWMM_table.write_subareas(targetFilePathtxt)
    # # 写入shp文件
    SWMM_shp.write_raingageshp(targetFilePathtxt)
    # # SWMM_shp.write_subshp(filename)
    SWMM_shp.write_junctionshp(targetFilePathtxt)

    SWMM_time.write_routing_step(targetFilePathtxt, routing_step)
    SWMM_time.write_dry_step(targetFilePathtxt, dry_step_key)
    SWMM_time.write_wet_step(targetFilePathtxt, wet_step_key)

    # 写入气候文件
    SWMM_wether.create_tem(1)
    SWMM_wether.create_rain(1)
    tem_file_name = os.getcwd() + '\\data\\admin\\run\\validate\\SWMM\\tem.dat'
    rain_file_name = os.getcwd() + '\\data\\admin\\run\\validate\\SWMM\\Grain.dat'

    shutil.copy(os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\tem.dat', tem_file_name)
    shutil.copy(os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\Grain.dat', rain_file_name)

    SWMM_wether.write_rain(targetFilePathtxt, rain_file_name)
    SWMM_wether.write_tem(targetFilePathtxt, tem_file_name)

    # 运行热启动文件，并将结果保存到新的文件夹中
    write_hotstart(0, targetFilePathtxt)

    file_list = []
    for root, dirs, files in os.walk(os.getcwd() + '\\data\\admin\\run\\validate\\SWMM'):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_name = os.path.basename(file_path)  # 提取文件名
            file_list.append(file_name)

    return file_list


# 启动外部可执行文件
def Execute_SWMM(CurrentTime, routing_step, dry_step_key, wet_step_key):
    if not os.path.exists(os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(CurrentTime)):
        os.makedirs(os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(CurrentTime))

    if not os.path.exists(os.getcwd() + '\\data\\admin\\run\\run\\SWMM'):
        os.makedirs(os.getcwd() + '\\data\\admin\\run\\run\\SWMM')

    targetFilePathtxt = os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(CurrentTime) + '\\control.txt'

    if CurrentTime == 1:
        backupFilePathtxt = os.getcwd() + '\\Model\\backFile\\SWMM\\control.txt'
        shutil.copy(backupFilePathtxt, targetFilePathtxt)
    else:
        backupFilePathtxt = os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(CurrentTime - 1) + '\\control.txt'
        shutil.copy(backupFilePathtxt, targetFilePathtxt)

    # 写入节点和子汇水区的参数文件
    SWMM_table.write_subcatchments(targetFilePathtxt)
    SWMM_table.write_junction(targetFilePathtxt)
    SWMM_table.write_raingage(targetFilePathtxt)
    SWMM_table.write_subareas(targetFilePathtxt)
    # # 写入shp文件
    SWMM_shp.write_raingageshp(targetFilePathtxt)
    # # SWMM_shp.write_subshp(filename)
    SWMM_shp.write_junctionshp(targetFilePathtxt)

    SWMM_time.write_routing_step(targetFilePathtxt, routing_step)
    SWMM_time.write_dry_step(targetFilePathtxt, dry_step_key)
    SWMM_time.write_wet_step(targetFilePathtxt, wet_step_key)

    # 写入气候文件
    SWMM_wether.create_tem(CurrentTime)
    SWMM_wether.create_rain(CurrentTime)
    tem_file_name = os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\tem.dat'
    rain_file_name = os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\Grain.dat'
    SWMM_wether.write_rain(targetFilePathtxt, rain_file_name)
    SWMM_wether.write_tem(targetFilePathtxt, tem_file_name)

    # 运行热启动文件，并将结果保存到新的文件夹中
    write_hotstart(CurrentTime - 1, targetFilePathtxt)

    shutil.copy(targetFilePathtxt, os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\control.inp')

    # 创建一个 CommonProcess 对象
    common_process = CommonProcess()
    # 将处理函数注册到事件中
    common_process.working_directory = os.getcwd() + '\\data\\admin\\run\\run\\SWMM'
    exe_path = os.getcwd() + r"\tools\SWMM1.exe"
    common_process.run(exe_path, None, "errors")
    # 等待命令执行完成
    common_process.wait()

    writedate(targetFilePathtxt)
