# -*- coding: gbk -*-
import os

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from django.db import connection

from Utils.topology import get_topological_result


def InitializeFirstModFlowWaterlevel(NowTimeWritePath, CurrentTime):
    def replace_and_sum(row):
        if pd.isna(row['efdcwater']):
            # ��� efdcwater �� NaN��������滻����
            modflowcol = row['modflowcol']
            modflowrow = row['modflowrow']
            row['efdcwater'] = (
                merged_gdf[
                    (merged_gdf['modflowcol'] >= modflowcol - 1)
                    & (merged_gdf['modflowcol'] <= modflowcol + 1)
                    & (merged_gdf['modflowrow'] >= modflowrow - 1)
                    & (merged_gdf['modflowrow'] <= modflowrow + 1)
                    & ~merged_gdf['efdcwater'].isna()
                    ]['efdcwater']
            ).mean()

            row['underwater_topography'] = (
                merged_gdf[
                    (merged_gdf['modflowcol'] >= modflowcol - 1)
                    & (merged_gdf['modflowcol'] <= modflowcol + 1)
                    & (merged_gdf['modflowrow'] >= modflowrow - 1)
                    & (merged_gdf['modflowrow'] <= modflowrow + 1)
                    & ~merged_gdf['underwater_topography'].isna()
                    ]['underwater_topography']
            ).mean()
        return row

    conn = connection
    UnderwaterRelief = os.getcwd() + r"\Data\Admin\BasicDataService\MonitoringData\RiverMonitoringStation\UnderwaterRelief\UnderwaterRelief.tif"
    model_riv = NowTimeWritePath + "\\model.riv"
    # ��ȡ��һ����ļ�������
    query_modflow = "SELECT fid, modflowcol, modflowrow, modflowcel, active, geometry FROM admin_modflowspatialdiscretedata"
    df_modflow = gpd.GeoDataFrame.from_postgis(query_modflow, conn, geom_col='geometry')

    # ��ȡ��������
    query_river = "SELECT fid, name, geometry FROM admin_river"
    df_river = gpd.GeoDataFrame.from_postgis(query_river, conn, geom_col='geometry')

    # ɾ�� active=0 ������
    df_modflow = df_modflow[df_modflow['active'] != 0]

    df_river_result = get_topological_result(df_modflow, df_river, 'modflowcel')

    # ��ȡ�ڶ�����ļ�������
    query_efdc = "SELECT fid, efdccel, efdcrow, efdccol, efdcwater, geometry FROM admin_efdc_initialwaterlevel"
    df_efdc = gpd.GeoDataFrame.from_postgis(query_efdc, conn, geom_col='geometry')

    # ��դ�������ļ�
    dataset = rasterio.open(UnderwaterRelief)
    # ��ȡ���в��ε�դ������
    data = dataset.read()
    # �ر����ݼ�
    dataset.close()
    # ���ض�ֵ������-9999���滻ΪNaN
    data = np.where(data == -9999, np.nan, data)
    # ����ά�б�����չƽΪһά�����޳�NaNֵ
    flattened_data = data.flatten()
    flattened_data = flattened_data[~np.isnan(flattened_data)]
    # ����һ���µ�����������
    new_column = 'underwater_topography'
    # ����һά��
    new_series = pd.Series(flattened_data, name=new_column)
    # ��һά����ӵ����е� GeoDataFrame ��
    df_efdc[new_column] = new_series

    # ��ȡ��������ļ�������
    query_efdcspatial = "SELECT fid, efdccol, efdcrow, efdccel, isdry, efdccollon, efdcrowlon, geometry FROM admin_efdcspatialdiscretedata"
    df_efdc_spatial = gpd.GeoDataFrame.from_postgis(query_efdcspatial, conn, geom_col='geometry')

    duplicated_columns = df_efdc.columns.intersection(df_efdc_spatial.columns)
    duplicated_columns = [col for col in duplicated_columns if col != "efdccel"]

    # ִ�кϲ�����
    merged_df = pd.merge(df_efdc, df_efdc_spatial.drop(columns=duplicated_columns), on='efdccel')
    # ���ϲ���� DataFrame ת��Ϊ GeoDataFrame
    merged_gdf = gpd.GeoDataFrame(merged_df, geometry='geometry')

    # ���� isdry ������ 2 ����
    merged_gdf = merged_gdf[merged_gdf['isdry'] != 2]

    result = get_topological_result(df_river_result, merged_gdf, 'modflowcel')
    result = result.drop(
        columns=['geometry', 'efdccel', 'efdcrow', 'efdccol', 'name', 'isdry', 'efdccollon', 'efdcrowlon', 'active'])

    result[['efdcwater', 'underwater_topography']] = result[['efdcwater', 'underwater_topography']].apply(pd.to_numeric)
    grouped = result.groupby('modflowcel').agg({'efdcwater': 'mean', 'underwater_topography': 'mean'})
    grouped[['efdcwater', 'underwater_topography']] = grouped[['efdcwater', 'underwater_topography']].values
    grouped.reset_index(inplace=True)

    merged_gdf = pd.merge(df_river_result, grouped, on='modflowcel', how='left')

    # Ӧ�ú��������滻����Ͳ���
    merged_gdf = merged_gdf.apply(replace_and_sum, axis=1)

    with open(model_riv, 'r') as file:
        lines = file.readlines()

    data_found = False
    extracted_data = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line:
            split_data = cleaned_line.split()
            extracted_data.append(split_data)

    for i in range(2, len(extracted_data)):

        for index, row in merged_gdf.iterrows():

            if int(row['modflowrow']) == int(extracted_data[i][1]) and int(row['modflowcol']) == int(
                    extracted_data[i][2]):
                extracted_data[i][3] = str(round(float(row['efdcwater']), 3))
                extracted_data[i][5] = str(round(float(row['underwater_topography']), 3))

    # ���ļ�����д��ģʽд������
    with open(model_riv, 'w') as file:
        # �����б��е�ÿ��Ԫ��
        for row in extracted_data:
            # ��ÿ��Ԫ��ת��Ϊ�ַ��������Ʊ���ָ�
            line = ' '.join(str(item) for item in row)
            # д��ÿһ�е��ļ��У�ÿ��ռһ��
            file.write(line + '\n')

    print("��" + str(CurrentTime) + "Ӧ����model.riv��д���")


def HandlingRCH(NowTimeWritePath, CurrentTime):
    conn = connection
    # ��ȡ��һ����ļ�������
    query1 = "SELECT fid, modflowcol, modflowrow, modflowcel, active, geometry FROM admin_modflowspatialdiscretedata"
    dataframe1 = gpd.GeoDataFrame.from_postgis(query1, conn, geom_col='geometry')

    query2 = "SELECT fid, name, landuse, nimp, nperv, simp, sperv, raingage, outfall, curblen, width, slope, pctzero, routeto, area, geometry FROM admin_swmmspatialdiscretedata"
    dataframe2 = gpd.GeoDataFrame.from_postgis(query2, conn, geom_col='geometry')

    result = get_topological_result(dataframe1, dataframe2, 'modflowcel')

    with open(os.getcwd() + r"\Data\Admin\Run\result\SWMM\��" + str(CurrentTime) + r"Ӧ����\test1.rep", 'r') as file:
        lines = file.readlines()

    data_found = False
    extracted_data = []

    for line in lines:
        if not data_found and "Subcatchment                 mm         mm         mm         mm         mm         mm         mm    10^6 ltr      CMS" in line:
            data_found = True
            continue
        if "Analysis begun on:" in line:
            data_found = True
            continue
        if data_found:
            cleaned_line = line.strip()
            if cleaned_line:
                split_data = cleaned_line.split()
                extracted_data.append(split_data)

    # �Ƴ���һ�к����һ��
    new_list = extracted_data[1:-1]

    result_dict = {row[0]: row[4] for row in new_list}

    result['rch'] = result['name'].apply(lambda x: result_dict.get(x))

    duplicated_columns = dataframe1.columns.intersection(result.columns)
    duplicated_columns = [col for col in duplicated_columns if col != "modflowcel"]
    gdf_unique = result.drop(columns=duplicated_columns)
    merged_gdf = pd.merge(dataframe1, gdf_unique, on='modflowcel', how='left')
    merged_gdf = merged_gdf.fillna(0)

    with open(NowTimeWritePath + "\\model.rch", 'r') as file:
        lines = file.readlines()
    extracted_data = []

    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line:
            split_data = cleaned_line.split()
            extracted_data.append(split_data)

    # ���ļ�����д��ģʽд������
    with open(NowTimeWritePath + "\\model.rch", 'w') as file:
        # �����б��е�ÿ��Ԫ��
        for row in extracted_data[:3]:
            # ��ÿ��Ԫ��ת��Ϊ�ַ��������Ʊ���ָ�
            line = ' '.join(str(item) for item in row)
            # д��ÿһ�е��ļ��У�ÿ��ռһ��
            file.write(line + '\n')

        prev_modflowrow = None

        # ѭ������GeoDataFrame
        for index, row in merged_gdf.iterrows():
            modflowrow = row['modflowrow']
            rch = row['rch']

            # ��modflowcol�仯ʱ�����л���д��
            if modflowrow != prev_modflowrow and prev_modflowrow is not None:
                file.write('\n')

            # д��rchֵ
            file.write(str(rch) + ' ')

            prev_modflowrow = modflowrow

    print("��" + str(CurrentTime) + "Ӧ����rch��д���")


def EFDCToMODFLOWContext(NowTimeWritePath, CurrentTime):
    conn = connection

    def replace_and_sum(row):
        if pd.isna(row['level']):
            # ��� efdcwater �� NaN��������滻����
            modflowcol = row['modflowcol']
            modflowrow = row['modflowrow']
            row['level'] = (
                merged_gdf[
                    (merged_gdf['modflowcol'] >= modflowcol - 1)
                    & (merged_gdf['modflowcol'] <= modflowcol + 1)
                    & (merged_gdf['modflowrow'] >= modflowrow - 1)
                    & (merged_gdf['modflowrow'] <= modflowrow + 1)
                    & ~merged_gdf['level'].isna()
                    ]['level']
            ).mean()
        return row

    UnderwaterRelief = os.getcwd() + r"\Data\Admin\BasicDataService\MonitoringData\RiverMonitoringStation\UnderwaterRelief\UnderwaterRelief.tif"

    # ��ȡ��һ����ļ�������
    query_modflow = "SELECT fid, modflowcol, modflowrow, modflowcel, active, geometry FROM admin_modflowspatialdiscretedata"
    df_modflow = gpd.GeoDataFrame.from_postgis(query_modflow, conn, geom_col='geometry')

    # ��ȡ��������
    query_river = "SELECT fid, name, geometry FROM admin_river"
    df_river = gpd.GeoDataFrame.from_postgis(query_river, conn, geom_col='geometry')

    # ɾ��δ��������
    df_modflow = df_modflow[df_modflow['active'] != 0]

    # ��ȡ���˽��
    df_river_result = get_topological_result(df_modflow, df_river, 'modflowcel')

    # ��դ�������ļ�
    with rasterio.open(UnderwaterRelief) as dataset:
        data = dataset.read()
        rows, cols = dataset.shape

    # ���������ļ���
    folder = os.getcwd() + r"\Data\Admin\Run\Run\EFDC\��" + str(CurrentTime - 1) + r"Ӧ����\#output"
    keyword = "ˮλ"
    extracted_data = []

    # ѭ�������ļ����µ��ļ�
    for file_name in os.listdir(folder):
        if keyword in file_name:
            file_path = os.path.join(folder, file_name)

            # ��ȡ�ļ��е�����
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    cleaned_line = line.strip()
                    if cleaned_line:
                        split_data = cleaned_line.split()
                        extracted_data.append(split_data)

    # ��ȡEFDC�ռ���ɢ����
    query_efdc = "SELECT fid, efdccol, efdcrow, efdccel, isdry, efdccollon, efdcrowlon, geometry FROM admin_efdcspatialdiscretedata"
    df_efdc = gpd.GeoDataFrame.from_postgis(query_efdc, conn, geom_col='geometry')

    # ����ˮλ����
    for data in extracted_data:
        data[2] = str(int(rows) - int(data[2]) + 3)
        data[1] = str(int(data[1]) - 2)

        mask = (df_efdc['efdccol'] == int(data[1])) & (df_efdc['efdcrow'] == int(data[2]))
        df_efdc.loc[mask, 'level'] = data[3]

    # ����isdry������2����
    df_efdc = df_efdc[df_efdc['isdry'] != 2]

    # ɾ������Ҫ����
    df_efdc.drop(
        columns=['efdccol', 'efdcrow', 'efdccel', 'isdry', 'efdccollon', 'efdcrowlon'], inplace=True)

    # ��ȡ������EFDC�����˽��
    df_efdc_river_result = get_topological_result(df_river_result, df_efdc, 'modflowcel')

    # ת��Ϊ��ֵ����
    df_efdc_river_result[['level']] = df_efdc_river_result[['level']].apply(pd.to_numeric)

    # ���鲢��level��ƽ��
    grouped = df_efdc_river_result.groupby('modflowcel').agg({'level': 'mean'}).reset_index()

    # �ϲ����
    merged_gdf = pd.merge(df_river_result, grouped, on='modflowcel', how='left')

    # Ӧ�ú��������滻����Ͳ���
    merged_gdf = merged_gdf.apply(replace_and_sum, axis=1)

    # ��ȡģ���ļ�
    with open(os.getcwd() + r"\Data\Admin\Run\file\modflow\��1Ӧ����\model.riv", 'r') as file:
        lines = file.readlines()

    extracted_data = [line.strip().split() for line in lines if line.strip()]

    # ����ˮλ����
    for i in range(2, len(extracted_data)):
        for index, row in merged_gdf.iterrows():
            if int(row['modflowrow']) == int(extracted_data[i][1]) and int(row['modflowcol']) == int(
                    extracted_data[i][2]):
                extracted_data[i][3] = str(round(float(row['level']) + float(extracted_data[i][5]), 3))

    # д���ļ�
    with open(NowTimeWritePath + "\\model.riv", 'w') as file:
        for row in extracted_data:
            file.write(' '.join(map(str, row)) + '\n')

    print("��" + str(CurrentTime) + "Ӧ����model.riv��д���")


def GetBasicFileContext(CurrentTime):
    basic_dis_file = os.getcwd() + r"\Data\Admin\Run\file\modflow\��1Ӧ����\model.dis"
    basic_hds_file = os.getcwd() + r"\Data\Admin\Run\result\modflow\��" + str(CurrentTime - 1) + r"Ӧ����\model.HDS"

    # ��Dis��ȡ�ռ���ɢ��ʱ����ɢ
    spatial_dispersion_stream_reader = open(basic_dis_file, "r")

    spatial_dispersion_stream_reader_line = spatial_dispersion_stream_reader.readline()
    parts = spatial_dispersion_stream_reader_line.split(' ')
    spatial_dispersion_stream_reader_lines = []
    for part in parts:
        if part.strip():
            spatial_dispersion_stream_reader_lines.append(part)

    all_layer = int(spatial_dispersion_stream_reader_lines[0])
    row = int(spatial_dispersion_stream_reader_lines[1])
    column = int(spatial_dispersion_stream_reader_lines[2])
    stress_periods_count = int(spatial_dispersion_stream_reader_lines[3])

    spatial_dispersion_stream_reader.close()

    line = ""
    flag_count = 0
    modflow_basic_file_head = []
    modflow_basic_file_context = []

    basic_bas_file = os.getcwd() + r"\Data\Admin\Run\file\modflow\��" + str(CurrentTime - 1) + r"Ӧ����\model.bas6"
    basic_current_bas_file = os.getcwd() + r"\Data\Admin\Run\file\modflow\��" + str(CurrentTime) + r"Ӧ����\model.bas6"

    basic_file_path = basic_bas_file

    sw = open(basic_current_bas_file, 'w')

    # ��ȡ��һ��Ӧ����Bas����
    with open(basic_file_path, 'r') as reader:
        for line in reader:
            if flag_count < 1:
                if line == "-999\n":
                    flag_count += 1
                modflow_basic_file_head.append(line)
                sw.write(line)
            else:
                parts = line.rstrip().split(' ')
                modflow_basic_file_context.append(parts)

    modflow_hds_file = []
    modflow_hds_file_lines = []

    modflow_hds_file_path = basic_hds_file

    with open(modflow_hds_file_path, 'r') as reader:
        for line in reader:
            parts = line.rstrip().split(' ')
            modflow_hds_file.append(parts)

    # ȥ�����ַ���
    modflow_hds_file = [[x for x in sublist if x.strip()] for sublist in modflow_hds_file]

    # �������ˮͷ����ת��Ϊ��һʱ�̵�bas6
    values = [[[None for _ in range(column)] for _ in range(row)] for _ in range(all_layer)]
    layer_flag = 0
    row_flag = 0
    column_flag = 0
    for i in range(len(modflow_hds_file)):
        if len(modflow_hds_file[i]) == 9 and modflow_hds_file[i][4] == "HEAD":
            continue
        else:
            for j in range(len(modflow_hds_file[i])):
                values[layer_flag][row_flag][column_flag] = modflow_hds_file[i][j]
                column_flag += 1
            if column_flag == column:
                row_flag += 1
                column_flag = 0
            if row_flag == row:
                layer_flag += 1
                row_flag = 0
                column_flag = 0
            if layer_flag == all_layer:
                break

    writeline = ""
    flag = 0
    for i in range(all_layer):
        # ��дINTERNAL 0.0 (FREE) 0
        if flag == i:
            for j in range(len(modflow_basic_file_context[i * row + flag])):
                if j == 0:
                    writeline = modflow_basic_file_context[i * row + flag][j]
                else:
                    writeline += " " + modflow_basic_file_context[i * row + flag][j]
            sw.write(writeline + "\n")
            flag += 1

        # ��дӦ����������
        for j in range(row):
            for k in range(column):
                if k == 0:
                    writeline = values[i][j][k]
                else:
                    writeline += " " + values[i][j][k]
            sw.write(writeline + "\n")

    sw.close()
    print("��" + str(CurrentTime) + "Ӧ����model.bas6��д���")


def generate_efdc_file(CurrentTime):
    with open(os.getcwd() + r"\Data\Admin\Run\result\modflow\��" + str(CurrentTime) + r"Ӧ����\model.BGT",
              'r') as file:
        found_target = False
        skip_lines = 3
        second_line_after_target = ""
        data_counter = 0
        should_record_data = False
        data_array = []

        for line in file:
            if found_target:

                if skip_lines > 0:
                    skip_lines -= 1
                    if skip_lines == 0:
                        second_line_after_target = line
                else:
                    data = line.split()
                    value_3 = data[2]
                    value_4 = data[3]
                    value_5 = str(float(data[4]) / 86400)
                    data_array.append([value_3, value_4, value_5])
                    data_counter += 1
                    if data_counter == int(second_line_after_target):
                        found_target = True
                        break

            if 'RIVER LEAKAGE' in line:
                found_target = True

    with open(os.getcwd() + r"\Data\Admin\Run\Result\MODFLOW\��" + str(CurrentTime) + r"Ӧ����\ModflowRiverFlow.txt",
              'w') as output_file:
        output_file.write("Modflowcol	Modflowrow	RiverFlow\n")
        for row in data_array:
            output_file.write('\t'.join(row) + '\n')
