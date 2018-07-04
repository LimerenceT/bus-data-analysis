from .gen_geojson import get_data, gen_sql

"""
geo_speedjson

读取数据库，提取每一条数据的速度信息，生成和speed属性相关的geojson传给前端渲染
"""


def gen(data: list):
    result = []
    for point in data:
        if not point["LONGITUDE"]:
            continue
        intensity = 1 - point["SPEED"]/60
        result.append([point["LATITUDE"], point["LONGITUDE"], intensity])
    return result


def get_speedjson(carid: str, start: str, end: str):
    sql = gen_sql(carid, start, end)
    data = get_data(sql)
    return gen(data)
