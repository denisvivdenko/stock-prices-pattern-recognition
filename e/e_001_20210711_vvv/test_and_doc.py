#!/usr/bin/env python
# coding: utf-8

# ---
# ## Тестуємо нейромережу SOM
# 1. Ініціалізація параметрів
#     - за замовчуванням мережа 10 на 10 із 2000 епох
# 2. Підготовка даних для нейромережі
#     - окремо масив із назвами патернів і окремо масив із даними. Потім можна реалізувати конкретно під panda
# 3. Генерація масиву нейронів
# 4. Підготовка даних для відправки у SOM
#     - нормалізація даних
# 5. Тренування
# 5. Пошук класу, до якого належить навчальний приклад
# ---

# In[38]:


# 1 ------------------------------------------------------------
from NN_SOM import NN_SOM as som
import random

x_cells = 3
y_cells = 3
all_iterations = 2000
num_random_train_pattern = 100
num_real_weights_in_pattern = 5
a_name = [] # масив імен
a_real = [] # масив навчальних даних

# nn = som()
nn = som(x_cells, y_cells, all_iterations)
print('Мережа {} на {} нейронів.'.format(nn.i_x_cells, nn.i_y_cells))
print('Кількість епох для обробки -> {}'.format(nn.i_iterations))
print('Початковий радіус околиці -> {:0.09f}'.format(nn.r_map_radius))
print('r_time_constant -> {:0.09f}'.format(nn.r_time_constant))
print('Початковий коефіцієнт навчання (ступінь впливу на зміну вагів нейронів) -> {:0.09f}'.format(nn.r_initial_learning_rate))


# In[39]:


# 2 ------------------------------------------------------------
# a_name - окремо одновимірний масив імен навчальних прикладів/паттернів
# a_real - окремо двовимірний масив реальних значень. Це мають бути значення із навчальних прикладів
# як хочеш, так і подаєш дані
for i in range(num_random_train_pattern):
    a_name.append(f'{i}')
    a_real.append([random.random() for i in range(num_real_weights_in_pattern)])
    print('"{}" -> {}'.format(a_name[-1], a_real[-1]))


# In[40]:


# 3 ------------------------------------------------------------
# повертаємо масив із об'єктів класа NN_SOM_Neuron
ns_start = nn.setInitParam(a_real)


# In[41]:


# 4 ------------------------------------------------------------
# нормалізація даних та вивід на екран перших 3ох результатів
a_real_normalize = nn.getNormalizeData(a_real)
for i in range(3):
    print('-'*20)
    print(a_real[i])
    print(a_real_normalize[i])


# In[42]:


# TEST @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
for i in range(len(ns_start)):
    s1 = '#{} -> '.format(i)
    for y in range(len(ns_start[i].a_weights)):
        s1 += '{:0.03f}|'.format(ns_start[i].a_weights[y])
    print(s1[:-1])
# TEST @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# In[43]:


# 5 ------------------------------------------------------------
# Повне навчання
ns_end = nn.TrainAll(ns_start, a_real_normalize)


# In[44]:


# 6 ------------------------------------------------------------
# Дістаємо усю інформацію, яка відноситься до певного навчального прикладу
num_research_pattern = 0
research_pattern_name = a_name[num_research_pattern]
research_pattern_real = a_real_normalize[num_research_pattern]
num_class_old = nn.getBestMatchingNode(ns_start, research_pattern_real)
num_class_new = nn.getBestMatchingNode(ns_end, research_pattern_real)
print('Навчальний приклад "{}" -> '.format(research_pattern_name), end="")
print(research_pattern_real)
print('Перед початком тренування цей паттерн відносився до класу #{:02d}'.format(num_class_old))
print('Після тренування цей паттерн став відноситись до класу #{:02d}'.format(num_class_new))


# In[45]:


for i in range(len(a_name)):
    nbmn_old = nn.getBestMatchingNode(ns_start, a_real_normalize[i])
    nbmn_new = nn.getBestMatchingNode(ns_end, a_real_normalize[i])
    print('#{:02d}: {} -> {}'.format(i, nbmn_old, nbmn_new))


# In[ ]:




