from django.core.management.base import BaseCommand, CommandError
from cnn import *
import scipy
from glob import glob
from PIL import Image
import numpy as np
class Command(BaseCommand):
	help = 'use this cmd to generate Training Datasets or testing Datasets !!!'

	def add_arguments(self, parser):
		parser.add_argument('--type', type=str, default=False)

	@staticmethod
	def pilmerge(output_im, input_im):
	    list_im = [output_im, input_im]
	    imgs    = [ Image.open(i) for i in list_im ]
	    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
	    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	    # save that beautiful picture
	    imgs_comb = Image.fromarray( imgs_comb)
	    imgs_comb.save('merge.jpg')

	def handle(self, *args, **options):
		pcr = NNPCR()
		pcr.loadModel('nnmodel.bin')
		result = pcr.predict(['tmp.jpg'])[0]

		pilmerge('1.jpg', '2.jpg')

		self.stdout.write(self.style.SUCCESS('finish generating Datasets'))