import os


def create_user_model_folders(filename):
    # 使用下划线拆分字符串
    parts = filename.split("_")

    folder_path = os.path.join("Data", "Admin")
    # 创建文件夹路径
    folder_path = os.path.join(folder_path, *parts)

    if not os.path.exists(folder_path):
        # 创建文件夹
        os.makedirs(folder_path)

    return folder_path
