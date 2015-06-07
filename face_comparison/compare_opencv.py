import numpy as np
import cv2
import sys
import math
import os
import Queue
from PIL import Image

class FaceComparer:

	def __init__(self, dir):
		self.eigen  = cv2.createEigenFaceRecognizer(num_components=80)
		self.fisher = cv2.createFisherFaceRecognizer()
		self.lbph   = cv2.createLBPHFaceRecognizer()

		cascadePath = "../face_detection/haarcascade_frontalface_alt2.xml"
		self.face_cascade = cv2.CascadeClassifier(cascadePath)

		self.int_names = {}
		# self.name_ints = {}
		self.avg_width  = 0
		self.avg_height = 0
		self.thresholds = [8000,5000,240]#[6000, 5300, 220] #[7000, 5000, 250] #

		self.train(dir)

	def normalize(self, scores, thresholds):
		for s in range(len(scores)):
			scores[s] /= float(thresholds[s])
		return scores

	def prep_training_set(self, dir, look_for_faces):
		num_images = 0

		trains = []
		labels = []
		label = 0

		# store images as arrays and get average image size
		identities = os.listdir(dir)
		for identity in identities:
			self.int_names[label] = identity
			# self.name_ints[identity] = label
			images = os.listdir(dir+'/'+identity)
			for image in images:
				img = cv2.imread(dir+'/'+identity+'/'+image, cv2.IMREAD_GRAYSCALE)
				# img = cv2.imread(dir+'/'+identity+'/'+image)
				# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				# img = cv2.equalizeHist(img)
				detected_faces = self.face_cascade.detectMultiScale(img, 1.4, 1)
			  # OR
				# img_pil = Image.open(dir+'/'+identity+'/'+image).convert('L')
				# img = np.array(img_pil, 'uint8')
				# detected_faces = self.face_cascade.detectMultiScale(img)
				# print str(len(detected_faces)) + " faces added for " + identity
				
				if look_for_faces:
					for (x, y, w, h) in detected_faces:
						trains.append(img[y: y + h, x: x + w])
						labels.append(label)
					# trains.append(img)
					# labels.append(label)
					# w, h = img.shape[:2]
						self.avg_width += w
						self.avg_height += h
						num_images += 1
				else:
					trains.append(img)
					labels.append(label)
					w, h = img.shape[:2]
					self.avg_width += w
					self.avg_height += h
					num_images += 1
			label += 1
		self.avg_width /= float(num_images)
		self.avg_height /= float(num_images)

		# resize all images to average width and height
		for i in range(len(trains)):
			trains[i] = cv2.resize(trains[i], (int(self.avg_width), int(self.avg_height)))
			# cv2.imshow("Adding faces to training set...", trains[i])
			# cv2.waitKey(50)

		return trains, labels

	def train(self, dir):
		trains, labels = self.prep_training_set(dir, True)

		print self.int_names
		try:
			self.fisher.train(trains, np.asarray(labels))
			self.eigen.train(trains, np.asarray(labels))
			self.lbph.train(trains, np.asarray(labels))
		except:
			trains, labels = self.prep_training_set(dir, False)
			self.fisher.train(trains, np.asarray(labels))
			self.eigen.train(trains, np.asarray(labels))
			self.lbph.train(trains, np.asarray(labels))
		

	# returns the predicted identity of the test image
	def predict_test(self, test, thresholds):
		if thresholds is None:
			thresholds = self.thresholds
		img = cv2.imread(test, cv2.IMREAD_GRAYSCALE)
		img = cv2.equalizeHist(img)
		detected_faces = self.face_cascade.detectMultiScale(img, 1.4, 1)
		
		for (x, y, w, h) in detected_faces:
			face = cv2.resize(img[y: y+h, x:x+w], (int(self.avg_width), int(self.avg_height)))
			# cv2.imshow("Testing face:", face)
			# cv2.waitKey(50)
			p_eigen  = self.eigen.predict(face)
			p_fisher = self.fisher.predict(face)
			p_lbph   = self.lbph.predict(face)
			scores = self.normalize([p_eigen[1], p_fisher[1], p_lbph[1]], thresholds)
			# print "Prediction: " + str(self.int_names[p_eigen[0]])
			# print "Confidence: " + str(scores[0])
			# print "Prediction: " + str(self.int_names[p_fisher[0]])
			# print "Confidence: " + str(scores[1])
			# print "Prediction: " + str(self.int_names[p_lbph[0]])
			# print "Confidence: " + str(scores[2])

			min_n_score = sys.maxint
			prediction = 0
			for s in range(len(scores)):
				if scores[s] <= min_n_score:
					min_n_score = scores[s]
					prediction = s
			if prediction == 0:
				return (self.int_names[p_eigen[0]], 'EigenFaces')
			elif prediction == 1:
				return (self.int_names[p_fisher[0]], 'FisherFaces')
			else:
				return (self.int_names[p_lbph[0]], 'Linear Binary Pattern Histograms')

	# updating not supported for eigen nor fisher faces
	# def update(self, train, label):
	# 	train_img = cv2.imread(train, cv2. IMREAD_GRAYSCALE)
	# 	train_img = cv2.resize(train_img, (self.avg_width, self.avg_height))
	# 	if label in self.name_ints.keys():
	# 		self.fisher.update(train_img, self.name_ints[label])