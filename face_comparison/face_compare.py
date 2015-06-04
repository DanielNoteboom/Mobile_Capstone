import numpy as np
import cv2
import sys
import math
import os
import Queue

class FaceComparer:

	def __init__(self):
		# self.eigen  = cv2.createEigenFaceRecognizer(threshold=100.0)
		self.fisher = cv2.createFisherFaceRecognizer()
		# self.lbph   = cv2.createLBPHFaceRecognizer()

		self.int_names = {}
		self.avg_width  = 0
		self.avg_height = 0

	def train(self, dir):
		num_images = 0

		trains = []
		labels = []
		label = 1

		# store images as arrays and get average image size
		identities = os.listdir(dir)
		for identity in identities:
			self.int_names[label] = identity
			images = os.listdir(dir+'/'+identity)
			for image in images:
				img = cv2.imread(dir+'/'+identity+'/'+image, cv2.IMREAD_GRAYSCALE)
				trains.append(img)
				labels.append(label)
				w, h = img.shape[:2]
				self.avg_width += w
				self.avg_height += h
				num_images += 1
			label += 1
		self.avg_width /= num_images
		self.avg_height /= num_images

		# resize all images to average width and height
		for i in range(len(trains)):
			trains[i] = cv2.resize(trains[i], (self.avg_width, self.avg_height))

		self.fisher.train(trains, np.asarray(labels))
		print self.int_names

	# returns the predicted identity of the test image
	def predict(self, test):
		test_img = cv2.imread(test, cv2.IMREAD_GRAYSCALE)
		test_img = cv2.resize(test_img, (self.avg_width, self.avg_height))
		predicted = self.fisher.predict(test_img)
		return self.int_names[predicted[0]]