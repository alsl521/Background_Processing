from Utils.CopyFiles import copy_models_files
from Utils.CreateFolders import create_user_model_folders
from Utils.DeleteFiles import delete_folder_contents_only


def handling_spreadsheet_files(filename, file, shpName):
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
    delete_folder_contents_only("Data/TemporaryFolder")  # 清空临时文件夹内容
    folder_path = create_user_model_folders(filename)
    file_name = file.name
    # 确定是哪个类型的文件
    file_parts = file_name.split('.')

    parts = filename.split("_")

    if file_parts[1] == "txt":
        handling_txt_files(shpName, file)
    elif file_parts[1] == "xlsx":
        handling_xlsx_files(shpName, file)
    elif file_parts[1] == "xls":
        handling_xls_files(shpName, file)

    copy_models_files("Data/TemporaryFolder", folder_path)


def handling_txt_files(filename, file):
    """
    处理 TXT 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"Data/TemporaryFolder/{filename}.txt"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()


def handling_xlsx_files(filename, file):
    """
    处理 XLSX 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"Data/TemporaryFolder/{filename}.xlsx"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()


def handling_xls_files(filename, file):
    """
    处理 XLS 文件。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (File): 文件对象。

    """
    # 获取文件数据并存储起来
    filePath = f"Data/TemporaryFolder/{filename}.xls"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
