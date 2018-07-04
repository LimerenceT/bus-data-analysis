#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
geo_geojson

读取数据库，将需要的经纬度生成geojson传给前端渲染
"""
import sqlite3
import geojson

DATABASE = 'db/bus.db'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_data(sql: str) -> list:
    """返回database中需要的数据"""
    con = sqlite3.connect(DATABASE)
    # apply the function to the sqlite3 engine
    con.row_factory = dict_factory
    print(sql)
    data = con.execute(sql).fetchall()
    print(len(data))
    con.close()
    return data


def gen_sql(carid: str, start: str, end: str) -> str:
    sql = ("select CARID, LONGITUDE, LATITUDE, GPS_TIME, STANDSPEED, SPEED, DEF1, ACTIVE from bus "
           "where GPS_TIME>'{start}' and GPS_TIME <'{end}' "
           "and CARID like '{carid}' "
           "order by GPS_TIME").format(start=start, end=end, carid=carid)
    return sql


def gen(result: list) -> geojson:
    """将result每一项生成对应feature，然后组成一个feature的集合并返回"""
    feature_collection = []
    points = []
    for point in result:
        if not point["LONGITUDE"]:
            continue

        geometry = geojson.Point((point["LONGITUDE"], point["LATITUDE"]))
        points.append([point["LATITUDE"], point["LONGITUDE"]])
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
                                                                                          active=point["ACTIVE"]),
                                                              "line": point["DEF1"],
                                                              }))

    feature_collection.append(geojson.Feature(geometry=geojson.LineString(points)))
    return feature_collection


def get_result(carid: str, start: str, end: str) -> dict:
    """根据开始结束日期，返回相应的结果"""
    sql = gen_sql(carid,  start, end)
    data = get_data(sql)
    feature_collection = gen(data)
    location = geojson.FeatureCollection(feature_collection)
    return location
