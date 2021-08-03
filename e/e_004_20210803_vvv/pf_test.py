#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Тестуємо бібліотеку. Дивимось результати
'''
import os, sys, sqlite3, time, calendar
from mylib import *

adr = 'test.db'

if __name__ == '__main__':
  query = 'select pOpen, pHigh, pLow, pClose from d_2010;'
  m1 = sql3_getDataMoreRow(adr, query)
  for i in range(5):
    s = ''
    for y in range(len(m1[i])):
      s += '{:0.05f} | '.format(m1[i][y])
    print(s)

