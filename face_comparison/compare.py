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
  
  matches = getMatches(cDir, runOpenBR(test, cDir))
  return matchInfo(matches)

def runOpenBR( test, cDir ):
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
  return scores

def getMatches( cDir, scores ):
  matches = Queue.PriorityQueue(0)
  extCtr = 0 # index in the large array
  comparisons = listdir(cDir)
  # only works because both OpenBR and python recurse thru dirs alphanumerically
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):
      idScores = []
      max = 0.0

      # aggregate all scores for a given id
      images = listdir(cDir + "/" + identity)
      numImages = len(images)
      bestImage = 0
      for i in range(numImages):
        score = scores[extCtr]
        extCtr += 1
        if score > max:
          max = score
          bestImage = i
        idScores.append(score)
      if idScores:
        matches.put((-sum(idScores)/numImages, -sorted(idScores)[numImages/2], #average, median
        #matches.put((-sorted(idScores)[numImages/2], -sum(idScores)/numImages, #median, average
                    {
                      'id': identity,
                      'match_path': os.path.abspath(cDir + "/" + identity + "/" + images[bestImage])
                    }))
  return matches

def matchInfo( matches ):
  hits = []
  for i in range(NUM_MATCHES):
      try:
          hit = matches.get_nowait()
          hits.append({
            'match_path': hit[2]['match_path'], 
            'id': hit[2]['id'], 
<<<<<<< HEAD
            'median': -hit[1],
            'average': -hit[0]
=======
            'median': -hit[0],
            'average': -hit[1]
>>>>>>> cea4e80ae86f1c07944746f6a715a7d12c2f09cf
            })
      except Queue.Empty:
        return None
  return hits

def getMatchesBySubDirectory(cDir, comparisons): #tooSlow
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
