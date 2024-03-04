import os
import shutil


def copy_models_files(source_folder, destination_folder):
    # 遍历源文件夹中的所有文件
    for file_name in os.listdir(source_folder):
        # 构建文件的完整路径
        file_path = os.path.join(source_folder, file_name)

        # 检查文件是否是普通文件且不以 ".zip" 结尾
        if os.path.isfile(file_path) and not file_name.endswith(".zip"):
            # 构建目标文件的完整路径
            destination_path = os.path.join(destination_folder, file_name)

            # 复制文件
            shutil.copy2(file_path, destination_path)
