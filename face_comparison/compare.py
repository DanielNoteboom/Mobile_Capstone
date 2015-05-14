from subprocess import call, Popen, PIPE
from os import listdir
import sys
import Queue
import os.path

#controls the number of matches that the code will return
NUM_MATCHES = 3

# returns an array with the top NUM_MATCHES comparison match
# @params
#   test    the image file to be identified
#   cDir    the directory containing subdirectories of test images
def compare( test, cDir ):

  if not os.path.isfile(test):
    print "Invalid test image " + test
    return None

  if not os.path.isdir(cDir):
    print "Invalid directory " + cDir
    return None
  
  # OpenBR recursively compares across all images in subdirectories
  compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", 
                      test, cDir], stdout=PIPE, stderr=PIPE)
  data = compOutput.communicate()
  # data is contained in fist index of output
  dataArray = str(data[0]).split()
  scores = []
  for i in range(len(dataArray)):
    if i % 2 == 0 and i != 0:
      scores.append(float(dataArray[i]))

  matches = getMatches(cDir, scores)

  hits = []
  for i in range(NUM_MATCHES):
      try:
          hit = matches.get_nowait()
          hits.append({
            'matchPath': hit[2], 
            'id': hit[1].split("/")[-1:][0], 
            'average': -hit[0],
            'median': -hit[3]
            })
      except Queue.Empty:
      	break
  return hits

def getMatches( cDir, scores ):
  matches = Queue.PriorityQueue(0)
  extCtr = 0 # index in the large array
  comparisons = listdir(cDir)
  # only works because both OpenBR and python recurse thru dirs alphanumerically
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):
      idScores = []
      max = 1.0

      # aggregate all scores for a given id
      images = listdir(cDir + "/" + identity)
      numImages = len(images)
      bestImage = 1
      for i in range(numImages):
        score = scores[extCtr]
        extCtr += 1
        if score > max:
          max = score
          bestImage = i
        idScores.append(score)
      matches.put((-sum(idScores)/numImages, #average
                  os.path.abspath(cDir + "/" + identity), #id
                  os.path.abspath(cDir + "/" + identity + "/" + images[bestImage]), #bestImage.jpg
                  -sorted(idScores)[numImages/2])) #median
  return matches

def compareByDir(cDir, comparisons): #tooSlow
  matches = Queue.PriorityQueue(0)
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):  
      cImages = listdir(cDir + "/" + identity)
      aggregateIndex = 0
      compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", 
                          test, cDir + "/" + identity],
                          stdout=PIPE, stderr=PIPE)
      data = compOutput.communicate()
      dataArray = str(data[0]).split()
      source = str(data[1]).split()[9].split("/")[1]
      for i in range(len(dataArray)):
        if i % 2 == 0 and i != 0:
          aggregateIndex += float(dataArray[i].strip())
      matches.put((-aggregateIndex, os.path.abspath(cDir + "/" + identity)))

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Usage: python compare.py IMAGE_PATH COMPARISON_DIRECTORY"
    sys.exit(0)
  else:
    matches = compare(sys.argv[1], sys.argv[2])
    print matches