# 后台处理

使用以下内容构建：

Django：4.2.7

GDAL：3.4.3

GeoServer REST：2.5.3

Psycopg binary：3.1.14

该项目使用Django构建，主要内容是接受前端请求，使用GDAL处理shp或栅格数据，使用Psycopg binary在PostgreSQL中处理与查询数据，使用GeoServer REST发布服务，并将服务链接返回给前端。
