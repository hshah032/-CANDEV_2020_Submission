import math
import csv
from dataclasses import dataclass
import json
from urllib.request import urlopen


# Constants
NFDB_POINT_FILE = 'data/nfdb_point.csv'




def c_m0(_F0):
  return 147.2 * (101 - _F0) / (59.5 + _F0)

def c_rf(_r0):
  if _r0 > 0.5:
    return _r0 - 0.5
  else:
    return _r0

def c_mr(_m0, _rf):
  if _m0 <= 150:
    return _m0 + 42.5 * _rf * (pow(math.e, -100/(251-_m0))) * (1 - pow(math.e, -6.93/_rf))
  else:
    return _m0 + 42.5 * _rf * (pow(math.e, -100/(251-_m0))) * (1 - pow(math.e, -6.93/_rf)) + 0.0015 * pow(_m0 - 150, 2) * pow(_rf, 0.5)

def c_Ed(_H, _T):
  return 0.942 * pow(_H, 0.679) + 11 * pow(math.e, (_H - 100) / 10) + 0.18 * (21.1 - _T) * (1 - pow(math.e, -0.115 * _H))

def c_Ew(_H, _T):
  return 0.618 * pow(_H, 0.753) + 10 * pow(math.e, (_H - 100) / 10) + 0.18 * (21.1 - _T) * (1 - pow(math.e, -0.115 * _H))

def c_k0(_H, _W):
  return 0.424 * (1 - pow(_H/100, 1.7)) + 0.0694 * pow(_W, 0.5) * (1 - pow(_H/100, 8))

def c_kd(_k0, _T):
  return _k0 * 0.581 * pow(math.e, 0.0365 * _T)

def c_k1(_H, _W):
  return 0.424 * (1 - pow((100-_H)/100, 1.7)) + 0.0694 * pow(_W, 0.5) * (1 - pow((100-_H)/100, 8))

def c_kw(_k1, _T):
  return _k1 * 0.581 * pow(math.e, 0.0365 * _T)

def c_m_8(_Ed, _m0, _kd):
  return _Ed + (_m0 - _Ed) * pow(10, -_kd)

def c_m_9(_Ew, _m0, _kw):
  return _Ew - (_Ew - _m0) * pow(10, -_kw)

def c_F(_m):
  return 59.5 * (250 - _m)/(147.2 + _m)


def FFMC(_F0, _r0, _H, _T, _W):
  _m0 = c_m0(_F0)
  _m = _m0
  _rf = c_rf(_m0)
  _mr = c_mr(_m0, _rf)
  _Ed = c_Ed(_H, _T)

  if _m0 > _Ed:
    _kd = c_kd(c_k0(_H, _W), _T)
    _m = c_m_8(_Ed, _m0, _kd)

  if _m0 < _Ed:
    _Ew = c_Ew(_H, _T)
    if _m0 < _Ew:
      _kw = c_kw(c_k1(_H, _W), _T)
      _m = c_m_9(_Ew, _m0, _kw)

  #if Ed >= m0 and m0 >= Ew:
  #  m = m0

  return c_F(_m)


def read_nfdb_point():
  x = []

  with open(NFDB_POINT_FILE) as nfdb_point_csv:
    nfdb_point_reader = csv.DictReader(nfdb_point_csv)

    for row in nfdb_point_reader:
      ffmc = FFMC(row['FFMC'])