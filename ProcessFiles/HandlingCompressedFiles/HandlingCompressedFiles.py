from ProcessFiles.HandlingCompressedFiles.UnzipFiles import Unzip_Zip_Files
from Utils.CopyFiles import copy_models_files
from Utils.CreateFolders import create_user_model_folders
from Utils.DeleteFiles import delete_folder_contents_only


def handling_compressed_files(filename, file):
    """
    处理压缩文件并返回发布的表的名称。

    Args:
        filename (str): 文件名称
        file (UploadedFile): 上传的文件对象。

    Returns:
        str: 发布的表的名称。

    """
    delete_folder_contents_only("Data/TemporaryFolder")  # 清空临时文件夹内容
    folder_path = create_user_model_folders(filename)
    # 获取文件名
    file_name = file.name

    # 确定是哪个类型的文件
    file_parts = file_name.split('.')

    if file_parts[1] == "zip":
        handling_zip_files(filename, file)
    elif file_parts[1] == "rar":
        print("sssss")
    elif file_parts[1] == "7z":
        print("ssss")

    copy_models_files("Data/TemporaryFolder", folder_path)


def handling_zip_files(filename, file):
    """
    处理ZIP文件，包括存储文件、解压文件和处理shp数据。

    Args:
        filename (str): 文件名称
        file (UploadedFile): 上传的文件对象。

    Returns:
        str: 发布的表的名称。

    """

    # 获取文件数据并存储起来
    filePath = "Data/TemporaryFolder/UpLoadFile.zip"
    file_obj = file
    f = open(filePath, mode='wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()

    # 解压文件
    Unzip_Zip_Files(filePath, "Data/TemporaryFolder", filename)
