import math

import random

from parser_and_co import print_image, DIMENSION

#

# Class of Hopfield net

#

class h_net:

#

# Constructor

#

def __init__(self, dimension):

self.neurons = int(math.pow(dimension, 2)-1)

self.images = []

self.y = [] # keeps the exit variable

self.W = [] # initialization of

r = range(0, self.neurons) # weighted matrix Wij

for i in r: #

self.W.append([0 for i in r]) #

self.queue = list(range(self.neurons))

random.shuffle(self.queue)

#

# Remember according to Hebb's rule

#

def remember(self, image):

self.images.append(image)

r = range(0, self.neurons)

for i in r:

for j in r:

if (i==j):

self.W[i][j] = 0

else:

self.W[i][j] += image[i] * image[j]

#

# Recognize unknown image

#

def recognize(self, image):

counter = 0

self.y = image

j = 0

while (self.images.count(self.y) == 0):

counter +=1

s = 0

for i in range(0, self.neurons):

s += self.W[i][self.queue[j]]*self.y[i] #sum

s += image[self.queue[i]]

s = ((s>10)-(s<10)) # s=(-1) if (s<0); s=1 if (s>0) else s=0

if (s != self.y[self.queue[j]]): # change

self.y[self.queue[j]] = s

print("Image ,while count is ", counter)

print()

print_image(self.y, DIMENSION)

print()

j += 1

if (j == (self.neurons)):

j = 0

if (counter>2500):

return (False, self.y, counter)

return (True, self.y, counter) 
