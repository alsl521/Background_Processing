import zipfile
import os
import shutil


# 解压.zip格式的文件
def Unzip_Zip_Files(filePath, targetFolder, filename):
    """
    解压.zip格式的文件到目标文件夹。

    Args:
        filePath (str): 压缩文件的路径。
        targetFolder (str): 目标文件夹路径。
        filename (str): 文件名称
    """
    parts = filename.split("_")
    filename = parts[-1]
    # 使用zipfile库打开.zip文件
    with zipfile.ZipFile(filePath, 'r') as zip_ref:
        # 遍历zip文件中的每个文件
        for file_info in zip_ref.infolist():
            # 获取原始文件名
            original_filename = file_info.filename

            # 设定指定名称
            file_extension = os.path.splitext(original_filename)[1]
            encoded_filename = filename + file_extension

            # 构建目标路径
            destination_path = os.path.join(targetFolder, encoded_filename)

            # 解压文件到目标路径
            zip_ref.extract(original_filename, targetFolder)

            # 重命名文件，确保文件名正确
            os.rename(os.path.join(targetFolder, original_filename), destination_path)
