# 1 ------------------------------------------------------------
from NN_SOM import NN_SOM as som
import random

x_cells = 10
y_cells = 10
all_iterations = 100
num_random_train_pattern = 10
num_real_weights_in_pattern = 3
a_name = [] # масив імен
a_real = [] # масив навчальних даних

nn = som()
# nn = som(x_cells, y_cells, all_iterations)
print('Мережа {} на {} нейронів.'.format(nn.i_x_cells, nn.i_y_cells))
print('Кількість епох для обробки -> {}'.format(nn.i_iterations))
print('Початковий радіус околиці -> {:0.09f}'.format(nn.r_map_radius))
print('r_time_constant -> {:0.09f}'.format(nn.r_time_constant))
print('Початковий коефіцієнт навчання (ступінь впливу на зміну вагів нейронів) -> {:0.09f}'.format(nn.r_initial_learning_rate))
# 2 ------------------------------------------------------------
# a_name - окремо одновимірний масив імен навчальних прикладів/паттернів
# a_real - окремо двовимірний масив реальних значень. Це мають бути значення із навчальних прикладів
# як хочеш, так і подаєш дані
for i in range(num_random_train_pattern):
    a_name.append(f'{i}')
    a_real.append([random.random() for i in range(num_real_weights_in_pattern)])
    print('"{}" -> {}'.format(a_name[-1], a_real[-1]))
# 3 ------------------------------------------------------------
# повертаємо масив із об'єктів класа NN_SOM_Neuron
ns = nn.setInitParam(a_real)
# 4 ------------------------------------------------------------
# нормалізація даних та вивід на екран перших 3ох результатів
a_real_normalize = nn.getNormalizeData(a_real)
for i in range(3):
    print('-'*20)
    print(a_real[i])
    print(a_real_normalize[i])
# 5 ------------------------------------------------------------
# Повне навчання
train_a_nn = nn.TrainAll(ns, a_real_normalize)
