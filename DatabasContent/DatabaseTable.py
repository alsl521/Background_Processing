from django.db import connection  # Importing connection for interacting with the database


def get_table_fields(table_name):
    """
    获取表中的所有字段。

    Args:
        table_name (str): 表名。

    Returns:
        list: 字段列表。

    """
    # 获取表中的所有字段
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")

    # 获取字段名称
    fields = [row[0] for row in cursor.fetchall()]

    # 关闭数据库连接
    cursor.close()

    # 返回字段列表
    return fields


def drop_table_if_exists(table_name):
    """
        如果表存在，则删除表。

        Args:
            table_name (str): 表名。

        """
    cursor = connection.cursor()

    # 检查表是否存在
    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
    exists = cursor.fetchone()[0]

    if exists:
        # 删除表
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"The table '{table_name}' has been dropped.")
    else:
        print(f"The table '{table_name}' does not exist.")

    connection.commit()
    cursor.close()
