#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Бібліотека по обробці даних та пошуку кореляції між елементами
'''
import math

def getCorrelationPearson(a, b):
  '''Коефіцієнт кореляції Пірсона (r-Пірсона) використовується 
  для дослідження зв'язків двох однакових за розміром наборів даних
  виміряних для дослідження у метричній шкалі на однаковій вибірці.
  Це дозволяє виміряти, наскільки пропорційна складова двох наборів даних
  a, b - два однорангові масиви для порівняння'''
  a_average = sum(a) / len(a)
  b_average = sum(b) / len(b)
  p1 = [(a[i] - a_average) for i in range(len(a))]
  p2 = [(b[i] - b_average) for i in range(len(b))]
  chiselnik = sum([p1[i] * p2[i] for i in range(len(p1))])
  left = sum([p1[i] ** 2 for i in range(len(p1))])
  right = sum([p2[i] ** 2 for i in range(len(p2))])
  znamennik = (left * right) ** 0.5
  ret = chiselnik / znamennik
  return ret
