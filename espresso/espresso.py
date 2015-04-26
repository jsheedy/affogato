from flask import Flask

from models import Detectors

app = Flask(__name__)



@app.route('/detectors')
def detectors():
	detectors
    return '[]'

if __name__ == '__main__':
    app.run()