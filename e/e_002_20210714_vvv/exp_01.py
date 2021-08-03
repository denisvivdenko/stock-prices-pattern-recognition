#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Опис файлу
'''
import os, sys, sqlite3, time, calendar
import numpy as np
from math import *
from mylib import *
from PIL import Image

adr = '1.db'
num_train_candle = 30
num_boxes = 50
min_height = 0.02

def prepare(data, num_box, num_candle):
  '''Готує матрицю для малювання графіку'''
  print('Починаємо працювати над створенням малюнків')
  work_dir = os.getcwd() + os.sep + 'graph'
  if os.path.exists(work_dir) == False:
    os.mkdir(work_dir)
    print('Створили папку для малюнків')
  os.chdir(work_dir)
  ret = []
  print('Перейшли у папку для малюнків і починаємо циклічно оброблювати дані')
  for i in range(len(data)):
    zero_array = [[[255, 255, 255] for e in range(num_candle)] for w in range(num_box)]
    for m in range(num_candle):
      # читаємо по стовпцях
      tmp_min = data[i][m * 2]
      tmp_max = data[i][m * 2 + 1]
      num_min = int(tmp_min * num_box)
      num_max = int(tmp_max // (1.0 / num_box))
      for n in range(num_min, num_max + 1):
        zero_array[len(zero_array) - 1 - n][m] = [0, 0, 0]
    np_tmp = np.array(zero_array, dtype=np.uint8)
    ret.append(np_tmp)
  print('Кількість малюнків складає : {}'.format(len(ret)))
  return ret

def getNormalizeDataRow(data):
  '''Нормалізація даних масиву на проміжку [0.0;1.0] по рядках
  Використовувати для однорідних даних по рядках.'''
  print('Нормалізація даних')
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

def prepareDataTrainPattern(data, num_bars, m_h):
  '''Підготовка масиву із фільтруванням'''
  print('Фільтруємо дані із висотою {:0.05f}'.format(m_h))
  a_name = []
  a_real = []
  for i in range(len(data) - num_bars):
    a = []
    a = data[i:i+num_bars]
    tmp_max = max([a[w][1] for w in range(len(a))])
    tmp_min = min([a[q][2] for q in range(len(a))])
    if m_h < (tmp_max - tmp_min):
      tmp = []
      for t in range(num_bars):
        tmp.append(data[i+t][2])
        tmp.append(data[i+t][1])
      a_name.append(data[i][0])
      a_real.append(tmp)
  return a_name, a_real

def prepareData_01(data):
  '''Видаляємо tuple та залишаємо array'''
  tmp = []
  for i in range(len(data)):
    tmp.append(list(data[i]))
  return tmp

if __name__ == '__main__':
  query_get_data = 'select pTime, pHigh, pLow from d_2010;'
  ret = sql3_getDataMoreRow(adr, query_get_data)
  ret = prepareData_01(ret)
  ret_name, ret = prepareDataTrainPattern(ret, num_train_candle, min_height)
  ret = getNormalizeDataRow(ret)
  ret = prepare(ret, num_boxes, num_train_candle)
  for i in range(len(ret)):
    img = Image.fromarray(ret[i])
    s_time = time.strftime('%d %b %Y %H %M', time.gmtime(int(ret_name[i])))
    img.save('chart_{}_{}.png'.format(ret_name[i], s_time))

