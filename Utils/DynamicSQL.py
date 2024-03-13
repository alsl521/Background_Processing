import datetime


# 进行类型映射，将 GeoServer 中的字段类型映射为 SQL 数据库字段类型
def map_geoserver_type_to_sql(geoserver_type):
    type_mapping = {
        'Integer64': 'BIGINT',
        'Integer': 'INTEGER',
        'Real': 'double precision',
        'String': 'VARCHAR',
        'Boolean': 'BOOLEAN',
        'Date': 'DATE',
        'Time': 'TIME',
        'DateTime': 'TIMESTAMP',
        # 添加更多映射...
    }

    # 返回映射结果，如果未找到则返回原类型
    return type_mapping.get(geoserver_type, geoserver_type.upper())


# 动态生成创建表的SQL语句
def generate_create_table_sql_from_shp(table_name, field_info_list, field_from_form):
    """
    动态生成创建表的SQL语句。

    Args:
        table_name (str): 表名。
        field_info_list (list): 字段信息列表。

    Returns:
        str: 创建表的SQL语句。

    """
    # 构建 CREATE TABLE 语句的起始部分
    sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY, "
    # 遍历属性字段信息，添加到 SQL 语句中
    for field_info in field_from_form:

        field_info_key = ""
        field_info_value = ""

        for key, value in field_info.items():
            field_info_key = key
            field_info_value = value

        if field_info_value != "":

            for item in field_info_list:
                if item['name'] == field_info_value:

                    geoserver_type = item['type']
                    field_width = item.get('width', None)

                    # 进行类型映射
                    sql_type = map_geoserver_type_to_sql(geoserver_type)

                    # 根据字段信息添加到 SQL 语句中
                    sql_statement += f"{field_info_key} {sql_type}"

                    # 如果是字符串类型，添加宽度信息
                    if sql_type == 'VARCHAR' and field_width is not None:
                        sql_statement += f"({field_width})"
        else:
            sql_statement += f"{field_info_key} {'VARCHAR'}"

        # 添加逗号分隔符
        sql_statement += ", "

    # 移除最后一个逗号和空格
    sql_statement = sql_statement.rstrip(', ')

    # 添加几何字段
    sql_statement += ", geometry GEOMETRY);"

    return sql_statement


def get_create_spreadsheet_sql(shpName, table_name):
    cases = {
        "FlowRate": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,flow double precision)",
        "Temperature": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,maxtemperature double precision,mintemperature double precision)",
        "AtmosphericPressure": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,atmosphericpressure double precision)",
        "Evaporation": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,evaporation double precision)",
        "Rainfall": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,rainfall double precision)",
        "SolarRadiation": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,solarradiation double precision)",
        "CloudCover": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,cloudcover double precision)",
        "WindSpeedAndDirection": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,windspeed double precision,winddirection double precision)",
        "WaterTemperature": f"CREATE TABLE IF NOT EXISTS {table_name} (Fid serial PRIMARY KEY,name VARCHAR,time TIMESTAMP,watertemperature double precision)",
    }
    sql_statement = cases.get(shpName)
    return sql_statement


def insert_into_table_from_shp_sql(table_name, field_from_form, feature, attribute_info_list):
    # 构建 CREATE TABLE 语句的起始部分
    sql_statement = f"INSERT INTO {table_name}("
    for field_info in field_from_form:
        for key, value in field_info.items():
            sql_statement += f"{key}, "
    sql_statement += "geometry) VALUES ("

    # 遍历属性字段信息，添加到 SQL 语句中
    for field_info in field_from_form:
        for key, value in field_info.items():
            if value != "":
                result = [d for d in attribute_info_list if d.get('name') == value]
                type_value = result[0].get('type')
                if type_value == 'String':
                    sql_statement += f"'{feature.GetField(value)}', "
                else:
                    sql_statement += f"{feature.GetField(value)}, "
            else:
                sql_statement += "\'\', "

    # 移除最后一个逗号和空格
    sql_statement = sql_statement.rstrip(', ')

    # 添加几何字段
    sql_statement += ", ST_GeomFromText(%s, %s));"
    return sql_statement


def get_relationship_between_data_and_fields_from_spreadsheet(field_from_form, attribute, data):
    result = []

    for row in data:
        row_dict = {}
        for field in field_from_form:
            key = list(field.keys())[0]
            value = list(field.values())[0]
            index = attribute[0].index(value)
            row_dict[key] = row[index]
        result.append(row_dict)

    return result


def insert_into_table_from_spreadsheet_sql(data, table_name, fields):
    sql_statement = f"INSERT INTO {table_name}("
    for field_info in fields:
        if field_info.lower() != 'fid':
            sql_statement += f"{field_info}, "
    sql_statement = sql_statement.rstrip(', ')
    sql_statement += ") VALUES ("

    for field_name, field_type in fields.items():
        if field_name.lower() != 'time' and field_name.lower() != 'fid':
            dataValue = data.get(field_name)
            if field_type == "character varying":
                sql_statement += "'" + dataValue + "'" + ","
            else:
                sql_statement += str(dataValue) + ","
        elif field_name.lower() == 'time':
            date = data.get(field_name)
            dataValue = date.strftime("%Y-%m-%d %H:%M:%S")
            sql_statement += "'" + dataValue + "'" + ","

    sql_statement = sql_statement.rstrip(', ')
    sql_statement += ")"

    return sql_statement


def update_table_from_form_shp_sql(results, table_name, body_data):
    sql_statement = f"UPDATE {table_name} SET "
    # 打印字段名和类型
    for row in results:
        column_name, data_type = row
        if column_name != "geometry" and column_name != "fid":
            for key, value in body_data.items():
                if column_name == key:
                    if data_type == "character varying":
                        sql_statement += column_name + "='" + value + "', "
                    elif "timestamp" in data_type:
                        sql_statement += column_name + "='" + value + "', "
                    elif value == '':
                        sql_statement += column_name + "= NULL , "
                    else:
                        sql_statement += column_name + "=" + value + ", "

    # 移除最后一个逗号和空格
    sql_statement = sql_statement.rstrip(', ')
    sql_statement += f" where fid = {body_data['fid']}"
    return sql_statement
