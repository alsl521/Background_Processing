from django.http import JsonResponse

# 自定义方法
from Utils.DeleteFiles import delete_folder_contents_only
from Utils.Result import Result
from DatabasContent.GetMenuFromTable import get_menu_from_table
from ProcessFiles.HandlingCompressedFiles.HandlingCompressedFiles import handling_compressed_files
from ProcessFiles.HandlingSpreadsheetFiles.HandlingSpreadsheetFiles import handling_spreadsheet_files


# Create your views here.
# 返回已选择模型的菜单
def selectModels(request):
    """
    根据请求中的POST数据，选择模型并返回JSON响应。

    Args:
        request: Django的HttpRequest对象，包含请求信息和数据。

    Returns:
        JsonResponse: 包含选择的模型信息的JSON响应。

    """
    reqDict = request.POST.dict()  # 将POST数据转换为字典形式
    data = []
    # 遍历POST数据字典
    for key, value in reqDict.items():
        submenu_dict = {
            "index": value,
            "menu_name": value,
            "sub_menu_name": get_menu_from_table(value),  # 从表中获取菜单名称
            "upload_file_type": None,
        }
        data.append(submenu_dict)
    # 构造JSON响应并返回
    return JsonResponse(Result.success(data=data).to_dict())


# 上传数据
def upLoadFiles(request):
    """
        处理文件上传请求并返回JSON响应。

        Args:
            request: Django的HttpRequest对象，包含请求信息和数据。

        Returns:
            JsonResponse: 包含处理结果的JSON响应。

        """

    # ==============================
    # 获取数据
    # 获取非文件数据
    reqDict = request.POST.dict()
    ModelName = reqDict["ModelName"]  # 模型名称
    MenuName = reqDict["MenuName"]  # 菜单名称
    fileType = reqDict["fileType"]  # 文件类型

    # 删除无用数据
    delete_folder_contents_only("TemporaryFolder")  # 清空临时文件夹内容

    # 上传类型为压缩格式的shp文件
    if fileType == '1':
        file = request.FILES.get("file")  # 获取上传的文件
        table_name = handling_compressed_files("TemporaryFolder", ModelName, MenuName, file)  # 处理压缩文件
        data = {'type': '1', 'url': "http://localhost:8081/geoserver/test/wms", 'name': table_name}
        return JsonResponse(Result.success(data=data).to_dict())
    elif fileType == '2':
        file = request.FILES.get("file")  # 获取上传的文件
        table_name = handling_spreadsheet_files("TemporaryFolder", ModelName, MenuName, file)  # 处理文本文件
        data = {'type': '2'}
        return JsonResponse(Result.success(data=data).to_dict())
    elif fileType == '3':
        print("33")

    # 返回默认响应
    return JsonResponse(Result.success().to_dict())
