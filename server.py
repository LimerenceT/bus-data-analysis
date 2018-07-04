from sanic import Sanic
from sanic.response import json, file
from tools.gen_geojson import get_result
from tools.gen_speedjson import get_speedjson
app = Sanic()


@app.route("/")
async def index(request):
    return await file('./map.html')


@app.route('/<choice>/', methods=['POST'])
async def query(request, choice):
    request_data = request.json or {}
    carid = request_data.get('carid', None) or '%'
    start = request_data.get('start_time', None) or '2017/03/13 16:00:00'
    end = request_data.get('end_time', None) or '2017/03/13 20:00:00'
    if choice == 'point':
        return json(get_result(carid, start, end))
    elif choice == 'firebase':
        return json(get_speedjson(carid, start, end))


@app.route("/js/<js>")
async def get_js(request, js):
    return await file('js/{}'.format(js))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
