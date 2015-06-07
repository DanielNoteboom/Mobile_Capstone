from compare_opencv import FaceComparer
import sys
import os

def find_threshold(cX):
	fc = FaceComparer(cX+'_train')
	acc = 0
	thresholds = [11000, 4500, 220]
	best_thresh = []

	for i in xrange(thresholds[0], 13000, 1000):
		for j in xrange(thresholds[1], 7000, 500):
			for k in xrange(thresholds[2], 250, 10):
				print "Testing [" + str(i) + ", " + str(j) + ", " + str(k) + "]: ",
				local_accuracy = accuracy(fc, cX+'_test', [i, j, k])
				print str(local_accuracy)
				if local_accuracy >= acc:
					acc = local_accuracy
					best_thresh = [i, j, k]
	return best_thresh

def accuracy(fc, test_dir, thresholds):
	correct = 0
	ct = 0
	
	identities = os.listdir(test_dir)
	for identity in identities:
		images = os.listdir(test_dir+'/'+identity)
		for image in images:
			res = fc.predict_test(test_dir+'/'+identity+'/'+image, None)
			if res is not None:
				# print str(test_labels[test]) + " predicted as " + str(res[0]) + " using " + str(res[1])
				if res[0] == identity:
					correct += 1
				ct += 1
	return correct/float(ct)

def test(train_dir, test_dir):
	fc = FaceComparer(train_dir)
	identities = os.listdir(test_dir)
	for identity in identities:
		images = os.listdir(test_dir+'/'+identity)
		for image in images:
			print "Testing " + str(identity)
			res = fc.predict_test(test_dir+'/'+identity+'/'+image, None)
			print " " + str(res)
			# if res is None:
			# 	print ", closest match: NOT FOUND."
			# else:
			# 	", closest match: " + str(res[0])

if __name__ == "__main__":
  if len(sys.argv) != 3 and len(sys.argv) != 2:
    print "Usage: python face_compare_test.py TRAIN_DIR TEST_DIR"
    sys.exit(0)
  elif len(sys.argv) == 3:
  	train_dir = sys.argv[1]
  	test_dir  = sys.argv[2]
  	test(train_dir, test_dir)
  else:
  	best_thresh = find_threshold(sys.argv[1])
  	print best_thresh