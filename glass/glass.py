import os
import sqlite3

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

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def import_counters():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS counters')
    cursor.execute("""CREATE TABLE counters (id INTEGER PRIMARY KEY, url TEXT,
                        lat REAL, lon REAL, title TEXT)""")
    for counter in counters:
        print("inserting {}".format(counter))
        cursor.execute("""INSERT INTO counters (url, lat, lon, title)
                       VALUES (:url, :lat, :lon, :title)""", counter)
        conn.commit()


def get_counters():
    conn = get_conn()
    c = conn.cursor()
    for row in c.execute('SELECT * from counters'):
        yield row

if __name__ == "__main__":
    print("Counters in DB:")
    for counter in get_counters():
        print("{id}: {url} {title}".format(**counter))
