import json

from django.db import connection


def get_menu_from_table(ModelName):
    """
    从数据库表中获取菜单。

    Args:
        ModelName (str): 模型名称。

    Returns:
        dict: 菜单字典。

    """
    cur = connection.cursor()

    query = "SELECT model_table.model_table FROM model_table WHERE model_table.model_name = %s;"
    cur.execute(query, (ModelName,))
    result = cur.fetchone()

    if result:
        model_table_value = result[0]
        result_dict = get_menu(ModelName, model_table_value)
        return result_dict
    else:
        print("未找到匹配的记录")


def get_menu(ModelName, model_table_value):
    """
    获取菜单。

    Args:
        ModelName (str): 模型名称。
        model_table_value (str): 模型表的值。

    Returns:
        list: 菜单列表。

    """
    cur = connection.cursor()

    query = f"SELECT * FROM {model_table_value} WHERE not_submenu = true ORDER BY id ASC;"
    cur.execute(query)
    result = cur.fetchall()

    result_list = []
    for row in result:
        menu_item = {
            "index": ModelName + "-" + row[1],
            "menu_name": row[1],
            "sub_menu_name": None,  # Default value
            "upload_file_type": row[4]
        }

        submenu = get_submenu(ModelName, model_table_value, row[3])
        if submenu:
            menu_item["sub_menu_name"] = submenu

        result_list.append(menu_item)

    return result_list


def get_submenu(ModelName, model_table_value, submenu):
    """
    获取子菜单。

    Args:
        ModelName (str): 模型名称。
        model_table_value (str): 模型表的值。
        submenu (str): 子菜单。

    Returns:
        list or None: 子菜单列表或None。

    """
    if submenu is not None:
        cur = connection.cursor()
        submenu = submenu.split(',')
        submenu_list = []

        for submenuitem in submenu:
            query = f"SELECT * FROM {model_table_value} WHERE menu_name = '{submenuitem}';"
            cur.execute(query)
            result = cur.fetchall()

            for row in result:
                submenu_item = {
                    "index": ModelName + "-" + row[1],
                    "menu_name": row[1],
                    "sub_menu_name": None,  # Default value
                    "upload_file_type": row[4]
                }

                sub_submenu = get_submenu(ModelName, model_table_value, row[3])
                if sub_submenu:
                    submenu_item["sub_menu_name"] = sub_submenu

                submenu_list.append(submenu_item)

        return submenu_list

    return None
