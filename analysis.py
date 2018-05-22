from convert_json import get_data
import requests
import geojson


def get_bus_lines(line):
    url = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=500000&geoobj=106.371807%7C29.486379%7C106.731609%7C29.581967&keywords={}'.format(line)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    res = requests.get(url, headers=headers)
    bus_lines = res.json()['data']['busline_list']
    return bus_lines


def gen_geojson(bus_lines):
    lines_geojson = []
    for line in bus_lines:
        feature_collection = []
        points = []
        line_name = line['name']
        stations = line['stations']
        for station in stations:
            station_name = station['name']
            latlng = list(map(float, station['xy_coords'].split(';')))
            points.append(latlng)
            geometry = geojson.Point(tuple(latlng))
            feature_collection.append(geojson.Feature(geometry=geometry,
                                                      properties={"info": "线路：{line_name}<br>"
                                                                          "车站：{station_name}<br>"
                                                                          "经纬度：{latlng}<br>".format(
                                                          line_name=line_name,
                                                          station_name=station_name,
                                                          latlng=latlng)}))

        feature_collection.append(geojson.Feature(geometry=geojson.LineString(points)))
        lines_geojson.append(geojson.FeatureCollection(feature_collection))
    return lines_geojson


def get_stations(line):
    result = get_bus_lines(line)
    return gen_geojson(result)
