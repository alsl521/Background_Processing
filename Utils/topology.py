import pandas as pd
import geopandas as gpd


def get_topological_result(dataframe1, dataframe2, unique_value_index="fid_1"):
    # 假设dataframe1和dataframe2是两个DataFrame对象

    # 获取两个DataFrame的列名
    columns1 = dataframe1.columns
    columns2 = dataframe2.columns

    # 合并列名列表
    merged_columns = list(filter(lambda x: x != "fid" and x != "geometry", columns1)) + list(
        filter(lambda x: x != "fid", columns2))

    # 执行相交处理
    intersection = gpd.overlay(dataframe1, dataframe2, how='intersection')
    intersection.rename(columns={"fid_1": "fid"}, inplace=True)

    # 根据 modflowcel 列的最大面积筛选数据
    max_area_rows = intersection.groupby(unique_value_index)['geometry'].apply(lambda x: x[x.area == x.area.max()])

    # 将最大面积的多边形数据存储在新的 GeoDataFrame 中
    max_area_df = gpd.GeoDataFrame(max_area_rows, geometry='geometry')

    # 从原始 intersection 中删除对应数据
    filtered_intersection = pd.merge(intersection, max_area_df, how='inner', on=[unique_value_index, 'geometry'],
                                     suffixes=('_orig', '_filtered'))

    # 合并 filtered_intersection 和 dataframe1，并替换几何信息
    merged_df = filtered_intersection.merge(dataframe1[[unique_value_index, 'geometry']], on=unique_value_index,
                                            suffixes=('_filtered', '_dataframe1'))
    merged_df['geometry'] = merged_df['geometry_dataframe1']

    # 创建新的 GeoDataFrame，包含替换后的几何信息
    filtered_intersection_with_geometry = gpd.GeoDataFrame(merged_df, geometry='geometry')

    # 选择一个几何列并转换为 GeoDataFrame
    filtered_intersection_with_geometry_single = filtered_intersection_with_geometry[merged_columns].copy()
    filtered_intersection_with_geometry_single = gpd.GeoDataFrame(filtered_intersection_with_geometry_single,
                                                                  geometry='geometry')

    return filtered_intersection_with_geometry_single
