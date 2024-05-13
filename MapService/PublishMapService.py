import os

from geo.Geoserver import Geoserver
# 自己写的方法
from DatabasContent.DatabaseTable import get_table_fields
from ProcessFiles.HandlingShapeFiles.ShpProcess import get_epsg_from_prj


def publish_Shp(path, tablename):
    """
    将数据库中的数据发布到GeoServer。

    Args:
        tablename (str): 表名。

    Returns:table_name
        int: 发布结果，如果成功则返回200。

    """
    # ==============================
    table_name = "Admin" + "_" + tablename

    # 将数据库中的数据发布到GeoServer
    geo = Geoserver('http://223.2.45.130:57910/geoserver', username='admin',
                    password='geoserver')  # Creating a Geoserver instance
    try:
        workspace = geo.get_workspace(workspace='ModelCoupling')
        if workspace is None:
            geo.create_workspace(workspace='ModelCoupling')
    except:
        geo.create_workspace(workspace='ModelCoupling')

    try:
        store = geo.get_featurestore(workspace='ModelCoupling', store_name='ModelCoupledServer')
        if store is None:
            geo.create_featurestore(store_name='ModelCoupledServer', workspace='ModelCoupling', db='testDatabase',
                                    host='localhost', pg_user='postgres', pg_password='postgresql')
    except:
        geo.create_featurestore(store_name='ModelCoupledServer', workspace='ModelCoupling', db='testDatabase',
                                host='localhost', pg_user='postgres', pg_password='postgresql')
    try:
        # 使用 get_layer 方法获取图层
        layer = geo.get_layer(layer_name=table_name, workspace='ModelCoupling')
        if layer is not None:
            # 图层存在，删除图层
            geo.delete_layer(table_name)
    except:
        print("图层不存在")

    fields = get_table_fields(table_name.lower())

    # 构建 SELECT 子句
    select_clause = ", ".join(fields)

    query = f"SELECT {select_clause} FROM {table_name}"

    print("publish_Shp：" + query)

    prj_file_path = os.path.join("Data", "Admin", path, tablename + ".prj")
    epsg_code = get_epsg_from_prj(prj_file_path)
    geo.publish_featurestore_sqlview(store_name='ModelCoupledServer', name=table_name, sql=query, key_column='fid',
                                     srid=epsg_code, workspace='ModelCoupling')


def publish_Tiff(path, tablename):
    table_name = "Admin" + "_" + tablename

    # 将数据库中的数据发布到GeoServer
    geo = Geoserver('http://223.2.45.130:57910/geoserver', username='admin',
                    password='geoserver')  # Creating a Geoserver instance

    tif_file_path = os.path.join("Data", "Admin", path, tablename + ".tif")

    geo.create_coveragestore(layer_name=table_name, path=tif_file_path, workspace='ModelCoupling')
