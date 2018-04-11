from django.core.management.base import BaseCommand, CommandError
from collections import defaultdict
import os

class Command(BaseCommand):
	help = 'use this cmd to crawl hot girl pic from huaban !!!'
	def handle(self, *args, **options):
		sizeTable = defaultdict(list)
		for dirname, dirnames, filenames in os.walk('.'):
		    # print path to all subdirectories first.
		    if 'huaban' in dirname:
		        for f in filenames:
		            filepath = os.path.join(dirname, f)
		            sizeTable[filepath].append(os.stat(filepath).st_size)

		for k, v in sizeTable.items():
		    if len(v) > 1:
		        print('Repeated picture:' + k)
		self.stdout.write(self.style.SUCCESS('finish inspection !!!'))