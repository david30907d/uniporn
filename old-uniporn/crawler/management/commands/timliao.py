#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time
from pyquery import PyQuery as pq
from PIL import Image

class Command(BaseCommand):
	help = 'Use this script to crawl hot pic from http://www.timliao.com'
	domain = 'http://www.timliao.com/bbs/'
	start_url = 'http://www.timliao.com/bbs/forumdisplay.php?fid=18&page='
	pic_type = 'hybrid_'

	def handle(self, *args, **options):
		first_res = requests.get(self.start_url)
		first_dom = pq(first_res.text)
		max_page = first_dom('.p_redirect+ .p_redirect')[0].attrib['href'].split('page=')[-1]
		max_page = int(max_page)
		for page_num in tqdm.tqdm(range(1, max_page+1)):
			# iterate through all pages
			# and get DOM by requests and PyQuery
			page_num = str(page_num)
			res = requests.get(self.start_url + page_num)
			res.encoding = res.apparent_encoding
			dom = pq(res.text)

			# iterate all ladies in a single page
			for lady in dom('.subject a').items():
				lady_href = lady.attr('href')
				# ad item in timliao pages wont have href attribute.
				if not lady_href:continue

				# get lady_url and dir_name
				lady_url, dir_name = self.domain + lady_href, self.pic_type + lady.text().replace('/', '')

				# start parsing this lady's page
				print('start crawling page {}, inner page {}'.format(page_num, dir_name))
				subprocess.call(['mkdir', dir_name])
				if os.path.exists(os.path.join(dir_name, 'done')):
					print('already finish this page!!!')
					continue

				inner_res = requests.get(lady_url)
				inner_res.encoding = inner_res.apparent_encoding
				inner_soup = pq(inner_res.text)
				print('There\'s {} pictures in total'.format(len(list(inner_soup('img.imglimit').items()))))
				for index, img in enumerate(inner_soup('img.imglimit').items()):
					img_src = img.attr('src')
					# this filename extension is just guess
					# timliao web also has wrong filename extension on dom
					# so need to use PIL to check later...
					guessed_filename_extension = '.' + img_src.split('.')[-1][:3].upper() 
					if 'JPG' in guessed_filename_extension:
						guessed_filename_extension = guessed_filename_extension.replace('JPG', 'JPEG')
					if index == 0:
						file_name_prefix = dir_name
					else:
						file_name_prefix = str(index)
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
						print('Cannot save pic {}'.format(guess_filename))
						continue
					except OSError as e:
						print('Cannot save pic {}'.format(guess_filename))
						continue
					except requests.packages.urllib3.exceptions.ProtocolError as e:
						for _ in range(3):
							try:
								img_binary = requests.get(img_src, stream=True)
								img = Image.open(img_binary.raw)
								# get correct filename extension with PIL function
								filename_extension = '.' + img.format

								correct_file_name = file_name_prefix + filename_extension
								img.save(os.path.join(dir_name, correct_file_name))
								print('got image {}'.format(correct_file_name))
								break
							except Exception as e:
								time.sleep(3)

				# save file done as a flag
				with open(os.path.join(dir_name, 'done'), 'w') as f:
					pass
		self.stdout.write(self.style.SUCCESS('finish crawling http://www.timliao.com !!!'))