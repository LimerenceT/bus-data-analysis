from tools.gen_geojson import get_data, gen_sql
from math import radians, cos, sin, asin, sqrt

"""分析一天的往返次数,每天跑几个来回"""


def haversine(latlng1: tuple, latlng2: tuple) -> float:  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    (lon1, lat1), (lon2, lat2) = latlng1, latlng2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def get_times(carid: str) -> list:
    sql = gen_sql(carid, "2017/03/16 00:01:00", "2017/03/16 23:59:00")
    data = get_data(sql)
    go = True
    times = []
    for point in data:
        latlng = (point['LONGITUDE'], point['LATITUDE'])
        if latlng == (0.0, 0.0):
            continue
        end_latlng = (106.53072, 29.63871)
        distance = haversine(latlng, end_latlng)
        if distance <= 10:
            if go:
                times.append(point["GPS_TIME"])
                go = False
            else:
                continue
        else:
            go = True
    return times
