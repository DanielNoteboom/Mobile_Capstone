
# This file contains some funcitons that are called by the gui

  
import os
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../face_detection/"))
from face import get_top_matches

COUNT = 10
'''sample main method that runs through all the components 
to give an idea of how functions should be used'''
def main():
  run_pupil()
  picture, coord = take_snapshot()
  facial_detection(picture, coord)

'''Runs the pupil player in a separate process'''
#TODO Kill process when program is done
def run_pupil():
  newpid = os.fork()
  #Run pupil in the background with new process(have to kill later somehow...)
  if newpid == 0:
    os.execv("../pupil/run_capture", ['foo'])
  #else:
  #Give the pupil player time to load up
  #  time.sleep(5)

'''Captures the latest snapshot from the pupil player
Returns: picture and coordinates of image'''
def take_snapshot():
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
  
  coord = find_coordinates(coord, pic_num)
  coord = [coord[1], coord[3]]
  
  return (pic_file, coord)


'''find the coordinates in the most recent file possible
params:
  coord-Current coordinate(array of 'x',x-coord,'y',y-coord when correct format
  picnum-current picture number of the current coordinate
  return coordinate
'''
def find_coordinates(coord, pic_num):
  count = COUNT
  adj_pic_num = pic_num
  while len(coord) != 4 and count > 0:
    pic_num = int(pic_num) - 1
    count = count- 1
    if pic_num < 0:
      adj_pic_num = COUNT + pic_num
    pic_coord_file = "../pupil/pupil_src/capture/pic/pic" + str(adj_pic_num) + ".txt"
    f = open(pic_coord_file, 'r')
    coord = f.readline().split()
  if count == 0:
    print "Please plug-in pupil player, place on face, and make sure camera is focused"

    f = open("../pupil/pupil_src/capture/pic/quit.txt", 'w') 
    f.write("quit")
    sys.exit(0)
  return coord

'''detects the face given the picture file and the coordinate
params
pic_file: picture that you're looking for faces in
x_coord: x coordinate of face
y_coord y-coordinate of face
return: tuple of files that contain top matches'''
def facial_detection(pic_file, x_coord, y_coord):
  return get_top_matches(pic_file, x_coord, y_coord)



if __name__ == "__main__":
  main()


