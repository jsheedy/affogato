import contextlib
import datetime
import json
import logging
import os
import sqlite3
from six.moves.urllib.request import urlopen

from dateutil import parser


logging.basicConfig(level=logging.INFO)

DB_FILE = os.path.join(os.path.dirname(__file__), 'glass.db')

counters = [
    {'url': 'https://data.seattle.gov/resource/mefu-7eau',
     'lat': 47.562903, 'lon': -122.365474,
     'title': '26th Ave SW Greenway at SW Oregon St',
     'inbound_field': 'north',
     'outbound_field': 'south'},
    {'url': 'https://data.seattle.gov/resource/4qej-qvrz',
     'lat': 47.619760, 'lon': -122.361463,
     'title': 'Elliott Bay Trail in Myrtle Edwards Park',
     'inbound_field': 'bike_south',
     'outbound_field': 'bike_north'},
    {'url': 'https://data.seattle.gov/resource/u38e-ybnc',
     'lat': 47.590466, 'lon': -122.286760,
     'title': 'MTS Trail west of I-90 Bridge',
     'inbound_field': 'bike_north',
     'outbound_field': 'bike_south'},
    {'url': 'https://data.seattle.gov/resource/uh8h-bme7',
     'lat': 47.527991, 'lon': -122.280988,
     'title': 'Chief Sealth Trail North of Thistle',
     'inbound_field': 'bike_north',
     'outbound_field': 'bike_south'},
    {'url': 'https://data.seattle.gov/resource/47yq-6ugv',
     'lat': 47.670921, 'lon': -122.384768,
     'title': 'NW 58th St Greenway at 22nd Ave NW',
     'inbound_field': 'east',
     'outbound_field': 'west'},
    {'url': 'https://data.seattle.gov/resource/2z5v-ecg8',
     'lat': 47.679563, 'lon': -122.265262,
     'title': 'Burke Gilman Trail north of NE 70th St',
     'inbound_field': 'bike_south',
     'outbound_field': 'bike_north'},
    {'url': 'https://data.seattle.gov/resource/3h7e-f49s',
     'lat': 47.673972, 'lon': -122.285791,
     'title': '39th Ave NE Greenway at NE 62nd St',
     'inbound_field': 'south',
     'outbound_field': 'north'},
    {'url': 'https://data.seattle.gov/resource/j4vh-b42a',
     'lat': 47.612966, 'lon': -122.320829,
     'title': 'Broadway Bikeway at Union St',
     'inbound_field': 'nb',
     'outbound_field': 'sb'},
    {'url': 'https://data.seattle.gov/resource/65db-xm6k',
     'lat': 47.647716, 'lon': -122.347391,
     'title': 'Fremont Street Bridge',
     'inbound_field': 'fremont_bridge_sb',
     'outbound_field': 'fremont_bridge_nb'},
    {'url': 'https://data.seattle.gov/resource/upms-nr8w',
     'lat': 47.571353, 'lon': -122.350940,
     'title': 'Spokane Street Bridge',
     'inbound_field': 'east',
     'outbound_field': 'west'}
]

@contextlib.contextmanager
def get_conn():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        logging.critical("Closing with rollback. Error: {}".format(str(e)))
        conn.rollback()
    else:
        conn.commit()
    finally:
        conn.close()

def import_counters():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS counters')
        cursor.execute("""CREATE TABLE counters (id INTEGER PRIMARY KEY,
                                                 url TEXT,
                                                 lat REAL,
                                                 lon REAL,
                                                 inbound_field TEXT,
                                                 outbound_field TEXT,
                                                 title TEXT)"""
                       )
        for counter in counters:
            logging.info("inserting {}".format(counter))
            cursor.execute("""INSERT INTO counters (url, lat, lon,
                           inbound_field, outbound_field, title)
                           VALUES (:url, :lat, :lon, :inbound_field, :outbound_field,
                           :title)""", counter)

def parse_date(date_str):
    return parser.parse(date_str)

def normalize_field_names(dct, counter, last_dct):
    """previous record is passed in as last_dct to fill
    in missing dates"""

    logging.debug('parsing ' + str(dct))
    translation_map = {
        counter['inbound_field']: 'inbound',
        counter['outbound_field']: 'outbound'
    }

    for k,v in list(dct.items()):
        if k in translation_map:
            dct[translation_map[k]] = int(float(v))
            del dct[k]

        if 'total' in k:
            dct['total'] = v
            del dct[k]

    dct['id'] = counter['id']
    try:
        dct['date'] = parse_date(dct['date'])
    except KeyError as e:
        logging.warn("record didn't contain a date?")
        if last_dct and 'date' in last_dct:
            faked_date = last_dct['date'] + datetime.timedelta(hours=1)
            logging.warn("Attempting to fill in previous date ({}) + 1 hour ({})".format(last_dct['date'], faked_date))
            dct['date'] = faked_date

    required_params = ('inbound', 'outbound')
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
        url = counter['url'] + '.json' + '?$limit=50000'
        raw_data = urlopen(url).read().decode('utf-8')
        with open(cached, 'w') as f:
            f.write(raw_data)
    finally:
        return raw_data

def import_counter_data(counter):
    raw_data = cache_counter_response(counter)
    def data():
        dct = {}
        for record in json.loads(raw_data):
            dct = normalize_field_names(record, counter, dct)
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
            inbound INTEGER,
            outbound INTEGER,
            FOREIGN KEY(counter_id) REFERENCES counters(id),
            UNIQUE(counter_id, datetime)
            )
            """)

        insert_query = """INSERT OR IGNORE INTO raw(counter_id, datetime, inbound, outbound)
            VALUES(:id, :date, :inbound, :outbound)"""

        cursor.executemany(insert_query, data())

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
            SELECT counter_id,
            datetime,
            inbound,
            outbound
            FROM raw
            {WHERE}
            ORDER BY counter_id, datetime""".format(**{'WHERE': WHERE })
        c.execute(query, {'id':id})
        data = (dict(x) for x in c)
        yield from data

def get_aggregated_counter_data(id=None, aggregate='daily'):
    with get_conn() as conn:
        c = conn.cursor()
        if id:
            WHERE = "WHERE counter_id = :id"
        else:
            WHERE = ""

        if aggregate == 'daily':
            AGGREGATE = "GROUP BY DATE(datetime)"
        elif aggregate == 'weekly':
            AGGREGATE = "GROUP BY STRFTIME('%W', datetime)"

        query = """
            SELECT
            counter_id,
            MAX(DATE(datetime)) as datetime,
            sum(inbound) as inbound,
            sum(outbound) as outbound
            FROM raw
            {WHERE}
            {AGGREGATE}
            ORDER BY datetime""".format(**{'WHERE': WHERE, 'AGGREGATE': AGGREGATE})

        c.execute(query, {'id':id})
        data = (dict(x) for x in c)
        yield from data


if __name__ == "__main__":
    import_counters()
    for counter in list(get_counters()):
        logging.info("{id}: {url} {title}".format(**counter))
        import_counter_data(counter)
