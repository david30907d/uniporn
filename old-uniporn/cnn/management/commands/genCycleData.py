from django.core.management.base import BaseCommand, CommandError
from cnn import *
import random, subprocess, os, shutil, json
from sklearn.model_selection import train_test_split

class Command(BaseCommand):
	help = 'use this cmd to generate Training Datasets or testing Datasets for cycle gan!!!'

	def add_arguments(self, parser):
		parser.add_argument('--model', type=str, default='nnmodel.bin.origin')
		parser.add_argument('--porndir', type=str)
		parser.add_argument('--nonporndir', type=str)
		parser.add_argument('--folder', type=str)

	def handle(self, *args, **options):
		pcr = NNPCR()
		pcr.loadModel(options['model'])

		criteria = {
			options['porndir']: True,
			options['nonporndir']: False
		}

		refine_porn = []
		refine_nonporn = []

		for folder in [options['porndir'], options['nonporndir']]:
			for file in os.listdir(folder):
				filepath = os.path.join(folder, file)
				try:
					# there's some picture use CMYK
					# need to hanle this issue
					predict = pcr.predict([filepath])[0]
				except Exception as e:
					continue
				# if prediction meets criteria
				# means that i'm much more confident that this image belongs to thie category
				if bool(predict) == criteria[folder]:
					if bool(predict) == True:
						# porn
						refine_porn.append(filepath)
					else:
						# nonporn
						refine_nonporn.append(filepath)

		# train, test
		if os.path.isdir(options['folder']):
			shutil.rmtree(options['folder'])
		os.makedirs(os.path.join(options['folder'], 'testA'))
		os.makedirs(os.path.join(options['folder'], 'testB'))
		os.makedirs(os.path.join(options['folder'], 'trainA'))
		os.makedirs(os.path.join(options['folder'], 'trainB'))

		min_len = min((len(refine_nonporn), len(refine_porn)))
		refine_porn = refine_porn[:min_len]
		refine_nonporn = refine_nonporn[:min_len]
		X_train, X_test, y_train, y_test = train_test_split(refine_nonporn, refine_porn, test_size=0.33, random_state=42)
		# print(len(X_train), len(X_test), len(y_train), len(y_test))
		# json.dump(X_train, open('X_train.json', 'w'))
		# json.dump(y_train, open('y_train.json', 'w'))
		# json.dump(X_test, open('X_test.json', 'w'))
		# json.dump(y_test, open('y_test.json', 'w'))

		# move these pics to folder
		for path, filepaths in zip(['trainA', 'trainB', 'testA', 'testB'], [X_train, y_train, X_test, y_test]):
			for filepath in filepaths:
				print(filepath)
				shutil.move(filepath,  os.path.join(options['folder'], path))
		self.stdout.write(self.style.SUCCESS('finish generating Datasets'))