import json

from flask import Flask, Response

import sys
sys.path.append('..')
from glass import glass

app = Flask(__name__)


@app.route('/counters/')
def counters():
    counters = map(dict, glass.get_counters())
    return Response(json.dumps(list(counters)), mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run()