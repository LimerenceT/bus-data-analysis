from .gen_geojson import get_data, gen_sql


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
