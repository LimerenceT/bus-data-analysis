from sanic import Sanic
from sanic.response import json, html
from convert_json import get_result
from analysis import get_stations
app = Sanic()


@app.route("/")
async def test(request):
    with open("leaf.html", 'r', encoding='utf-8') as f:
        return html(f.read())


@app.route("/point/<carid>/<start>/<end>")
async def tes(request, carid, start, end):
    start = start.replace('%20', ' ').replace('-', '/')
    end = end.replace('%20', ' ').replace('-', '/')
    return json(get_result(carid, start, end))


@app.route("/line/<line>/<num>")
async def line(request, line, num):
    #先判断数据库有没有，没有先爬虫到数据库，在从数据库取数据
    return json(get_stations(line)[int(num)])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
