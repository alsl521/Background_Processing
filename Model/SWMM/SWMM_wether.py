import os

import pandas as pd
import shutil

from django.db import connection

# 建立与数据库的连接
conn = connection


# 定义SWMM存放路径
# filename = 'control.txt'
# 生成tem文件
def create_tem(time):
    tem_query = "select name,time,maxtemperature,mintemperature from admin_temperature_observation order by fid"
    tem = pd.read_sql(tem_query, conn)
    eva_query = "select time,evaporation from admin_evaporation_observation order by fid"
    eva = pd.read_sql(eva_query, conn)
    windspeed_query = "select time,windspeed from admin_windspeedanddirection_observation order by fid"
    windspeed = pd.read_sql(windspeed_query, conn)
    dates = pd.to_datetime(tem['time'])
    years = dates.dt.year
    month = dates.dt.month
    day = dates.dt.day
    tem_with_dates = pd.concat([tem['name'], years, month, day], axis=1)
    tem_with_dates = pd.concat([tem_with_dates, tem.iloc[:, 2:]], axis=1)
    tem_with_dates = pd.concat([tem_with_dates, eva['evaporation']], axis=1)
    tem_with_dates = pd.concat([tem_with_dates, windspeed['windspeed']], axis=1)

    tem_file_name = os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\tem.dat'
    tem_text_name = os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(time) + '\\tem.txt'
    tem_with_dates.to_csv(tem_text_name, sep=' ', header=False, index=False)
    shutil.copy(tem_text_name, tem_file_name)


# 生成降雨文件
def create_rain(time):
    rain_query = "select time,rainfall from office_rainfall_observation order by fid"
    rain = pd.read_sql(rain_query, conn)
    dates = pd.to_datetime(rain['time'])
    formatted_dates = dates.dt.strftime('%m/%d/%Y')

    time_col = pd.Series(['0:00'] * len(rain))
    rain_with_dates = pd.concat([formatted_dates, time_col, rain.iloc[:, 1:]], axis=1)

    rain_file_name = os.getcwd() + '\\data\\admin\\run\\run\\SWMM\\Grain.dat'
    rain_text_name = os.getcwd() + '\\data\\admin\\run\\file\\SWMM\\' + str(time) + '\\Grain.txt'
    rain_with_dates.to_csv(rain_text_name, sep='\t', header=False, index=False)
    shutil.copy(rain_text_name, rain_file_name)


# 读写气候
def write_tem(filename, tem_file_name):
    tem_query = "select time,maxtemperature,mintemperature from admin_temperature_observation order by fid"
    tem = pd.read_sql(tem_query, conn)

    tem_key = '[TEMPERATURE]'
    eva_key = '[EVAPORATION]'
    end_key = '['
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if tem_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Data Element     Values    \n')
                file.write(f'FILE               "{tem_file_name}"         \n')
                file.write('WINDSPEED FILE  \nSNOWMELT           34 0.5 0.6 0.0 50.0 0.0\nADC IMPERVIOUS     1.0 1.0 '
                           '1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0\nADC PERVIOUS       1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 '
                           '1.0\n')
                continue

            if eva_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Data Source    Parameters\n')
                file.write(f'TEMPERATURE\nDRY_ONLY      NO\n\n')

                continue

            if end_key in line and delete_lines:
                delete_lines = False
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue

            if not delete_lines:
                file.write(line)


# 读写降雨序列
def write_rain(filename, rain_file_name):
    rain_key = '[TIMESERIES]'
    end_key = '['
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if rain_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Name           Date       Time       Value    \n')
                file.write(';;-------------- ---------- ---------- ----------\n')
                file.write(f'S1              FILE "{rain_file_name}"    \n')

                continue

            if end_key in line and delete_lines:
                delete_lines = False
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue

            if not delete_lines:
                file.write(line)
