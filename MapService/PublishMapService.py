from geo.Geoserver import Geoserver
# 自己写的方法
from DatabasContent.DatabaseTable import get_table_fields


def publish_Shp(epsg_code, table_name):
    """
    将数据库中的数据发布到GeoServer。

    Args:
        epsg_code (int): EPSG代码。
        table_name (str): 表名。

    Returns:
        int: 发布结果，如果成功则返回200。

    """
    # ==============================
    # 将数据库中的数据发布到GeoServer
    geo = Geoserver('http://localhost:8080/geoserver', username='admin',
                    password='geoserver')  # Creating a Geoserver instance
    try:
        workspace = geo.get_workspace(workspace='test')
        if workspace is not None:
            print("工作空间已存在")
        else:
            geo.create_workspace(workspace='test')
    except:
        print("不存在")
        geo.create_workspace(workspace='test')

    try:
        store = geo.get_featurestore(workspace='test', store_name='test')
        if store is not None:
            print("存储仓库已存在")
        else:
            geo.create_featurestore(store_name='test', workspace='test', db='testDatabase', host='localhost',
                                    pg_user='postgres', pg_password='postgresql')
    except:
        print("不存在")
        geo.create_featurestore(store_name='test', workspace='test', db='testDatabase', host='localhost',
                                pg_user='postgres', pg_password='postgresql')

    # 使用 get_layer 方法获取图层
    try:
        layer = geo.get_layer(layer_name=table_name, workspace='test')
        if layer is not None:
            # 图层存在，删除图层
            geo.delete_layer(table_name)
            print(f"The layer '{table_name}' in workspace '{table_name}' has been deleted.")
        else:
            print(f"The layer '{table_name}' does not exist in workspace '{table_name}'.")
    except:
        print("不存在")

    fields = get_table_fields(table_name)

    # 构建 SELECT 子句
    select_clause = ", ".join(fields)

    # 构建 FROM 子句
    from_clause = table_name

    query = f"SELECT {select_clause} FROM {from_clause}"

    print(query)

    result = geo.publish_featurestore_sqlview(store_name='test', name=table_name, sql=query, key_column='id',
                                              srid=epsg_code,
                                              workspace='test')
    if result == 201:
        return 200
