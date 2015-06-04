from face_compare import FaceComparer

fc = FaceComparer()
fc.train('c1')
print "testing evan test.jpg..." + str(fc.predict('test.jpg'))
print "testing evan evan1.jpg..." + str(fc.predict('test.jpg'))
print "testing daniel daniel1.jpg..." + str(fc.predict('daniel1.jpg'))
print "testing bryan bryan1.jpg..." + str(fc.predict('bryan1.jpg'))