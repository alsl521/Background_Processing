from pyproj import CRS


# 根据shp的“.prj文件”获取 EPSG 代码
def get_epsg_from_prj(prj_file_path):
    """
    从Shapefile的.prj文件中解析坐标参考系统（CRS）并获取EPSG代码。

    参数：
    prj_file_path (str): 包含坐标参考系统信息的.prj文件的路径。

    返回：
    int or None: 成功获取EPSG代码时返回EPSG代码（整数），否则返回None。

    注意：
    如果.prj文件中未找到EPSG代码，将打印错误消息并返回None。
    如果读取.prj文件时发生错误，将打印错误消息并返回None。
    """
    try:
        # 打开.prj文件并读取内容
        with open(prj_file_path, 'r') as prj_file:
            prj_content = prj_file.read()

            # 从字符串中创建坐标参考系统对象
            crs = CRS.from_string(prj_content)

            # 获取EPSG代码
            epsg_code = crs.to_epsg()

            # 检查EPSG代码是否成功获取
            if epsg_code is not None:
                return epsg_code
            else:
                print("EPSG code not found in the .prj file.")
                return None
    except Exception as e:
        # 处理异常情况
        print(f"Error reading .prj file: {e}")
        return None


def get_Shp_Field_Attributes(layer):
    """
        获取Shapefile图层的属性字段信息。

        Args:
            layer (ogr.Layer): Shapefile图层对象。

        Returns:
            list: 属性字段信息列表。
    """

    attribute_info_list = []  # 用于存储属性字段信息的列表

    # 获取图层的属性定义
    layer_definition = layer.GetLayerDefn()

    # 获取属性字段的数量
    num_fields = layer_definition.GetFieldCount()

    # 输出属性字段的名称
    for i in range(num_fields):
        field_definition = layer_definition.GetFieldDefn(i)

        # 如果表中存在ID字段，则将其跳过
        if field_definition.GetName().upper() == 'ID':
            continue

        field_info = {
            'name': field_definition.GetName(),
            'type': field_definition.GetTypeName(),
            'width': field_definition.GetWidth(),
            'precision': field_definition.GetPrecision()
        }

        # 将当前属性字段信息字典添加到列表中
        attribute_info_list.append(field_info)

    return attribute_info_list
