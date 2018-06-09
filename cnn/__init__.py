#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pickle
from urllib.request import urlopen
import sys
import os
import random
import cv2
from  PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.python.ops import init_ops
from tensorflow.contrib.losses.python.losses import loss_ops
import logging

FILE_SEED = 42
IMG_SIZE = 128


def loadCache(fname):
	return pickle.load(open(fname, 'rb'))


def saveCache(obj, fileName):
	pickle.dump(obj, open(fileName + '.tmp', 'wb'), -1)
	os.rename(fileName + '.tmp', fileName)


def loadDir(dirName):
	files = os.listdir(dirName)
	fnames = []
	for f in files:
		if f.endswith('.png') or f.endswith('.PNG'):
			continue
		fileName = dirName + '/' + f
		fnames.append(fileName)
	return fnames


def loadFileLists():
	random.seed(FILE_SEED)

	positiveFiles = sorted(loadDir('porn'))
	negativeFiles = sorted(loadDir('nonporn'))
	trashFiles = sorted(loadDir('trash'))

	random.shuffle(positiveFiles)
	random.shuffle(negativeFiles)
	random.shuffle(trashFiles)

	minLen = min(len(positiveFiles), len(negativeFiles), len(trashFiles))

	p20 = int(0.2 * minLen)

	testPositive = positiveFiles[:p20]
	testNegative = negativeFiles[:p20]
	testTrash = trashFiles[:p20]

	positiveFiles = positiveFiles[p20:]
	negativeFiles = negativeFiles[p20:]
	trashFiles = trashFiles[:p20]

	trainSamples = [(f, 2) for f in trashFiles] + [(f, 1) for f in positiveFiles] + [(f, 0) for f in negativeFiles]
	testSamples = [(f, 2) for f in testTrash] + [(f, 1) for f in testPositive] + [(f, 0) for f in testNegative]

	random.shuffle(trainSamples)
	random.shuffle(testSamples)

	trainX = [e[0] for e in trainSamples]
	trainY = [e[1] for e in trainSamples]
	testX = [e[0] for e in testSamples]
	testY = [e[1] for e in testSamples]

	return trainX, trainY, testX, testY


def loadFeatures(files):
	data = np.ndarray((len(files), IMG_SIZE * IMG_SIZE * 3))
	for n, f in enumerate(files):
		logging.debug('loading file #%d' % n)
		img = np.array(Image.open(f))
		h, w, _ = img.shape 
		if w > h:
			diff = w - h
			img = img[:, int(diff / 2): int(diff / 2) + h]
		elif w < h:
			diff = h - w
			img = img[int(diff / 2): int(diff / 2) + w, :]
		img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
		data[n] = img.ravel()
	return data


def denseToOneHot(labels_dense, num_classes):
	"""Convert class labels from scalars to one-hot vectors."""
	num_labels = labels_dense.shape[0]
	index_offset = np.arange(num_labels) * num_classes
	labels_one_hot = np.zeros((num_labels, num_classes))
	labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
	return labels_one_hot


def loadDataset():
	try:
		trainX, trainY, testX, testY = loadCache('nncache.bin')
	except: 
		trainX, trainY, testX, testY = loadFileLists()
		trainX = loadFeatures(trainX)
		testX = loadFeatures(testX)
		saveCache((trainX, trainY, testX, testY), 'nncache.bin')
	trainY = denseToOneHot(np.array(trainY), 2)
	testY = denseToOneHot(np.array(testY), 2)
	return trainX, trainY, testX, testY


class Batcher(object):

	def __init__(self, x, y, batchSize):
		assert len(y) >= batchSize
		self.__batchSize = batchSize
		self.__x = x
		self.__y = y
		self.shuffle()
		self.__currentIdx = 0
		self.__epochNumber = 0

	def shuffle(self):
		perm = np.arange(len(self.__y))
		np.random.shuffle(perm)
		self.__x = self.__x[perm]
		self.__y = self.__y[perm]

	def nextBatch(self):
		nextIdx = self.__currentIdx + self.__batchSize
		if nextIdx > len(self.__y):
			nextIdx = self.__batchSize
			self.__currentIdx = 0
			self.shuffle()
			self.__epochNumber += 1
		x = self.__x[self.__currentIdx:nextIdx]
		y = self.__y[self.__currentIdx:nextIdx]
		self.__currentIdx = nextIdx
		return x, y

	def getEpochNumber(self):
		return self.__epochNumber


def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)


def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)


def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

xavier = tf.contrib.layers.xavier_initializer


class Estimator(object):

	def __init__(self):
		self.x = tf.placeholder(tf.float32, shape=[None,  * IMG_SIZE * 3])
		self.y_ = tf.placeholder(tf.float32, shape=[None, 3])

		x_image = tf.reshape(self.x, [-1, IMG_SIZE, IMG_SIZE, 3])		# 256 * 256 * 3

		W_conv1 = tf.get_variable("W_conv1", shape=[3, 3, 3, 6], initializer=xavier())  #定義遮罩 (高度、寬度、通道數，遮罩數量)
		b_conv1 = tf.get_variable('b_conv1', [1, 1, 1, 6])
		h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
		h_pool1 = max_pool_2x2(h_conv1)								# 64

		W_conv2 = tf.get_variable("W_conv2", shape=[3, 3, 6, 6], initializer=xavier())
		b_conv2 = tf.get_variable('b_conv2', [1, 1, 1, 6])
		h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
		h_pool2 = max_pool_2x2(h_conv2)								# 32

		W_conv3 = tf.get_variable("W_conv3", shape=[3, 3, 6, 12], initializer=xavier())
		b_conv3 = tf.get_variable('b_conv3', [1, 1, 1, 12])
		h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
		h_pool3 = max_pool_2x2(h_conv3)								# 16

		W_conv4 = tf.get_variable("W_conv4", shape=[3, 3, 12, 24], initializer=xavier())
		b_conv4 = tf.get_variable('b_conv4', [1, 1, 1, 24])
		h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4) + b_conv4)
		h_pool4 = max_pool_2x2(h_conv4)								# 8

		h_pool4_flat = tf.reshape(h_pool4, [-1, 8 * 8 * 24])

		W_fc1 = tf.get_variable("W_fc1", shape=[8 * 8 * 24, 1024], initializer=xavier())
		b_fc1 = tf.get_variable('b_fc1', [1024], initializer=init_ops.zeros_initializer)
		h_fc1 = tf.nn.relu(tf.matmul(h_pool4_flat, W_fc1) + b_fc1)

		self.keep_prob = tf.placeholder(tf.float32)
		h_fc1_drop = tf.nn.dropout(h_fc1, self.keep_prob)

		W_fcO = tf.get_variable("W_fcO", shape=[1024, 3], initializer=xavier())
		b_fcO = tf.get_variable('b_fcO', [3], initializer=init_ops.zeros_initializer)

		logits = tf.matmul(h_fc1_drop, W_fcO) + b_fcO
		y_conv = tf.nn.softmax(logits)

		self.cross_entropy = loss_ops.softmax_cross_entropy(logits, self.y_)

		self.train_step = tf.train.AdagradOptimizer(0.01).minimize(self.cross_entropy)

		self.predictions = predictions = tf.argmax(y_conv, 1)

		correct_prediction = tf.equal(predictions, tf.argmax(self.y_, 1))
		self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		# for tensorboard
		tf.summary.scalar('loss', self.cross_entropy) 
		tf.summary.scalar('acc', self.accuracy)
		self.summary_op = tf.summary.merge_all()

	def train(self, x, y, keepProb=1.0):
		self.train_step.run(feed_dict={ self.x: x, self.y_: y, self.keep_prob: keepProb})

	def getLoss(self, x, y):
		return self.cross_entropy.eval(feed_dict={
			self.x: x,
			self.y_: y,
			self.keep_prob: 1.0,
		})

	def getAccuracy(self, x, y):
		return self.accuracy.eval(feed_dict={
			self.x: x,
			self.y_: y,
			self.keep_prob: 1.0,
		})

	def getSummary(self, x, y):
		return self.summary_op.eval(feed_dict={
			self.x: x,
			self.y_: y,
			self.keep_prob: 1.0,
		})

	def predict(self, x):
		return self.predictions.eval(feed_dict={
			self.x: x,
			self.keep_prob: 1.0,
		})


class NNPCR(object):

	def __init__(self):
		tf.set_random_seed(FILE_SEED)
		self.__sess = tf.InteractiveSession()
		self.__est = Estimator()
		self.val_summary_writer = tf.summary.FileWriter('tensorboard' + '/validation', graph=self.__sess.graph)
		self.summary_writer = tf.summary.FileWriter('tensorboard' + '/training', graph=self.__sess.graph)

	def train(self, numIterations=600):
		logging.info('loading dataset')
		trainX, trainY, testX, testY = loadDataset()
		batcher = Batcher(trainX, trainY, 128)

		self.__sess.run(tf.initialize_all_variables())

		logging.info('training')

		for step in range(numIterations):
			batch = batcher.nextBatch()
			self.__est.train(batch[0], batch[1], keepProb=0.5)

			if step % 50 == 0:
				en = batcher.getEpochNumber()

				# val
				val_acc = self.__est.getAccuracy(testX, testY)
				val_loss = self.__est.getLoss(testX, testY)
				val_summary = self.__est.getSummary(testX, testY)

				# training
				acc = self.__est.getAccuracy(batch[0], batch[1])
				loss = self.__est.getLoss(batch[0], batch[1])
				summary = self.__est.getSummary(batch[0], batch[1])
				logging.info('epoch %d, iteration %d, val_accuracy %f, val_loss %f, acc %f, loss %f' % (en, step, val_acc, val_loss, acc, loss))

				# for tensorboard
				self.summary_writer.add_summary(summary, step)
				self.val_summary_writer.add_summary(val_summary, step)

	def testAccuracy(self):
		logging.info('loading dataset')
		trainX, trainY, testX, testY = loadDataset()
		return self.__est.getAccuracy(trainX, trainY), self.__est.getAccuracy(testX, testY)

	def saveModel(self, fileName):
		saver = tf.train.Saver()
		saver.save(self.__sess, fileName)

	def loadModel(self, fileName):
		saver = tf.train.Saver()
		saver.restore(self.__sess, fileName)

	def predict(self, files):
		features = loadFeatures(files)
		return self.__est.predict(features)


def printUsage():
	print('Usage: ')
	print('  %s train                              - train model' % sys.argv[0])
	print('  %s file testImg.jpg                   - check given file' % sys.argv[0])
	print('  %s url http://sample.com/img.jpg      - check given url' % sys.argv[0])
	sys.exit(42)


if __name__ == '__main__':

	logging.basicConfig(format=u'[%(asctime)s %(filename)s:%(lineno)d %(levelname)s]  %(message)s', level=logging.INFO)

	pcr = NNPCR()

	if len(sys.argv) < 2:
		printUsage()
	mode = sys.argv[1]
	if mode == 'train':
		pcr.train()
		pcr.saveModel('./'+'nnmodel.bin')
	elif mode == 'file':
		if len(sys.argv) < 3:
			printUsage()
		fileName = sys.argv[2]
		pcr.loadModel('nnmodel.bin')
		print(pcr.predict([fileName])[0])
	elif mode == 'url':
		if len(sys.argv) < 3:
			printUsage()
		url = sys.argv[2]
		f = open('tmp.jpg', 'wb')
		f.write(urlopen(url).read())
		f.close()
		pcr.loadModel('nnmodel.bin')
		print(pcr.predict(['tmp.jpg'])[0])
		os.remove('tmp.jpg')
	else:
		printUsage()

