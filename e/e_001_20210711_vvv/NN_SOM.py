#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Self Organized Map
'''
from NN_SOM_Neuron import NN_SOM_Neuron
import math, copy, random

class NN_SOM():
  '''NN_SOM'''

  def __init__(self, x=10, y=10, iter=2000):
    self.i_x_cells = x
    '''Кількість комірок по горизонталі, по осі Х'''

    self.i_y_cells = y
    '''Кількість комірок по вертикалі, по осі Y'''
    
    self.a_NN = []
    '''Масив нейронів'''
    
    self.i_iterations = iter
    '''Загальна кількість епох'''

    self.i_iter_now = 0
    '''Поточний номер епохи'''

    self.r_map_radius = 0.0
    '''Початковий радіус околиці'''
    
    self.r_time_constant = 0.0
    
    self.r_initial_learning_rate = 0.1;
    '''Початковий коефіцієнт навчання'''
    
    if self.i_x_cells > self.i_y_cells:
      self.r_map_radius = self.i_x_cells / 2.0
    else:
      self.r_map_radius = self.i_y_cells / 2.0
    self.r_time_constant = 1.0 * self.i_iterations / math.log(self.r_map_radius)

  def getNormalizeDataColumn(self, data):
    '''Нормалізація даних по стовпцях на проміжку [0.0;1.0]
    Використовувати для даних, що не мають нічого спільного по стовпцях'''
    tmp1 = []
    for i in range(len(data[0])):
      __min = data[0][i]
      __max = __min
      for y in range(1, len(data)):
        if data[y][i] > __max:
          __max = data[y][i]
        if data[y][i] < __min:
          __min = data[y][i]
      tmp1.append([__min, __max])
    for i in range(len(data[y])):
      __height = tmp1[i][1] - tmp1[i][0]
      tmp2 = []
      for y in range(1, len(data)):
        if __height == 0.0:
          tmp2.append(0.5)
        elif data[y][i] == tmp1[i][0]:
          tmp2.append(0.0)
        else:
          tmp2.append((data[y][i] - tmp1[i][0]) / __height)
      a_normalize.append(tmp2)
    return list(map(list, zip(*a_normalize)))

  def getNormalizeDataRow(self, data):
    '''Нормалізація даних по рядках на проміжку [0.0;1.0]
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

  def setInitParam(self, a_tp):
    '''Ініціалізація нейронної мережі.
    Повертає масив нейронів'''
    a_NN = []
    for y in range(self.i_y_cells):
      for x in range(self.i_x_cells):
        tmp_nn = NN_SOM_Neuron(x, y, len(a_tp[0]))
        a_NN.append(tmp_nn)
    return a_NN

  def getBestMatchingNode(self, a_nn, train_vector):
    '''Повертає індекс найбільш близького вузла до параметрів масиву vector
    a_nn - масив нейронів
    train_vector - навчальний приклад, має бути нормалізованим'''
    tmp_min_ind = 0
    tmp_min_dist = a_nn[tmp_min_ind].getCalculateDistance(train_vector)
    for i in range(1, len(a_nn)):
      tmp = a_nn[i].getCalculateDistance(train_vector)
      if tmp < tmp_min_dist:
        tmp_min_dist = tmp
        tmp_min_ind = i
    return tmp_min_ind

  def TrainPart(self, a_nn, a_vector):
    '''Часткове тренування мережі. Тренування 1 епохи.
    a_nn - масив нейромереж
    a_vector - навчальний приклад '''
    num_winningNode = self.getBestMatchingNode(a_nn, a_vector)
    r_neighbourhood_radius = self.r_map_radius * math.exp(-1.0 * self.i_iter_now / self.r_time_constant)
    '''Визначаємо поточний радіус околиці'''
    r_ws = r_neighbourhood_radius**2
    '''квадрат радіуса околиці'''
    for i in range(len(a_nn)):
      tmp_x = a_nn[num_winningNode].i_x - a_nn[i].i_x
      tmp_y = a_nn[num_winningNode].i_y - a_nn[i].i_y
      r_distToNodeSQR = tmp_x**2 + tmp_y**2
      '''Розрахунок квадрату відстані між вузлом num_winningNode та теперешнім'''
      '''Якщо вузол у середині околиці, то перераховуємо ваги'''
      if r_distToNodeSQR < r_ws:
        r_influence = math.exp(-0.5 * r_distToNodeSQR / r_ws)
        '''Розрахунок ступеня впливу на вузол або нейрон'''
        a_nn[i].setCorrectWeights(a_vector, self.r_initial_learning_rate, r_influence)
    self.r_initial_learning_rate = self.r_initial_learning_rate * math.exp(-1.0 * self.i_iter_now / self.i_iterations)
    self.i_iter_now += 1
    return a_nn

  def TrainAll(self, a_nn, a_r):
    '''Тренування мережі
    a_nn - масив нейронів
    a_r - масив нормалізованих даних'''
    tmp_learning_rate = self.r_initial_learning_rate
    '''Тимчасове експоненційне зниження коефіцієнту навчання'''
    self.i_iter_now = 0
    while self.i_iter_now < self.i_iterations:
      a_vector = a_r[random.randint(0, len(a_r) - 1)]
      '''Масив нормалізованих даних із навчального набору, не ваги'''
      num_winningNode = self.getBestMatchingNode(a_nn, a_vector)
      r_neighbourhood_radius = self.r_map_radius * math.exp(-1.0 * self.i_iter_now / self.r_time_constant)
      '''Визначаємо поточний радіус околиці'''
      r_ws = r_neighbourhood_radius**2
      '''квадрат радіуса околиці'''
      for i in range(len(a_nn)):
        tmp_x = a_nn[num_winningNode].i_x - a_nn[i].i_x
        tmp_y = a_nn[num_winningNode].i_y - a_nn[i].i_y
        r_distToNodeSQR = tmp_x**2 + tmp_y**2
        '''Розрахунок квадрату відстані між вузлом num_winningNode та теперешнім'''

        '''Якщо вузол у середині околиці, то перераховуємо ваги'''
        if r_distToNodeSQR < r_ws:
          r_influence = math.exp(-0.5 * r_distToNodeSQR / r_ws)
          '''Розрахунок ступеня впливу на вузол або нейрон'''
          a_nn[i].setCorrectWeights(a_vector, tmp_learning_rate, r_influence)
      tmp_learning_rate = self.r_initial_learning_rate * math.exp(-1.0 * self.i_iter_now / self.i_iterations)
      self.i_iter_now += 1
    return copy.deepcopy(a_nn)
