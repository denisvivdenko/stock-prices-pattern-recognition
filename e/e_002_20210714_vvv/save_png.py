#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Запис матриці із 0 та 1 у файл png
'''
import os, sys, sqlite3, time, calendar
from mylib import *
import PIL
from PIL import Image
import numpy as np
import random

if __name__ == '__main__':
  tst_all = []
  tst1 = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(3)]
  tst_all.append(tst1)
  tst2 = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(3)]
  tst_all.append(tst2)
  tst3 = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(3)]
  tst_all.append(tst3)
  tst4 = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(3)]
  tst_all.append(tst4)
  print('\ntst_all :')
  print(tst_all)
  tst = np.array(tst_all, dtype=np.uint8)
  print('\ntst_all numpy:')
  print(tst)

  img2 = Image.fromarray(tst)
  img2.save('tst4.png')
