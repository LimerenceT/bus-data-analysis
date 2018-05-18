from sanic import Sanic
from sanic.response import json, html
import json as js
from convert_json import get_result
app = Sanic()


@app.route("/")
async def test(request):
    with open("leaf.html", 'r', encoding='utf-8') as f:
        return html(f.read())


@app.route("/<carid>/<start>/<end>")
async def tes(request, carid, start, end):
    start = start.replace('%20', ' ').replace('-', '/')
    end = end.replace('%20', ' ').replace('-', '/')
    return json(get_result(carid, start, end))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
