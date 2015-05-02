import json
import random

from flask import Flask, Response
from flask_cors import CORS

import sys
sys.path.append('..')
from glass import glass

app = Flask(__name__)
cors = CORS(app)


def feature_collection(objects):
    """returns a GeoJSON feature collection of all objects"""
    features = []
    features = (
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [o['lon'], o['lat']]
            },
            "properties": {
                "title": o['title'],
                "id": o['id'],
                "url": o['url'],
            }
        }
        for o in objects)

    fc = {
        'type': 'FeatureCollection',
        'features': list(features)
    }
    return fc

@app.route('/counters/')
def counters():

    counters = map(dict, glass.get_counters())
    fc = feature_collection(counters)
    return Response(json.dumps(fc), mimetype='application/json')

@app.route('/counters/<int:id>/data/')
def counter_data(id):
    counter = dict(glass.get_counter(id))
    data = list(map(dict, glass.get_daily_counter_data(id)))

    response = {
        'counter': counter,
        'data': data
    }
    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run()