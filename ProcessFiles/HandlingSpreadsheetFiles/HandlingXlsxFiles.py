import pandas as pd


def get_xlsx_files_attributes(filepath, shpName):
    path = "Data\\Admin\\" + filepath + "\\" + shpName + ".xlsx"
    # 读取Excel文件并忽略第一行作为列名
    df = pd.read_excel(path, header=None)

    # 获取第一行的所有内容
    first_row = df.iloc[0].values

    return first_row.tolist()


def get_xlsx_files_data(filepath, shpName):
    path = "Data\\Admin\\" + filepath + "\\" + shpName + ".xlsx"
    # 读取Excel文件并忽略第一行作为列名
    df = pd.read_excel(path, header=None)

    # 排除第一行
    data_dict = df[1:]

    attribute_dict = df[0:1]

    return data_dict.values.tolist(), attribute_dict.values.tolist()
