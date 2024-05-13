import os
import shutil
from datetime import datetime, timedelta

file_key = 'FILES'
end_key = '['


# 写热启动
def write_hotstart(i, filename):
    if i == 0:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(filename, 'w', encoding='utf-8') as file:
            delete_lines = False
            for line in lines:
                if file_key in line:
                    delete_lines = True
                    file.write(line)
                    file.write('SAVE HOTSTART test_save.hst\n')
                    continue
                if end_key in line and delete_lines:
                    delete_lines = False
                    file.write('\n')
                    # 写入 end_key 行
                    file.write(line)
                    continue
                if not delete_lines:
                    file.write(line)
    else:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(filename, 'w', encoding='utf-8') as file:
            delete_lines = False
            for line in lines:
                if file_key in line:
                    delete_lines = True
                    file.write(line)
                    file.write('USE HOTSTART test_save.hst\nSAVE HOTSTART test_save.hst\n')
                    continue
                if end_key in line and delete_lines:
                    delete_lines = False
                    file.write('\n')
                    # 写入 end_key 行
                    file.write(line)
                    continue
                if not delete_lines:
                    file.write(line)


# 写开始运算日期和结束运算日期（以天为单位）
def writedate(filename):
    starttime_key = 'START_DATE'

    endtime_key = 'END_DATE'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if 'REPORT_START_DATE' in line:
                delete_lines = True
                data_list = line.split()
                # 获取日期部分并转换为日期格式
                date_string = data_list[1]
                date = datetime.strptime(date_string, "%m/%d/%Y")
                next_day = date + timedelta(days=1)
                next_day_string = next_day.strftime("%m/%d/%Y")
                file.write(f'REPORT_START_DATE           {next_day_string}\n')
                delete_lines = False  # 在写入后重置 delete_lines
                continue
            if starttime_key in line and 'REPORT_START_DATE' not in line:
                delete_lines = True
                data_list = line.split()
                # 获取日期部分并转换为日期格式
                date_string = data_list[1]
                date = datetime.strptime(date_string, "%m/%d/%Y")
                next_day = date + timedelta(days=1)
                next_day_string = next_day.strftime("%m/%d/%Y")
                file.write(f'START_DATE           {next_day_string}\n')
                delete_lines = False  # 在写入后重置 delete_lines
                continue
            if endtime_key in line:
                delete_lines = True
                data_list = line.split()
                # 获取日期部分并转换为日期格式
                date_string = data_list[1]
                date = datetime.strptime(date_string, "%m/%d/%Y")
                next_day = date + timedelta(days=1)
                next_day_string = next_day.strftime("%m/%d/%Y")
                file.write(f'END_DATE           {next_day_string}\n')
                delete_lines = False  # 在写入后重置 delete_lines
                continue

            if not delete_lines:
                file.write(line)
            if delete_lines:
                delete_lines = False


# 运行文件，并且将文件另存到对应文件夹中

def conduct(i, filename):
    write_hotstart(i, filename)
    # 运行热启动文件，并将结果保存到新的文件夹中
    writedate(filename)
