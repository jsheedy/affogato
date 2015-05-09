import json
import random

from flask import Flask, Response
from flask_cors import CORS

import sys
sys.path.append('..')
from glass import glass
from gelato import gelato

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
    data = list(map(dict, glass.get_counter_data(id)))

    response = {
        'counter': counter,
        'data': data
    }
    return Response(json.dumps(response), mimetype='application/json')

@app.route('/counters/<int:id>/data/deseasonalized/')
def counter_data_deseasonalized(id):
    counter_data = list(map(dict, glass.get_counter_data(id)))
    data = gelato.deseasonalize(counter_data)
    list_data = [(str(x[0]),x[1]) for x in data.values.tolist()]
    response = {
        'data': list_data
    }
    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run()