#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert_json

读取数据库，将需要的经纬度写入json文件给谷歌地图api描点用
"""
import sqlite3
import geojson


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(carid: str, start: str, end: str) -> list:
    """返回database中需要的数据"""
    con = sqlite3.connect('bus.db')
    # apply the function to the sqlite3 engine
    con.row_factory = dict_factory
    sql = ("select CARID, LONGITUDE, LATITUDE, GPS_TIME, STANDSPEED, SPEED, DEF1, ACTIVE from bus "
           "where GPS_TIME>'{start}' and GPS_TIME <'{end}' "
           "and CARID='{carid}' "
           "order by GPS_TIME").format(start=start, end=end, carid=carid)
    print(sql)
    data = con.execute(sql).fetchall()
    print(len(data))
    con.close()
    return data


def gen(result: list) -> geojson:
    """将result每一项生成对应feature，然后组成一个feature的集合并返回"""
    feature_collection = []
    points = []
    for point in result:
        if not point["LONGITUDE"]:
            continue
        geometry = geojson.Point((point["LONGITUDE"], point["LATITUDE"]))
        points.append([point["LONGITUDE"], point["LATITUDE"]])
        feature_collection.append(geojson.Feature(geometry=geometry,
                                                  properties={"info": "车辆：{carid}<br>"
                                                                      "线路：{def1}<br>"
                                                                      "经纬度：{latlng}<br>"
                                                                      "active：{active}<br>"
                                                                      "日期：{time}<br>"
                                                                      "标准速度：{standspeed}<br>"
                                                                      "速度：{speed}".format(carid=point["CARID"],
                                                                                          def1=point["DEF1"],
                                                                                          latlng=(point["LONGITUDE"], point["LATITUDE"]),
                                                                                          time=point["GPS_TIME"],
                                                                                          standspeed=point["STANDSPEED"],
                                                                                          speed=point["SPEED"],
                                                                                          active=point["ACTIVE"])}))

    feature_collection.append(geojson.Feature(geometry=geojson.LineString(points)))
    return feature_collection


def get_result(carid: str, start: str, end: str) -> dict:
    """根据开始结束日期，返回相应的结果"""
    data = get_data(carid, start, end)
    feature_collection = gen(data)
    location = geojson.FeatureCollection(feature_collection)
    return location
