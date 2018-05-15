#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert_json

读取数据库，将需要的经纬度写入json文件给百度api描点用
"""
import sqlite3
import geojson

con = sqlite3.connect('bus.db')
c = con.cursor()
result = c.execute(
    "select CARID, LONGITUDE, LATITUDE, GPS_TIME, STANDSPEED, SPEED from bus where GPS_TIME like '2017/03/16 06%' and CARID='12020'").fetchall()
print(len(result))
feature_collection = [geojson.Feature(geometry=geojson.Point(point[1:3]),
                                      properties={"info": "车辆：{carid} \n"
                                                         "经纬度：{latlng}\n"
                                                         "日期：{time}\n"
                                                         "标准速度：{standspeed}\n"
                                                         "速度：{speed}".format(carid=point[0],
                                                                             latlng=point[1:3],
                                                                             time=point[3],
                                                                             standspeed=point[4],
                                                                             speed=point[5])}) for point in result]
feature_collection.append(geojson.Feature(geometry=geojson.LineString([point[1:3] for point in result])))
location = geojson.FeatureCollection(feature_collection)
with open("location.js", 'w', encoding='utf-8') as f:
    f.write(geojson.dumps(location, indent=4))
c.close()
con.close()
