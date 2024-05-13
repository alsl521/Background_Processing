# -*- coding: gbk -*-
import os
import shutil

from Model.MODFLOW.utils import InitializeFirstModFlowWaterlevel, HandlingRCH, EFDCToMODFLOWContext, \
    GetBasicFileContext, generate_efdc_file
from Utils.execute_command import CommonProcess


def run_modflow(CurrentTime):
    NowTimeWritePath = os.getcwd() + r"\Data\Admin\Run\File\modflow\��" + str(CurrentTime) + r"Ӧ����"
    os.makedirs(NowTimeWritePath, exist_ok=True)
    NowTimeRunPath = os.getcwd() + r"\Data\Admin\Run\run\modflow\��" + str(CurrentTime) + r"Ӧ����"
    os.makedirs(NowTimeRunPath, exist_ok=True)
    resultPath = os.getcwd() + r"\Data\Admin\Run\result\modflow\��" + str(CurrentTime) + r"Ӧ����"
    os.makedirs(resultPath, exist_ok=True)

    HandlingRCH(NowTimeWritePath, CurrentTime)

    if CurrentTime == 1:
        InitializeFirstModFlowWaterlevel(NowTimeWritePath, CurrentTime)

    if CurrentTime != 1:
        EFDCToMODFLOWContext(NowTimeWritePath, CurrentTime)
        GetBasicFileContext(CurrentTime)

    source_folder = NowTimeWritePath
    destination_folder = NowTimeRunPath
    # ����Դ�ļ����е���������
    for root, dirs, files in os.walk(source_folder):
        # ��Ŀ���ļ��������´�����Ӧ��Ŀ¼�ṹ
        relative_path = os.path.relpath(root, source_folder)
        destination_path = os.path.join(destination_folder, relative_path)
        os.makedirs(destination_path, exist_ok=True)

        # ����Դ�ļ����е������ļ���Ŀ���ļ���
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_path, file)
            shutil.copy2(source_file, destination_file)

    # ����һ�� CommonProcess ����
    common_process = CommonProcess()
    # ��������ע�ᵽ�¼���
    common_process.working_directory = NowTimeRunPath
    exe_path = os.getcwd() + r"\tools\MF2005.exe"
    common_process.run(exe_path, "model.nam", "failed")
    # �ȴ�����ִ�����
    common_process.wait()

    # ����Դ�ļ��к�Ŀ���ļ��е�·��
    source_folder = NowTimeRunPath
    destination_folder = resultPath

    # ����Ҫ���Ƶ��ļ��б�
    files_to_copy = [
        'model.LST',
        'model.HDS',
        'model.DDN',
        'model.BGT',
        'SZH.TXT',
        'model.SZH'
    ]

    # �����ļ��б���������ļ�
    for file_name in files_to_copy:
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.copy(source_file, destination_file)

    generate_efdc_file(CurrentTime)
