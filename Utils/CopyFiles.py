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


def copy_swmm_result_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            target_file = os.path.join(destination_folder, file_name)
            if file_name == "infilx.txt" or file_name == "outflow.txt" or file_name == "test1.out" or file_name == "test1.rep":
                shutil.copy(file_path, target_file)


def copy_efdc_result_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            target_file = os.path.join(destination_folder, file_name)
            shutil.copy(file_path, target_file)


