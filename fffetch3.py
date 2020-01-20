import csv
from dataclasses import dataclass
import json
from urllib.request import urlopen


# Constants
NFDB_POINT_FILE = 'data/nfdb_point.csv'
ALTITUDES_FILE = 'data/altitudes.csv'


# Globals
altitudes = {}


# Dataclasses
@dataclass
class FireOccurrence:
  latitude: float
  longitude: float
  altitude: float = 0.0


# Functions
def download_utf8(url):
  opened = urlopen(url)
  return opened.read().decode('utf-8')

def read_nfdb_point():
  with open(NFDB_POINT_FILE) as nfdb_point_csv:
    nfdb_point_reader = csv.DictReader(nfdb_point_csv)

    ii = 0
    for row in nfdb_point_reader:
      fire_occurrence = FireOccurrence(float(row['LATITUDE']), float(row['LONGITUDE']))
      fire_occurrence.altitude = infer_altitude(fire_occurrence)
      ii = ii + 1
      if ii % 100 == 0:
        print(ii)

def write_altitudes(altitudes):
  with open(ALTITUDES_FILE, 'w', newline='') as altitudes_csv:  
    altitudes_writer = csv.writer(altitudes_csv)
    altitudes_writer.writerow(["LATITUDE", "LONGITUDE", "ALTITUDE"])
    for (latitude, longitude), altitude in altitudes.items():
       altitudes_writer.writerow([latitude, longitude, altitude])

def infer_altitude(fire_occurrence):
  latitude_str = '{0:.1f}'.format(fire_occurrence.latitude)
  longitude_str = '{0:.1f}'.format(fire_occurrence.longitude)

  dict_key = (latitude_str, longitude_str)
  if dict_key in altitudes:
    return altitudes[dict_key]

  json_str = download_utf8(f'http://geogratis.gc.ca/services/elevation/cdem/altitude?lat={latitude_str}&lon={longitude_str}')
  altitude = json.loads(json_str)['altitude']

  altitudes[dict_key] = altitude
  return altitude


# Entry point
try:
  read_altitudes()
  read_nfdb_point()
  write_altitudes()
except:
  write_altitudes()