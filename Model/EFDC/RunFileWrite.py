import shutil
import subprocess


def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print("文件复制成功！")
    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
    except IOError:
        print("发生了输入输出错误。")


def run_program(program_path):
    try:
        command = [program_path]
        subprocess.run(command, check=True)
        print("程序运行完成！")
    except FileNotFoundError:
        print("程序文件未找到，请检查路径是否正确。")
    except subprocess.CalledProcessError:
        print("程序运行出错。")


def get_first_occurrence_indices(arr):
    first_occurrence_indices = {}
    for i, element in enumerate(arr):
        if element not in first_occurrence_indices:
            first_occurrence_indices[element] = i
    return first_occurrence_indices
