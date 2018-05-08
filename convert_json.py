#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert_json

读取数据库，将需要的经纬度写入json文件给百度api描点用
"""
import sqlite3
import json

con = sqlite3.connect('bus.db')
c = con.cursor()
result = c.execute("select LONGITUDE, LATITUDE from bus where GPS_TIME like '2017/03/01%'").fetchall()
location = {'data': list(map(list, result))}
with open("location.js", 'w') as f:
    json.dump(location, f)
c.close()
con.close()

