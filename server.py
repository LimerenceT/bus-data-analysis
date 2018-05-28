from sanic import Sanic
from sanic.response import json, file
from tools.gen_geojson import get_result
from tools.stations import get_stations
from tools.gen_speedjson import get_speedjson
app = Sanic()


@app.route("/")
async def test(request):
    return await file('./leaf.html')


@app.route("/<choice>/<carid>/<start>/<end>")
async def tes(request, choice, carid, start, end):
    start = start.replace('%20', ' ').replace('-', '/')
    end = end.replace('%20', ' ').replace('-', '/')
    if choice == 'point':
        return json(get_result(carid, start, end))
    elif choice == 'firebase':
        return json(get_speedjson(carid, start, end))


@app.route("/line/<line>/<num>")
async def line(request, line, num):
    return json(get_stations(line)[int(num)])


@app.route("/js/<js>")
async def line(request, js):
    return await file('js/{}'.format(js))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
