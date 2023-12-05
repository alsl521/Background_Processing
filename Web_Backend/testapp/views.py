import json
import os
import requests
from django.core import serializers
from django.core.paginator import Paginator
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from geo.Geoserver import Geoserver
from osgeo import ogr


# Create your views here.
def index(request):
    # 相应内容
    geo = Geoserver('http://localhost:8081/geoserver', username='admin', password='geoserver')

    if geo.get_workspace(workspace='test'):
        dw = geo.get_workspace(workspace='test')
        print(dw)
    else:
        geo.create_workspace(workspace='test')

    if geo.get_featurestore(workspace='test', store_name='test'):
        print('dd存在')
    else:
        geo.create_featurestore(store_name='test', workspace='test', db='testDatabase', host='localhost',
                                pg_user='postgres', pg_password='postgresql')

    # sql = 'SELECT name, gid, geom FROM sub1'
    # geo.publish_featurestore_sqlview(store_name='test', name='sub1test', sql=sql, key_column='name', srid=4547, workspace='test')

    text1 = {}
    text1["url"] = "http://localhost:8081/geoserver/test/wms"
    json_data = json.dumps(text1, indent=2, sort_keys=True, ensure_ascii=False)
    return HttpResponse(json_data, content_type="application/json")


def something(request):
    shapefile_path = 'F:/NewGroupSystem/SWMMmodel/henandata/sub1.shp'

    if os.path.exists(shapefile_path):
        print('Shapefile exists')
    else:
        print('Shapefile does not exist')

    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(shapefile_path)

    if dataset is None:
        print('Error: Could not open the Shapefile')
    else:
        print('Shapefile opened successfully')

    # Connect to PostgreSQL
    cursor = connection.cursor()

    table_name = 'locations'

    # Open the Shapefile
    ds = ogr.Open(shapefile_path)
    layer = ds.GetLayer()

    print(ds)

    # Create table if not exists
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id serial PRIMARY KEY, name VARCHAR, geometry GEOMETRY);")
    connection.commit()

    # Insert data into the table
    for feature in layer:
        geometry = feature.GetGeometryRef()
        name = feature.GetField('Name')  # Update with your attribute field
        wkt_geometry = geometry.ExportToWkt()

        cursor.execute(f"INSERT INTO {table_name} (name, geometry) VALUES (%s, ST_GeomFromText(%s, 4326));",
                       (name, wkt_geometry))

    connection.commit()

    # Close connections
    cursor.close()
    connection.close()

    # 相应内容
    return HttpResponse("欢迎使用")
