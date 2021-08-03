#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Тестовий приклад із кореляції Спірмена
'''
import time, sys
from lib_correlation import *
from mylib import *
from numba import njit

adr = 'e_003_20210716_tst.db'
YEAR = 2010
n_t = f'experiment_03_{YEAR}_003'
num_bars = 20
min_pearson = 0.95

def getNormalizeDataRow(data):
  '''Нормалізація даних масиву на проміжку [0.0;1.0] по рядках
  Використовувати для однорідних даних по рядках.'''
  ret = []
  for y in range(len(data)):
    __min = min(data[y])
    __max = max(data[y])
    __height = __max - __min
    ret2 = []
    for x in range(len(data[y])):
      if __height == 0.0:
        ret2.append(0.5)
        continue
      elif data[y][x] == __min:
        ret2.append(0.0)
        continue
      else:
        ret2.append((data[y][x] - __min) / __height)
    ret.append(ret2)
  return ret

def sendData(name_table, data):
  '''Відправка даних у таблицю'''
  query = f'insert or ignore into {name_table} (d_original, d_copy, t_original, t_copy, pearson) values (?,?,?,?,?);'
  send = []
  for i in range(len(data)):
    tmp = []
    tmp.append(convert_UNIX2Human(data[i][0]))
    tmp.append(convert_UNIX2Human(data[i][1]))
    tmp.append(data[i][0])
    tmp.append(data[i][1])
    tmp.append(data[i][2])
    send.append(tuple(tmp))
  sql3_sendData(adr, query, send)

def createTable(name_table):
  '''Видалення та вставка нової таблиці, куди підуть наші дані'''
  query = f'drop table if exists {name_table};'
  sql3_executeQuery(adr, query)
  query = f'create table if not exists {name_table} (d_original text, d_copy text, t_original text, t_copy text, pearson real);'
  sql3_executeQuery(adr, query)

def prepareData_v2(a, num_bars):
  '''Формуємо масив у num_bars барів'''
  ret = []
  for i in range(len(a) - num_bars):
    tmp = []
    for n in range(i, (i + num_bars)):
      for y in range(len(a[i])):
        tmp.append(a[n][y])
    ret.append(tmp)
  return ret

def prepareData(a, num_bars):
  '''Формуємо масив у num_bars барів'''
  ret = []
  for i in range(len(a) - num_bars):
    ret.append(a[i:(i + num_bars)])
  return ret

def getDataFromDB_v2(year=2010):
  '''Забираємо усі дані у звичайному вигляді'''
  a_n = []
  a_r = []
  query = 'select pTime, pOpen, pHigh, pLow, pClose from d_{};'.format(year)
  ret = sql3_getDataMoreRow(adr, query)
  for i in range(len(ret)):
    tmp = []
    a_n.append(ret[i][0])
    tmp.append(ret[i][1])
    tmp.append(ret[i][2])
    tmp.append(ret[i][3])
    tmp.append(ret[i][4])
    a_r.append(tmp)
  return a_n, a_r

def getDataFromDB(year=2010):
  '''Забираємо усі дані у звичайному вигляді'''
  a_n = []
  a_r = []
  query = 'select pTime, pOpen, pHigh, pLow, pClose from d_{};'.format(year)
  ret = sql3_getDataMoreRow(adr, query)
  for i in range(len(ret)):
    a_n.append(ret[i][0])
    a_r.append((ret[i][1] + ret[i][2] + ret[i][3] + ret[i][4])/4.0)
  return a_n, a_r

if __name__ == '__main__':
  # a_n, a_r = getDataFromDB(YEAR)
  a_n, a_r = getDataFromDB_v2(YEAR)
  print('len a_n -> {}'.format(len(a_n)))
  ret = prepareData_v2(a_r, num_bars)
  print('len ret -> {}'.format(len(ret)))
  ret = getNormalizeDataRow(ret)

  all_result = []
  t1 = time.time()
  cnt_all = 0
  cnt_a = 0
  for i in range(len(ret) - 1):
    t_start = time.time()
    for y in range(i + 1, len(ret)):
      tmp = []
      pirson = getCorrelationPearson(ret[i], ret[y])
      if min_pearson < pirson:
        tmp.append(a_n[i])
        tmp.append(a_n[y])
        tmp.append(pirson)
        all_result.append(tmp)
        cnt_a += 1
      cnt_all += 1
    t_end = time.time()
    print('#{} {} -> {:0.03f} сек. Вже знайдено {} серед {}'.format(i, convert_UNIX2Human(a_n[i]), (t_end - t_start), cnt_a, cnt_all))
  t2 = time.time()
  print('length all_result => {}'.format(len(all_result)))
  print('Обробка тривала {:0.03f} сек.'.format((t2-t1)))
  print('З усіх випадків {} кореляцію пройшли {}. Показник кореляції склав {:0.3f}'.format(cnt_all, cnt_a, min_pearson))
  createTable(n_t)
  # Виводимо дані на екран
  sendData(n_t, all_result)
