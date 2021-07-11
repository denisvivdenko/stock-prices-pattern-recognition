#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Self Organized Map
'''
from NN_SOM_Neural import NN_SOM_Neural

class NN_SOM():
  '''NN_SOM'''

  def __init__(self):
    self.i_x_cells = 0
    '''Кількість комірок по горизонталі, по осі Х'''

    self.i_y_cells = 0
    '''Кількість комірок по вертикалі, по осі Y'''
    
    self.a_NN = []
    '''Масив нейронів'''
    
    self.i_total_train_sets = 0
    '''Загальна кількість навчальних прикладів'''
    
    self.i_iterations = 0
    '''Загальна кількість епох'''
    
    self.i_iter_now = 0
    '''Кількість епох, що мережа вже пройшла'''
    
    self.a_training_sets = []
    '''Навчальні приклади у масиві'''
    
    self.a_training_sets_normalize = []
    '''Навчальні приклади нормалізовані на проміжку [0.0;1.0)'''
    
    self.a_max_values = []
    '''Масив максимальних значень із навчальної вибірки'''
    
    self.a_min_values = []
    '''Масив мінімальних значень із навчальної вибірки'''

    self.r_map_radius = 0.0
    '''Початковий радіус окружності'''
    
    self.r_time_constant = 0.0
    
    self.r_initial_learning_rate = 0.1;
    '''Початковий коефіцієнт навчання'''
    
    self.i_select_index_train_pattern = -1
    '''Індекс навчального паттерна, який подається для кластерізації'''
