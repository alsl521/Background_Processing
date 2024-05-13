import pandas as pd
import geopandas as gpd


def get_topological_result(dataframe1, dataframe2, unique_value_index="fid_1"):
    # ����dataframe1��dataframe2������DataFrame����

    # ��ȡ����DataFrame������
    columns1 = dataframe1.columns
    columns2 = dataframe2.columns

    # �ϲ������б�
    merged_columns = list(filter(lambda x: x != "fid" and x != "geometry", columns1)) + list(
        filter(lambda x: x != "fid", columns2))

    # ִ���ཻ����
    intersection = gpd.overlay(dataframe1, dataframe2, how='intersection')
    intersection.rename(columns={"fid_1": "fid"}, inplace=True)

    # ���� modflowcel �е�������ɸѡ����
    max_area_rows = intersection.groupby(unique_value_index)['geometry'].apply(lambda x: x[x.area == x.area.max()])

    # ���������Ķ�������ݴ洢���µ� GeoDataFrame ��
    max_area_df = gpd.GeoDataFrame(max_area_rows, geometry='geometry')

    # ��ԭʼ intersection ��ɾ����Ӧ����
    filtered_intersection = pd.merge(intersection, max_area_df, how='inner', on=[unique_value_index, 'geometry'],
                                     suffixes=('_orig', '_filtered'))

    # �ϲ� filtered_intersection �� dataframe1�����滻������Ϣ
    merged_df = filtered_intersection.merge(dataframe1[[unique_value_index, 'geometry']], on=unique_value_index,
                                            suffixes=('_filtered', '_dataframe1'))
    merged_df['geometry'] = merged_df['geometry_dataframe1']

    # �����µ� GeoDataFrame�������滻��ļ�����Ϣ
    filtered_intersection_with_geometry = gpd.GeoDataFrame(merged_df, geometry='geometry')

    # ѡ��һ�������в�ת��Ϊ GeoDataFrame
    filtered_intersection_with_geometry_single = filtered_intersection_with_geometry[merged_columns].copy()
    filtered_intersection_with_geometry_single = gpd.GeoDataFrame(filtered_intersection_with_geometry_single,
                                                                  geometry='geometry')

    return filtered_intersection_with_geometry_single
