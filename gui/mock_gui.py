#This file is meant to demonstrate the ability to start the pupil player, grab a snapshot at aspecified time and run the program to get the top three matches. All the gui aspects that interact with the external environment in one program

import os
import time
os.system("source ~/.bashrc")
newpid = os.fork()

#Run pupil in the background with new process(have to kill later somehow...)
if newpid == 0:
  os.execv("../pupil/run_capture", ['foo'])
else:
  #Give the pupil player time to load up
  time.sleep(20)

  #This file contains the number of the current snapshot captured by the pupil player
  f = open("../pupil/pupil_src/capture/pic/current_count.txt", 'r')
  pic_num = f.readline().strip();

  #Contains the current snapshot
  pic_file = "../pupil/pupil_src/capture/pic/pic" + pic_num + ".jpg"
  #Coordinates of pupil
  pic_coord_file = "../pupil/pupil_src/capture/pic/pic" + pic_num + ".txt"
  print pic_coord_file
  f = open(pic_coord_file, 'r')
  coord = f.readline().split()
  
  #length 4 means x {x-coord} y {y-coord}
  while len(coord) != 4 and pic_num >= 0:
    pic_num = int(pic_num) - 1
    pic_coord_file = "../pupil/pupil_src/capture/pic/pic" + str(pic_num) + ".txt"
    print pic_num
    f = open(pic_coord_file, 'r')
    coord = f.readline().split()
  if pic_num < 0:
    print "Please plug-in pupil player, place on face, and make sure camera is focused"
  print coord
  os.system("identify ~/Mobile_Capstones/pupil/pupil_src/capture/pic/pic3535.jpg > output.txt")
  f = open("output.txt", 'r')
  image_size = f.readline().split()[2]
  image_dim = image_size.split("x")
  x_coord = int(float(coord[1]) * int(image_dim[0]))
  y_coord = int(float(coord[3]) * int(image_dim[1]))
  print x_coord
  print y_coord
  os.system("python ../face_detection/face.py " +  pic_file + " " +  str(x_coord) + " " + str(y_coord))
  cleanup()
  print "done"


def cleanup():
  os.system("rm output.txt")

