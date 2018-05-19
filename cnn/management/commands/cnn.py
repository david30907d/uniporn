from django.core.management.base import BaseCommand, CommandError
from cnn import *
class Command(BaseCommand):
	help = 'use this cmd tar all folder we crawled from web !!!'

	def add_arguments(self, parser):
	    parser.add_argument('train', type=bool, default=False)
	    parser.add_argument('img', type=str, default='')
	    parser.add_argument('url', type=str, default='')

	def handle(self, *args, **options):
		pcr = NNPCR()
		if options['train']:
			pcr.train()
			pcr.saveModel('./'+'nnmodel.bin')
		elif options['img']:
			fileName = options['img']
			pcr.loadModel('nnmodel.bin')
			print(pcr.predict([fileName])[0])
		elif mode == 'url':
			url = options['url']
			with open('tmp.jpg', 'wb') as f:
				f.write(urlopen(url).read())
			pcr.loadModel('nnmodel.bin')
			print(pcr.predict(['tmp.jpg'])[0])
			os.remove('tmp.jpg')
		self.stdout.write(self.style.SUCCESS('finish building cnn'))