import pandas as pd
from django.db import connection

# 建立与数据库的连接
conn = connection

end_key = '['


# 读取[subcatchment]节
# 【subcatchments】----------------------------------------------------------------------------------------
def write_subcatchments(filename):
    sub_query = "select name,raingage,outfall,area,zero,width, slope,curblen from admin_hru_observation order by fid"
    sub = pd.read_sql(sub_query, conn)
    subcatchments_key = '[SUBCATCHMENTS]'

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if subcatchments_key in line:
                delete_lines = True
                file.write(line)
                file.write(
                    ';;Name           Rain Gage        Outlet           Area     %Imperv  Width    %Slope   CurbLen  SnowPack        \n')
                file.write(
                    ';;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- ----------------\n')
                continue
            if end_key in line and delete_lines:
                delete_lines = False
                sub_csv = sub.to_csv(index=False, header=False, sep=',')
                sub_csv_with_multiple_spaces = sub_csv.replace(',', '          ')
                lines_to_write = sub_csv_with_multiple_spaces.split('\n')
                # 写入 sub_csv_with_multiple_spaces
                for idx, line_to_write in enumerate(lines_to_write):
                    if line_to_write.strip() or idx == len(lines_to_write) - 1:
                        file.write(line_to_write)
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue
            if not delete_lines:
                file.write(line)


# 读取[subarea]节
# 【subareas】----------------------------------------------------------------------------------------
def write_subareas(filename):
    subareas_query = "select name,nimp,nperv,simp,sperv,pctzero,routeto from admin_hru_observation order by fid"
    subareas = pd.read_sql(subareas_query, conn)
    subareas_key = '[SUBAREAS]'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if subareas_key in line:
                delete_lines = True
                file.write(line)
                file.write(
                    ';;Name           N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted         \n')
                file.write(
                    ';;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- ----------------\n')
                continue
            if end_key in line and delete_lines:
                delete_lines = False
                subareas_csv = subareas.to_csv(index=False, header=False, sep=',')
                subareas_csv_with_multiple_spaces = subareas_csv.replace(',', '          ')
                lines_to_write = subareas_csv_with_multiple_spaces.split('\n')
                # 写入 sub_csv_with_multiple_spaces
                for idx, line_to_write in enumerate(lines_to_write):
                    if line_to_write.strip() or idx == len(lines_to_write) - 1:
                        file.write(line_to_write)
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue
            if not delete_lines:
                file.write(line)


# 读取[JUNCTIONS]节
# 【junction】----------------------------------------------------------------------------------------
def write_junction(filename):
    junction_query = "select name,invertelevation,mdepth,idepth,sdepth,pondedarea from admin_junction_observation order by fid"
    junction = pd.read_sql(junction_query, conn)

    junction_key = '[JUNCTIONS]'

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if junction_key in line:
                delete_lines = True
                file.write(line)
                file.write(
                    ';;Name   InvertElev   MaxDepth     InitDepth   SurchargeDepth     PondedArea         \n')
                file.write(
                    ';;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- ----------------\n')
                continue
            if end_key in line and delete_lines:
                delete_lines = False
                junction_csv = junction.to_csv(index=False, header=False, sep=',')
                junction_csv_with_multiple_spaces = junction_csv.replace(',', '          ')
                lines_to_write = junction_csv_with_multiple_spaces.split('\n')
                # 写入 sub_csv_with_multiple_spaces
                for idx, line_to_write in enumerate(lines_to_write):
                    if line_to_write.strip() or idx == len(lines_to_write) - 1:
                        file.write(line_to_write)
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue
            if not delete_lines:
                file.write(line)


# 读取[RAINGAGES]节
# 【RAINGAGE】----------------------------------------------------------------------------------------
def write_raingage(filename):
    raingage_query = "select name,format,intvl,scf,datasource,sourcename from admin_raingauge_observation order by fid"
    raingage = pd.read_sql(raingage_query, conn)
    raingage_key = '[RAINGAGES]'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(filename, 'w', encoding='utf-8') as file:
        delete_lines = False
        for line in lines:
            if raingage_key in line:
                delete_lines = True
                file.write(line)
                file.write(';;Name           Format    Interval SCF      Source \n')
                file.write(
                    ';;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- ----------------\n')
                continue
            if end_key in line and delete_lines:
                delete_lines = False
                raingage_csv = raingage.to_csv(index=False, header=False, sep=',')
                raingage_csv_with_multiple_spaces = raingage_csv.replace(',', '          ')
                lines_to_write = raingage_csv_with_multiple_spaces.split('\n')
                # 写入 sub_csv_with_multiple_spaces
                for idx, line_to_write in enumerate(lines_to_write):
                    if line_to_write.strip() or idx == len(lines_to_write) - 1:
                        file.write(line_to_write)
                file.write('\n')
                # 写入 end_key 行
                file.write(line)
                continue

            if not delete_lines:
                file.write(line)
