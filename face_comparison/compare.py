from subprocess import call, Popen, PIPE
from os import listdir
import sys
import Queue
import os.path

#controls the number of matches that the code will return
NUM_MATCHES = 1

# returns an array with the top NUM_MATCHES comparison match
# @params
#   test    the image file to be identified
#   cDir    the directory containing subdirectories of test images
def compare( test, cDir ):

  if not os.path.isfile(test):
    print "Invalid test image " + test
    return None

  if not os.path.isdir(cDir):
    print "Invalid directory " + cDir;
    return None;

  comparisons = listdir(cDir)

  matches = Queue.PriorityQueue(0)
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):
      # find openBR correlation for each image in subdirectory    
      cImages = listdir(cDir + "/" + identity)
      aggregateIndex = 0;
      for img in cImages:
        if os.path.isfile(cDir + "/" + identity + "/" + img):
          compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", 
                              test, cDir + "/" + identity + "/" + img],
                              stdout=PIPE, stderr=PIPE)
          data = compOutput.communicate()
          aggregateIndex += float(data[0].strip())
      matches.put((-aggregateIndex, os.path.abspath(cDir + "/" + identity)))
    comparisonFiles = listdir(cDir + "/" + identity)
      
  hits = []
  for i in range(NUM_MATCHES):
      try:
          hit = matches.get_nowait()
          hits.append((hit[1] + "/1.jpg", hit[1].split("/")[-1:][0], -hit[0]))
      except Queue.Empty:
      	break
  return hits

  #outfile = open("face_compare_info.txt", "w")

  #outfile.write(str(len(hits)) + "\n")
  #for hit in hits:
  #    index = -hit[0]
  #    name  = hit[1]
  #    outfile.write("%s %s\n" % (name, str(index)))

if __name__ == "__main__":
  if len(sys.argv) != NUM_MATCHES:
    print "Usage: python main.py IMAGE_PATH COMPARISON_DIRECTORY"
    sys.exit(0)
  else:
    matches = compare(sys.argv[1], sys.argv[2])
    print matches
