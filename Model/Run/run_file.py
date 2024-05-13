import itertools
import os
from datetime import datetime
from django.db import connection

from Model.EFDC.EFDCMain import EFDCRUN, validate_EFDC
from Model.MODFLOW.MODFLOWmain import run_modflow
from Model.SWMM.conduct import Execute_SWMM, validate_SWMM
from Utils.CopyFiles import copy_swmm_result_files, copy_efdc_result_files


def validate_data():
    table_name = "admin_" + "time_dispersion"
    sql = "SELECT time from {} where name = 'total_start_time'".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    total_start_time = datetime.strptime(cursor.fetchone()[0], date_format)

    sql = "SELECT time from {} where name = 'total_end_time'".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    total_end_time = datetime.strptime(cursor.fetchone()[0], date_format)
    delta = total_end_time - total_start_time
    days_diff = delta.days + 1

    # # # # 写入时间离散文件
    table_name = "admin_" + "time_dispersion"
    sql = "SELECT * from {}".format(table_name)

    cursor.execute(sql)

    result = cursor.fetchall()
    wet_step_key, dry_step_key, routing_step = "", "", ""
    for row in result:
        if row[1] == 'swmm_wet':
            wet_step_key = str(row[2])
        elif row[1] == 'swmm_dry':
            dry_step_key = str(row[2])
        elif row[1] == 'swmm_calculate':
            routing_step = str(row[2])

    # 需要新加的参数
    # 垂向分层
    VerLay = 1
    # 目前的时间
    CurrentTime = 1
    # 水位边界或流量边界
    Isboundary = 1

    # SWMM与EFDC交互的点位
    swmmefdccol = [565]
    swmmefdcrow = [79]
    SWMMValue = [5]

    swmm_files = validate_SWMM(routing_step, dry_step_key, wet_step_key)
    swmm_files = convert_swmm_to_chinese(swmm_files)
    # modflow与efdc交互以文件的形式写入：File下的ModflowRiverFlow.txt
    efdc_files = validate_EFDC(swmmefdccol, swmmefdcrow, SWMMValue, VerLay, Isboundary)
    efdc_files = convert_efdc_to_chinese(efdc_files)

    modflow = convert_modflow_to_chinese(
        ['model.bas6', 'model.bcf6', 'model.dis', 'model.nam', 'model.oc', 'model.PCG', 'model.rch', 'model.riv'])

    table_data = [
        {'swmm': swmm_file, 'modflow': modflow, 'efdc': efdc_file}
        for swmm_file, modflow, efdc_file in itertools.zip_longest(swmm_files, modflow, efdc_files)
    ]

    return table_data


def convert_modflow_to_chinese(file_names):
    english_to_chinese = {
        'model.bas6': '基础文件',
        'model.dis': '离散文件',
        'model.chd': '水位边界',
        'model.fhb': '流量边界',
        'model.ghb': '混合边界',
        'model.riv': '河流',
        'model.drn': '排水沟渠',
        'model.wel': '开采井',
        'model.rch': '降雨',
        'model.evt': '蒸发',
        'model.bcf6': '层物理参数',
        'model.PCG': '求解参数',
        'model.nam': '文件名称',
        'model.lpf': '单元物理参数',
        'HobFile': '监测数据',
        'model.oc': '输出控制',
        'model.hfb': '地下构筑物场景',
        'model.ibs': '地面沉降场景(IBS)',
        'model.sub': '地面沉降场景(SUB)'
    }

    chinese_names = [english_to_chinese.get(file_name, file_name) for file_name in file_names]
    return chinese_names


def convert_efdc_to_chinese(file_names):
    print(file_names)
    required_files = ['decomp.jnp', 'decomp.inp', 'cell.inp', 'celllt.inp', 'dxdy.inp', 'lxly.inp', 'show.inp']
    results = []

    if all(file_name in file_names for file_name in required_files):
        results.append('空间离散')
    if 'efdc.inp' in file_names:
        results.append('物理参数')
    if 'wser.inp' in file_names:
        results.append('风力条件')
    if 'aser.inp' in file_names:
        results.append('气候条件')

    return results


def convert_swmm_to_chinese(file_names):
    english_to_chinese = {
        'control.inp': ['空间离散数据', '物理参数数据'],
        'tem.dat': '气候气象数据',
        'Grain.dat': '气候气象数据'
    }

    chinese_names = []

    if 'control.inp' in file_names:
        chinese_names.extend(english_to_chinese.get('control.inp'))
    else:
        chinese_names.extend(['空间离散数据', '物理参数数据'])

    if any(file_name in file_names for file_name in ['tem.dat', 'Grain.dat']):
        chinese_names.append(english_to_chinese.get('tem.dat'))
    else:
        chinese_names.append('气候气象数据')

    return chinese_names


def run_swmm_modflow_efdc_model():
    table_name = "admin_" + "time_dispersion"
    sql = "SELECT time from {} where name = 'total_start_time'".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    total_start_time = datetime.strptime(cursor.fetchone()[0], date_format)

    sql = "SELECT time from {} where name = 'total_end_time'".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    total_end_time = datetime.strptime(cursor.fetchone()[0], date_format)
    delta = total_end_time - total_start_time
    days_diff = delta.days + 1

    # 写入时间离散文件
    table_name = "admin_" + "time_dispersion"
    sql = "SELECT * from {}".format(table_name)

    cursor.execute(sql)

    result = cursor.fetchall()
    wet_step_key, dry_step_key, routing_step = "", "", ""
    for row in result:
        if row[1] == 'swmm_wet':
            wet_step_key = str(row[2])
        elif row[1] == 'swmm_dry':
            dry_step_key = str(row[2])
        elif row[1] == 'swmm_calculate':
            routing_step = str(row[2])

    for i in range(1, days_diff + 1):
        # 目前的时间
        CurrentTime = i

        Execute_SWMM(CurrentTime, routing_step, dry_step_key, wet_step_key)

        source_folder = os.getcwd() + '\\data\\admin\\run\\run\\SWMM'
        destination_folder = os.getcwd() + r"\Data\Admin\Run\Result\SWMM\第" + str(CurrentTime) + "应力期"
        os.makedirs(destination_folder, exist_ok=True)
        copy_swmm_result_files(source_folder, destination_folder)

        # 需要新加的参数
        # 垂向分层
        VerLay = 1
        # 水位边界或流量边界
        Isboundary = 1
        # SWMM与EFDC交互的点位
        swmmefdccol, swmmefdcrow, SWMMValue = swmm_to_efdc(CurrentTime)

        run_modflow(CurrentTime)

        # modflow与efdc交互以文件的形式写入：File下的ModflowRiverFlow.txt
        EFDCRUN(swmmefdccol, swmmefdcrow, SWMMValue, VerLay, Isboundary, CurrentTime)
        source_folder = os.getcwd() + r"\Data\Admin\Run\run\EFDC\第" + str(CurrentTime) + r"应力期\#output"
        destination_folder = os.getcwd() + r"\Data\Admin\Run\Result\EFDC\第" + str(CurrentTime) + "应力期"
        os.makedirs(destination_folder, exist_ok=True)
        copy_efdc_result_files(source_folder, destination_folder)


def swmm_to_efdc(CurrentTime):
    table_name = "admin_hru_observation"
    sql = "SELECT * from {} ".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    hru_observation = cursor.fetchall()

    table_name = "admin_swmmandefdcinteractiveunit"
    sql = "SELECT * from {}".format(table_name)

    cursor = connection.cursor()
    cursor.execute(sql)

    swmm_efdc_interactive_unit_observation = cursor.fetchall()

    topoly = []

    for hru in hru_observation:
        for swmm in swmm_efdc_interactive_unit_observation:
            if swmm[1] == hru[8]:
                data = {
                    'hru': hru[1],
                    'junction': swmm[1],
                    'efdcrow': swmm[2],
                    'efdccol': swmm[3],
                }

                topoly.append(data)

    # 打开文件
    file = open(os.getcwd() + r"\Data\Admin\Run\Result\SWMM\第" + str(CurrentTime) + r"应力期\test1.rep",
                'r')  # 'r'表示以只读模式打开文件

    # 读取文件内容
    content = file.read()
    lines = content.splitlines()
    swmmefdccol = []
    swmmefdcrow = []
    SWMMValue = []
    for index in range(len(lines)):
        if "Subcatchment Runoff Summary" in lines[index]:
            index = index + 8
            for indexNew in range(len(hru_observation)):
                lineArray = [item for item in lines[index + indexNew].split(" ") if item != '']
                for item in topoly:
                    if item["hru"] == lineArray[0]:
                        swmmefdccol.append(item["efdccol"])
                        swmmefdcrow.append(item["efdcrow"])
                        SWMMValue.append(float(lineArray[8]) * 1000 / 86400)

            break
    # 关闭文件
    file.close()
    return swmmefdccol, swmmefdcrow, SWMMValue
