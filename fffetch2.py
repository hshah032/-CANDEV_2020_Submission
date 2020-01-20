import csv
from dataclasses import dataclass
import json
from urllib.request import urlopen


# Constants
NFDB_POINT_FILE = 'data/nfdb_point.csv'
ELEVATION_MAP_FILE = 'data/can3d300'


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

def read_elevation_map():
  with open(ELEVATION_MAP_FILE) as elevation_map_txt:
    altitudes = {}

    lines = elevation_map_txt.readlines()
    ncols = int(lines[0].split(' ')[1])
    nrows = int(lines[1].split(' ')[1])
    xllcenter = float(lines[2].split(' ')[1])
    yllcenter = float(lines[3].split(' ')[1])
    cellsize = float(lines[4].split(' ')[1])
    nodata_value = lines[5].split(' ')[1]

    row = 0
    while row < nrows:
      cols = lines[6 + row].split(' ')
      col = 0
      while col < ncols:
        #if cols[col] == nodata_value:
        #  continue

        altitudes[(round_to_one_decimal(yllcenter + cellsize * row), round_to_one_decimal(xllcenter + cellsize * col))] = int(cols[col])
        col = col + 1
      
      row = row + 1

    return altitudes

def read_nfdb_point(altitudes):
  with open(NFDB_POINT_FILE) as nfdb_point_csv:
    nfdb_point_reader = csv.DictReader(nfdb_point_csv)

    ii = 0
    for row in nfdb_point_reader:
      fire_occurrence = FireOccurrence(float(row['LATITUDE']), float(row['LONGITUDE']))
      fire_occurrence = infer_altitude(fire_occurrence, altitudes)
      ii = ii + 1
      print(ii)
      print(fire_occurrence)
  
    write_altitudes(altitudes)

def infer_altitude(fire_occurrence, altitudes):
  latitude_rounded = round_to_one_decimal(fire_occurrence.latitude)
  longitude_rounded = round_to_one_decimal(fire_occurrence.longitude)
  fire_occurrence.altitude = altitudes[(latitude_rounded, longitude_rounded)]
  return fire_occurrence

def round_to_one_decimal(num):
  return float('{0:.1f}'.format(num))


# Entry point
altitudes = read_elevation_map()
read_nfdb_point(altitudes)
