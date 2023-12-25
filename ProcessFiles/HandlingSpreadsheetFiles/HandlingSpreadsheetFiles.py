def handling_spreadsheet_files(targetFolder, ModelName, MenuName, file):
    """
        处理电子表格文件。

        Args:
            targetFolder (str): 目标文件夹。
            ModelName (str): 模型名称。
            MenuName (str): 菜单名称。
            file (File): 文件对象。

        Returns:
            str: 表名。

    """
    # 获取文件名
    file_name = file.name

    # 确定是哪个类型的文件
    file_parts = file_name.split('.')

    table_name = ""
    if file_parts[1] == "txt":
        handling_txt_files(ModelName, MenuName, file)
    elif file_parts[1] == "xlsx":
        handling_xlsx_files(ModelName, MenuName, file)
    elif file_parts[1] == "xls":
        handling_xls_files(ModelName, MenuName, file)

    return table_name


def handling_txt_files(ModelName, MenuName, file):
    """
    处理 TXT 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"TemporaryFolder/{ModelName}_{MenuName}.txt"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()


def handling_xlsx_files(ModelName, MenuName, file):
    """
    处理 XLSX 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"TemporaryFolder/{ModelName}_{MenuName}.xlsx"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()


def handling_xls_files(ModelName, MenuName, file):
    """
    处理 XLS 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"TemporaryFolder/{ModelName}_{MenuName}.xls"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
