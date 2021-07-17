#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Тестовий приклад із кореляції Спірмена
'''

from lib_correlation import *
from mylib import *

adr = 'e_003_20210716_tst.db'
num_bars = 20

def prepareData(a, num_bars):
  '''Формуємо масив у num_bars барів'''
  ret = []
  for i in range(len(a) - num_bars):
    ret.append(a[i:(i + num_bars)])
  return ret

def getDataFromDB(year=2010):
  '''Забираємо усі дані у звичайному вигляді'''
  a_n = []
  a_r = []
  query = 'select pTime, pOpen, pHigh, pLow, pClose from d_{year};'.format(year)
  ret = sql3_getDataMoreRow(adr, query)
  for i in range(len(ret)):
    a_n.append(ret[i][0])
    a_r.append((ret[i][1] + ret[i][2] + ret[i][3] + ret[i][4])/4.0)
  return a_n, a_r


if __name__ == '__main__':
  a_n, a_r = getDataFromDB()
  tmp = prepareData(a_r, num_bars)

