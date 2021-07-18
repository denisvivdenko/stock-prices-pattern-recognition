from __future__ import with_statement
import os

MAX = 1024
DIMENSION = 16

d_parse = {'.': -1, '#': 1}
d_print = {-1:'.' ,1 :'#' }

def parse(dir):
  filenames_l = []
  for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    if os.path.isfile(filepath):
      filenames_l.append(filepath)
  images_l = []
  for filepath in filenames_l:
    image = parse_image(filepath)
    images_l.append(image)
  return images_l

# parse_image returns file in a list
def parse_image(filepath):
  with open(filepath) as f:
    temporary = f.read(MAX)
    temporary = temporary.replace("\n", "")
    temporary = temporary.replace("\r", "")
  image_l = []
  for i in temporary:
    image_l.append(d_parse[i])
  if len(image_l) != pow(DIMENSION, 2):
    raise Exception("The dimension of images must be %gx%g" % (DIMENSION, DIMENSION))
  return image_l

# print_image prints an image
def print_image (list, size):
  c = 0
  for i in list:
    print(d_print[i], end = ' ')
    c += 1
    if (c % size == 0):
      print()
