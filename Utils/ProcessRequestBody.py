import json


def get_same_attributes_from_request_body(request_body):
    # 解码请求的原始数据
    body_unicode = request_body.decode('utf-8')
    # 将数据解析为 JSON 对象
    body_data = json.loads(body_unicode)
    # 分类数据
    shp_data = {}
    observation_data = {}

    for key, value in body_data.items():
        if key.startswith("shp_"):
            shp_key = key.replace("shp_", "")
            shp_data[shp_key] = value
        elif key.startswith("observation_"):
            observation_key = key.replace("observation_", "")
            observation_data[observation_key] = value

    return shp_data, observation_data
