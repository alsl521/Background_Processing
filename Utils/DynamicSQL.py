from django.db import connection


def map_chinese_to_english(chinese_name):
    """
    将中文名称映射为英文名称。

    Args:
        chinese_name (str): 中文名称。

    Returns:
        str: 英文名称，如果映射失败则返回中文名称。

    """
    model = chinese_name.split('_')
    modelname = model[0]
    modelmenu = model[1]
    query = f"select model_table.model_table from model_table where model_name='{modelname}'"

    cursor = connection.cursor()  # Creating a cursor for the database connection
    cursor.execute(query)
    # 获取单个结果
    result = cursor.fetchone()
    if result is not None:
        model_table = result[0]
        query = f"select menu_alias from {model_table} where menu_name='{modelmenu}'"
        cursor = connection.cursor()  # Creating a cursor for the database connection
        cursor.execute(query)
        # 获取单个结果
        result = cursor.fetchone()
        if result is not None:
            print(result[0])
            return result[0]
    else:
        return chinese_name


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
def generate_create_table_sql(table_name, field_info_list):
    """
    动态生成创建表的SQL语句。

    Args:
        table_name (str): 表名。
        field_info_list (list): 字段信息列表。

    Returns:
        str: 创建表的SQL语句。

    """
    table_name = map_chinese_to_english(table_name)
    # 构建 CREATE TABLE 语句的起始部分
    sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (id serial PRIMARY KEY, "

    # 遍历属性字段信息，添加到 SQL 语句中
    for field_info in field_info_list:
        field_name = field_info['name']

        # 如果表中存在ID字段，则将其跳过
        if field_name.upper() == 'ID':
            continue

        geoserver_type = field_info['type']
        field_width = field_info.get('width', None)
        field_precision = field_info.get('precision', None)

        # 进行类型映射
        sql_type = map_geoserver_type_to_sql(geoserver_type)

        # 根据字段信息添加到 SQL 语句中
        sql_statement += f"{field_name} {sql_type}"

        # 如果是字符串类型，添加宽度信息
        if sql_type == 'VARCHAR' and field_width is not None:
            sql_statement += f"({field_width})"

        # 添加逗号分隔符
        sql_statement += ", "

    # 移除最后一个逗号和空格
    sql_statement = sql_statement.rstrip(', ')

    # 添加几何字段
    sql_statement += ", geometry GEOMETRY);"

    return sql_statement
