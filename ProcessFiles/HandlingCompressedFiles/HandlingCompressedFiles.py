from DatabasContent.ShpToDatabaseTable import shp_to_database_table
from ProcessFiles.HandlingCompressedFiles.UnzipFiles import Unzip_Zip_Files


def handling_compressed_files(targetFolder, ModelName, MenuName, file):
    """
    处理压缩文件并返回发布的表的名称。

    Args:
        targetFolder (str): 目标文件夹路径。
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (UploadedFile): 上传的文件对象。

    Returns:
        str: 发布的表的名称。

    """

    # 获取文件名
    file_name = file.name

    # 确定是哪个类型的文件
    file_parts = file_name.split('.')

    table_name = ""
    if file_parts[1] == "zip":
        table_name = handling_zip_files(ModelName, MenuName, file)
    elif file_parts[1] == "rar":
        print("sssss")
    elif file_parts[1] == "7z":
        print("ssss")

    return table_name


def handling_zip_files(ModelName, MenuName, file):
    """
    处理ZIP文件，包括存储文件、解压文件和处理shp数据。

    Args:
        ModelName (str): 模型名称。
        MenuName (str): 菜单名称。
        file (UploadedFile): 上传的文件对象。

    Returns:
        str: 发布的表的名称。

    """

    # 获取文件数据并存储起来
    filePath = "TemporaryFolder/UpLoadFile.zip"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()

    # 解压文件
    Unzip_Zip_Files(filePath, "TemporaryFolder", ModelName, MenuName)

    # 处理shp数据
    table_name = shp_to_database_table("TemporaryFolder")

    # 返回发布的表的名称
    return table_name
