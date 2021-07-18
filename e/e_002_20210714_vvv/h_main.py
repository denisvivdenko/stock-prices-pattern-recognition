import sys 
from parser_and_co import parse, parse_image, print_image, DIMENSION 
from h_net import h_net 
#https://moluch.ru/archive/40/4834/ 
learnt_images = "learnt_images" 
unfamiliar_image = "unfamiliar/unfamiliar.txt" 

def main(argv):
  images_ll = parse(learnt_images)
  image_l = parse_image(unfamiliar_image)
  print("Known images")
  for i in images_ll:
    print_image(i, DIMENSION)
    print("Remembering images")
    network = h_net(DIMENSION)
    for i in images_ll:
      network.remember(i)
      print()
      print("Changed image ")
      print_image(image_l, DIMENSION)
      print()
      print("Detecting image:")
      (recognized, recimage, counter) = network.recognize(image_l)
      print()
      if recognized:
        print("Recognized in %g" %counter)
      else:
        print("Not recognized in %g" %counter)
        print_image(recimage, DIMENSION)

if __name__ == '__main__':
  main(sys.argv[1:])

