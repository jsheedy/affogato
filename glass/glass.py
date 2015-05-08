import contextlib
import json
import logging
import os
import sqlite3
from six.moves.urllib.request import urlopen

from dateutil import parser


logging.basicConfig(level=logging.INFO)

DB_FILE = os.path.join(os.path.dirname(__file__), 'glass.db')

counters = [
    {'url': 'https://data.seattle.gov/resource/mefu-7eau.json',
     'lat': 47.562903, 'lon': -122.365474,
     'title': '26th Ave SW Greenway at SW Oregon St'},
    {'url': 'https://data.seattle.gov/resource/4qej-qvrz.json',
     'lat': 47.619760, 'lon': -122.361463,
     'title': 'Elliott Bay Trail in Myrtle Edwards Park'},
    {'url': 'https://data.seattle.gov/resource/u38e-ybnc.json',
     'lat': 47.590466, 'lon': -122.286760,
     'title': 'MTS Trail west of I-90 Bridge'},
    {'url': 'https://data.seattle.gov/resource/uh8h-bme7.json',
     'lat': 47.527991, 'lon': -122.280988,
     'title': 'Chief Sealth Trail North of Thistle'},
    {'url': 'https://data.seattle.gov/resource/47yq-6ugv.json',
     'lat': 47.670921, 'lon': -122.384768,
     'title': 'NW 58th St Greenway at 22nd Ave NW'},
    {'url': 'https://data.seattle.gov/resource/2z5v-ecg8.json',
     'lat': 47.679563, 'lon': -122.265262,
     'title': 'Burke Gilman Trail north of NE 70th St'},
    {'url': 'https://data.seattle.gov/resource/3h7e-f49s.json',
     'lat': 47.673972, 'lon': -122.285791,
     'title': '39th Ave NE Greenway at NE 62nd St'},
    {'url': 'https://data.seattle.gov/resource/j4vh-b42a.json',
     'lat': 47.612966, 'lon': -122.320829,
     'title': 'Broadway Bikeway at Union St'},
    {'url': 'https://data.seattle.gov/resource/65db-xm6k.json',
     'lat': 47.647716, 'lon': -122.347391,
     'title': 'Fremont Street Bridge'},
    {'url': 'https://data.seattle.gov/resource/upms-nr8w.json',
     'lat': 47.571353, 'lon': -122.350940,
     'title': 'Spokane Street Bridge'}
]

@contextlib.contextmanager
def get_conn():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        yield conn
    except:
        conn.rollback()
    else:
        conn.commit()
    finally:
        conn.close()

def import_counters():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS counters')
        cursor.execute("""CREATE TABLE counters (id INTEGER PRIMARY KEY, url TEXT,
                                                 lat REAL, lon REAL, title TEXT)"""
                       )
        for counter in counters:
            logging.info("inserting {}".format(counter))
            cursor.execute("""INSERT INTO counters (url, lat, lon, title)
                           VALUES (:url, :lat, :lon, :title)""", counter)

def normalize_field_names(dct, counter):
    logging.debug('parsing ' + str(dct))
    translation_map = {
        'north': 'bike_north',
        'nb': 'bike_north',
        'south': 'bike_south',
        'sb': 'bike_south',
        'east': 'bike_east',
        'west': 'bike_west',
        'fremont_bridge_nb': 'bike_north',
        'fremont_bridge_sb': 'bike_south',
    }

    for k,v in list(dct.items()):
        if k in translation_map:
            dct[translation_map[k]] = int(v)
            del dct[k]

        if 'total' in k:
            dct['total'] = v
            del dct[k]

    dct['id'] = counter['id']
    try:
        dct['date'] = parser.parse(dct['date'])
    except KeyError as e:
        logging.warn("record didn't contain a date? error: {}".format(e))
        return None
    required_params = ('bike_north', 'bike_south', 'bike_west', 'bike_east')
    for p in required_params:
        if not p in dct:
            dct[p] = None

    logging.debug(dct)
    return dct

def cache_counter_response(counter):
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    cached = os.path.join(cache_dir, str(counter['id']) + '.json')
    try:
        with open(cached) as f:
            logging.info("found cached API response")
            raw_data = f.read()
    except Exception as e:
        logging.info("caching API response")
        url = counter['url'] + '?$limit=50000'
        raw_data = urlopen(url).read().decode('utf-8')
        with open(cached, 'w') as f:
            f.write(raw_data)
    finally:
        return raw_data

def import_counter_data(counter):
    raw_data = cache_counter_response(counter)
    def data():
        for record in json.loads(raw_data):
            dct = normalize_field_names(record, counter)
            if dct:
                yield dct

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counter_id INTEGER,
            datetime INTEGER,
            bike_north INTEGER,
            bike_south INTEGER,
            bike_east INTEGER,
            bike_west INTEGER,
            FOREIGN KEY(counter_id) REFERENCES counters(id),
            UNIQUE(counter_id, datetime)
            )
            """)

        cursor.executemany("""INSERT OR IGNORE INTO raw(counter_id, datetime, bike_north, bike_south, bike_east, bike_west)
            VALUES(:id, :date, :bike_north, :bike_south, :bike_east, :bike_west)""",
            data()
            )

def get_counters():
    with get_conn() as conn:
        c = conn.cursor()
        for row in c.execute('SELECT * from counters'):
            yield row

def get_counter(id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * from counters where id=:id', {'id':id})
        return c.fetchone()

def get_counter_data(id=None):
    with get_conn() as conn:
        c = conn.cursor()
        if id:
            WHERE = "WHERE counter_id = :id"
        else:
            WHERE = ""

        query = """
            SELECT datetime,
            bike_north,
            bike_south,
            bike_east,
            bike_west
            FROM raw
            {WHERE}
            ORDER BY counter_id, datetime""".format(**{'WHERE': WHERE })
        c.execute(query, {'id':id})
        data = [dict(x) for x in c]
        return data

def get_daily_counter_data(id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT DATE(datetime) as datetime,
            sum(bike_north) as bike_north,
            sum(bike_south) as bike_south,
            sum(bike_east) as bike_east,
            sum(bike_west) as bike_west
            FROM raw
            WHERE counter_id=:id
            GROUP BY datetime
            ORDER BY datetime""", {'id':id})
        return c.fetchall()


if __name__ == "__main__":
    import_counters()
    for counter in list(get_counters()):
        logging.info("{id}: {url} {title}".format(**counter))
        import_counter_data(counter)
