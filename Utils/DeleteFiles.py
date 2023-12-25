import os
import shutil


def delete_folder_contents_only(folder_path):
    """
    删除文件夹中的所有文件，但保留文件夹本身。

    Args:
        folder_path (str): 文件夹路径。

    """
    # 删除文件夹中的所有文件，但保留文件夹本身
    for file_name in os.listdir(folder_path):

        # 获取需要删除的路径
        file_path = os.path.join(folder_path, file_name)
        try:

            # 如果是文件，直接删除
            if os.path.isfile(file_path):
                os.unlink(file_path)

                # 如果是子文件夹，递归删除
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
