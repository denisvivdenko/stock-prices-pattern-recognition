import PIL
from PIL import Image
an_image = Image.open('new.png')
sequence_of_pixels = an_image.getdata()
list_of_pixels = list(sequence_of_pixels)
for i in range(len(list_of_pixels)):
  clr = 'black'
  if (255, 255, 255, 255) == list_of_pixels[i]:
    clr = 'white'
  print('#{:03d} -> {} | {}'.format(i, list_of_pixels[i], clr))
