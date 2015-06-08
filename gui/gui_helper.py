
# This file contains some funcitons that are called by the gui

  
import os
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../face_detection/"))
#from face import get_top_matches

COUNT = 1000
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
  os.system("cp ../pupil/pupil_src/capture/pic/pic" + pic_num + ".jpg capture.jpg")

  #Coordinates of pupil
  pic_coord_file = "../pupil/pupil_src/capture/pic/pic" + pic_num + ".txt"
  print pic_coord_file
  f = open(pic_coord_file, 'r')
  coord = f.readline().split()
  
  coord = find_coordinates(coord, pic_num)
  if len(coord) != 0:
    coord = [coord[1], coord[3]]
  
  return ("capture.jpg", coord)


'''find the coordinates in the most recent file possible
params:
  coord-Current coordinate(array of 'x',x-coord,'y',y-coord when correct format
  picnum-current picture number of the current coordinate
  return coordinate or empty list if no coordinate found
'''
def find_coordinates(coord, pic_num):
  count = COUNT
  while len(coord) != 4 and count > 0:
    pic_num = int(pic_num) - 1
    count = count- 1
    if pic_num < 0:
      folder = "../pupil/pupil_src/capture/pic/"
      os.system("ls " + folder + " | wc -l > output.txt")
      f = open("output.txt", 'r')
      file_number = str(int(f.readline().rstrip().lstrip()) / 2)
      pic_num = pic_num % min(file_number, COUNT)
      #adj_pic_num = COUNT + pic_num
    pic_coord_file = "../pupil/pupil_src/capture/pic/pic" + str(pic_num) + ".txt"
    f = open(pic_coord_file, 'r')
    coord = f.readline().split()
  if count == 0:
    return []

  return coord



if __name__ == "__main__":
  main()


