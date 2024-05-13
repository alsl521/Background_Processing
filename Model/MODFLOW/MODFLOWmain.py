# -*- coding: gbk -*-
import os
import shutil

from Model.MODFLOW.utils import InitializeFirstModFlowWaterlevel, HandlingRCH, EFDCToMODFLOWContext, \
    GetBasicFileContext, generate_efdc_file
from Utils.execute_command import CommonProcess


def run_modflow(CurrentTime):
    NowTimeWritePath = os.getcwd() + r"\Data\Admin\Run\File\modflow\第" + str(CurrentTime) + r"应力期"
    os.makedirs(NowTimeWritePath, exist_ok=True)
    NowTimeRunPath = os.getcwd() + r"\Data\Admin\Run\run\modflow\第" + str(CurrentTime) + r"应力期"
    os.makedirs(NowTimeRunPath, exist_ok=True)
    resultPath = os.getcwd() + r"\Data\Admin\Run\result\modflow\第" + str(CurrentTime) + r"应力期"
    os.makedirs(resultPath, exist_ok=True)

    HandlingRCH(NowTimeWritePath, CurrentTime)

    if CurrentTime == 1:
        InitializeFirstModFlowWaterlevel(NowTimeWritePath, CurrentTime)

    if CurrentTime != 1:
        EFDCToMODFLOWContext(NowTimeWritePath, CurrentTime)
        GetBasicFileContext(CurrentTime)

    source_folder = NowTimeWritePath
    destination_folder = NowTimeRunPath
    # 遍历源文件夹中的所有内容
    for root, dirs, files in os.walk(source_folder):
        # 在目标文件夹中重新创建对应的目录结构
        relative_path = os.path.relpath(root, source_folder)
        destination_path = os.path.join(destination_folder, relative_path)
        os.makedirs(destination_path, exist_ok=True)

        # 复制源文件夹中的所有文件到目标文件夹
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_path, file)
            shutil.copy2(source_file, destination_file)

    # 创建一个 CommonProcess 对象
    common_process = CommonProcess()
    # 将处理函数注册到事件中
    common_process.working_directory = NowTimeRunPath
    exe_path = os.getcwd() + r"\tools\MF2005.exe"
    common_process.run(exe_path, "model.nam", "failed")
    # 等待命令执行完成
    common_process.wait()

    # 定义源文件夹和目标文件夹的路径
    source_folder = NowTimeRunPath
    destination_folder = resultPath

    # 定义要复制的文件列表
    files_to_copy = [
        'model.LST',
        'model.HDS',
        'model.DDN',
        'model.BGT',
        'SZH.TXT',
        'model.SZH'
    ]

    # 遍历文件列表，逐个复制文件
    for file_name in files_to_copy:
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.copy(source_file, destination_file)

    generate_efdc_file(CurrentTime)
