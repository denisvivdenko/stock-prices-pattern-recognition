#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Нейрон для Self Organized Map
'''
import random

class NN_SOM_Neuron():
  '''Нейрон мережі SOM.'''

  def __init__(self, x, y, num_w = 3):
    '''Ініціалізація нейрону:
      x,y - координати нейрону у середині мережі
      num_w - кількість вагів'''
    self.i_x = 0
    '''Координата нейрону/класу по осі X'''
    self.i_y = 0
    '''Координата нейрону/класу по осі Y'''
    self.i_num_weights = num_w
    '''Кількість вагів у нейроні або вузлі'''
    self.a_weights = [random.random() for i in range(self.i_num_weights)]
    '''Масив вагів на проміжку [0.0;1.0)'''

  def getCalculateDistance(self, vector):
    '''Розрахунок квадрату відстані між вагами та переданим вектором.'''
    dist_sqr = 0.0
    for i in range(len(self.a_weights)):
      dist_sqr += (vector[i] - self.a_weights[i])**2
    return dist_sqr

  def setCorrectWeights(self, vector, learning_rate, influence):
    '''Корекція вагів вузла у напрямку вектора
    :param vector array: сам вектор
    :param learning_rate real: коефіцієнт навчання
    :param influence real: розрахунок ступеня впливу на вузол або нейрон'''
    for i in range(len(self.a_weights)):
      self.a_weights[i] += learning_rate * influence * (vector[i] - self.a_weights[i])
