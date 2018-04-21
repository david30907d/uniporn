#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import requests, os, tqdm, re, pathlib
from pyquery import PyQuery as pq
from PIL import Image

class Command(BaseCommand):
	help = 'Use this script to crawl hot pic from https://www.jkforum.net'
	domain = 'https://www.jkforum.net/'
	start_url = 'https://www.jkforum.net/forum-234-'
	def handle(self, *args, **options):
		first_res = requests.get(self.start_url + '1.html')
		first_dom = pq(first_res.text)
		max_page = re.match(r'.*-(.+?).html', first_dom('.last')[0].attrib['href']).group(1)
		max_page = int(max_page)
		for page_num in tqdm.tqdm(range(1, max_page+1)):
			# iterate through all pages
			# and get DOM by requests and PyQuery
			page_num = str(page_num)
			res = requests.get(self.start_url + page_num + '.html')
			res.encoding = res.apparent_encoding
			dom = pq(res.text)

			# iterate all ladies in a single page
			for lady in dom('.xw0 a').items():
				lady_href = lady.attr('href')

				# get lady_url and dir_name
				lady_url, dir_name = self.domain + lady_href, lady.text()

				# start parsing this lady's page
				print('start crawling page {}, inner page {}'.format(page_num, dir_name))

				# python's version of mkdir
				# which is portable
				pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True) 
				if os.path.exists(os.path.join(dir_name, 'done')):
					print('already finish this page!!!')
					continue

				inner_res = requests.get(lady_url, verify=True)
				inner_res.encoding = inner_res.apparent_encoding
				inner_soup = pq(inner_res.text)
				print('There\'s {} pictures in total'.format(len(list(inner_soup('.zoom').items()))))
				for index, img in enumerate(inner_soup('.zoom').items()):
					img_src = img.attr('file')
					if not img_src: continue
					# this filename extension is just guess
					# timliao web also has wrong filename extension on dom
					# so need to use PIL to check later...
					guessed_filename_extension = '.' + img_src.split('.')[-1][:3].upper() 
					if 'JPG' in guessed_filename_extension:
						guessed_filename_extension = guessed_filename_extension.replace('JPG', 'JPEG')
					file_name_prefix = '{}-{}'.format(dir_name, str(index))
					guess_filename = file_name_prefix + guessed_filename_extension

					# if there's already a file name in guessed_filename_extension
					# it means that guessed_filename_extension is equal to correct filename extension
					# so can skip this one.
					# if we didn't have any files named in guessed_filename_extension
					# these's two case:
					# 1. we didn't have one
					# 2. guessed_filename_extension is wrong, but we cannot figure it out till we download this picture and check with PIL...
					if os.path.exists(os.path.join(dir_name, guess_filename)):
						print('already have {}, continue'.format(guess_filename))
						continue

					try:
						img_binary = requests.get(img_src, stream=True)
						img = Image.open(img_binary.raw)
						# get correct filename extension with PIL function
						filename_extension = '.' + img.format

						correct_file_name = file_name_prefix + filename_extension
						img.save(os.path.join(dir_name, correct_file_name))
						print('got image {}'.format(correct_file_name))
					except requests.ConnectionError as e:
						print(e)
						print('Cannot save pic {}'.format(guess_filename))
						continue
					except OSError as e:
						print(e)
						print('Cannot save pic {}'.format(guess_filename))
						continue

				# save file done as a flag
				with open(os.path.join(dir_name, 'done'), 'w') as f:
					pass
		self.stdout.write(self.style.SUCCESS('finish crawling https://www.jkforum.net !!!'))