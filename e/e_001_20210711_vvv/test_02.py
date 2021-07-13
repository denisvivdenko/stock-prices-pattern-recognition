from NN_SOM import NN_SOM as som
import random, copy

x_cells = 5
y_cells = 5
all_iterations = 2000
num_random_train_pattern = 100
num_real_weights_in_pattern = 5
a_name = [] # масив імен
a_real = [] # масив навчальних даних

# nn = som()
nn = som(x_cells, y_cells, all_iterations)

for i in range(num_random_train_pattern):
    a_name.append(f'{i}')
    a_real.append([random.random() for i in range(num_real_weights_in_pattern)])
    print('"{}" -> {}'.format(a_name[-1], a_real[-1]))
    if i >= 10:
        break


# In[3]:


# 3 ------------------------------------------------------------
# повертаємо масив із об'єктів класа NN_SOM_Neuron
ns = nn.setInitParam(a_real)
ns_old = copy.deepcopy(ns)


# In[4]:


for i in range(len(ns)):
    print(i)
    print(ns[i].a_weights)
    print(ns_old[i].a_weights)
    print('')
    if i > 10:
        break


# In[5]:


# 4 ------------------------------------------------------------
# нормалізація даних та вивід на екран перших 3ох результатів
a_real_normalize = nn.getNormalizeDataRow(a_real)
for i in range(3):
    print('-'*20)
    print(a_real[i])
    print(a_real_normalize[i])


# In[6]:


# 5 ------------------------------------------------------------
# Повне навчання
ns_new = nn.TrainAll(ns, a_real_normalize)


# In[7]:


# print all weights --------------------------------------------
for i in range(len(ns_new)):
    print('\n#{:03d} {}'.format(i, '-'*30))
    print('Старі дані')
    print(ns_old[i].a_weights)
    print('Нові дані')
    print(ns_new[i].a_weights)
    if i >= 4:
        break
# print all weights --------------------------------------------


# In[8]:


print(a_name[0])
print(a_real_normalize[0])
a_1 = a_real_normalize[0]
# first train ----------------------------
tmp_min_ind = 0
tmp_min_dist = ns_old[0].getCalculateDistance(a_1)
for i in range(1, len(ns_old)):
    tmp1 = ns_old[i].getCalculateDistance(a_1)
    #print('#{} -> {:0.05f}'.format(i, tmp1))
    if tmp1 < tmp_min_dist:
        tmp_min_dist = tmp1
        tmp_min_ind = i
print(tmp_min_ind)

# last train ----------------------------
tmp_min_ind = 0
tmp_min_dist = ns_new[0].getCalculateDistance(a_1)
for i in range(1, len(ns_new)):
    tmp1 = ns_new[i].getCalculateDistance(a_1)
    #print('#{} -> {:0.05f}'.format(i, tmp1))
    if tmp1 < tmp_min_dist:
        tmp_min_dist = tmp1
        tmp_min_ind = i
print(tmp_min_ind)


# In[9]:


# 6 ------------------------------------------------------------
# Дістаємо усю інформацію, яка відноситься до певного навчального прикладу
num_research_pattern = 0
research_pattern_name = a_name[num_research_pattern]
research_pattern_real = a_real_normalize[num_research_pattern]
num_class_old = nn.getBestMatchingNode(ns_old, research_pattern_real)
num_class_new = nn.getBestMatchingNode(ns_new, research_pattern_real)
print('Навчальний приклад "{}" -> '.format(research_pattern_name), end="")
print(research_pattern_real)
print('Перед початком тренування цей паттерн відносився до класу #{:02d}'.format(num_class_old))
print('Після тренування цей паттерн став відноситись до класу #{:02d}'.format(num_class_new))


# In[10]:


for i in range(len(a_name)):
    nbmn_old = nn.getBestMatchingNode(ns_old, a_real_normalize[i])
    nbmn_new = nn.getBestMatchingNode(ns_new, a_real_normalize[i])
    print('#{:02d}: {:03d} -> {:03d}'.format(i, nbmn_old, nbmn_new))
    if i >= 10:
        break


# In[ ]:




