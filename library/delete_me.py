#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Опис файлу
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

#discrete color scheme
cMap = ListedColormap(['white', 'white', 'white', 'white', 'black'])
if __name__ == '__main__':
  data = np.random.rand(10, 10)
  print(data)
  plt.title('Test')
  a = plt.pcolor(data, cmap=cMap, vmin = 0.0, vmax = 1.0)
  plt.colorbar(a)
  plt.savefig('delete_me.png')
  plt.show()
