from face_compare import FaceComparer
import sys

def find_threshold():
	fc = FaceComparer('c1')
	acc = 0
	thresholds = [10000, 2000, 100]
	best_thresh = []

	for i in xrange(thresholds[0], 16000, 1000):
		for j in xrange(thresholds[1], 2500, 100):
			for k in xrange(thresholds[2], 140, 10):
				print "Testing [" + str(i) + ", " + str(j) + ", " + str(k) + "]: ",
				local_accuracy = accuracy(fc, [i, j, k])
				print str(local_accuracy)
				if local_accuracy >= acc:
					acc = local_accuracy
					best_thresh = [i, j, k]
	return best_thresh

def accuracy(fc, thresholds):
	test_images = ['evan', 'bryan', 'daniel', 'jane', 'renee']
	test_labels = ['Evan_Whitfield', 'Bryan_Djunaedi', 'Daniel_Noteboom', 'Jane', 'Renee']

	correct = 0
	ct = 0
	for test in range(len(test_images)):
		for i in range(4):
			res = fc.predict_test(str(test_images[test]) + str(i+1) + '.jpg', thresholds)
			if res is not None:
				# print str(test_labels[test]) + " predicted as " + str(res[0]) + " using " + str(res[1])
				if res[0] == test_labels[test]:
					correct += 1
				ct += 1
	return correct/float(ct)

if __name__ == "__main__":
  if len(sys.argv) != 1:
    print "Usage: python face_compare_test.py"
    sys.exit(0)
  else:
    best_thresh = find_threshold()
    print best_thresh

# print "testing evan via evan1.jpg..." + str(fc.predict_test('evan1.jpg'))
# print "testing evan via evan2.jpg..." + str(fc.predict_test('evan2.jpg'))
# print "testing evan via evan3.jpg..." + str(fc.predict_test('evan3.jpg'))
# print "testing evan via evan4.jpg..." + str(fc.predict_test('evan4.jpg'))

# print "testing bryan via bryan1.jpg..." + str(fc.predict_test('bryan1.jpg'))
# print "testing bryan via bryan2.jpg..." + str(fc.predict_test('bryan2.jpg'))
# print "testing bryan via bryan3.jpg..." + str(fc.predict_test('bryan3.jpg'))
# print "testing bryan via bryan4.jpg..." + str(fc.predict_test('bryan4.jpg'))

# print "testing daniel via daniel1.jpg..." + str(fc.predict_test('daniel1.jpg'))
# print "testing daniel via daniel2.jpg..." + str(fc.predict_test('daniel2.jpg'))
# print "testing daniel via daniel3.jpg..." + str(fc.predict_test('daniel3.jpg'))
# print "testing daniel via daniel4.jpg..." + str(fc.predict_test('daniel4.jpg'))

# updates
# fc.update('test.jpg', 'Evan_Whitfield')
# fc.update('evan1.jpg', 'Evan_Whitfield')
# fc.update('daniel1.jpg', 'Daniel_Noteboom')
# fc.update('bryan1.jpg', 'Bryan_Djunaedi')

# print "testing evan test.jpg..." + str(fc.predict('test.jpg'))
# print "testing evan evan1.jpg..." + str(fc.predict('evan1.jpg'))
# print "testing daniel daniel1.jpg..." + str(fc.predict('daniel1.jpg'))
# print "testing bryan bryan1.jpg..." + str(fc.predict('bryan1.jpg'))