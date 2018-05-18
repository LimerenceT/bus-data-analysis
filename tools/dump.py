#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tool.dump

用于将xls文件中的数据存入到数据库中
"""

import os
import datetime
import sqlite3
import xlrd
from xlrd import xldate_as_tuple

con = sqlite3.connect('bus.db')
c = con.cursor()

for filename in os.listdir("./track/"):
    bus = xlrd.open_workbook(os.path.join('./track/', filename))
    sheet = bus.sheet_by_index(0)
    for row in range(1, sheet.nrows):
        row_val = sheet.row_values(row)
        row_val[6] = datetime.datetime(*xldate_as_tuple(row_val[6], 0)).strftime('%Y/%m/%d %H:%M:%S')
        c.execute("insert into bus values {}".format(tuple([val for val in row_val])))
c.close()
con.commit()
con.close()
