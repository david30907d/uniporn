#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time
from pyquery import PyQuery as pq

class Command(BaseCommand):
	help = 'Use this script to crawl hot pic from http://www.timliao.com'
	domain = 'http://www.timliao.com/bbs/'
	start_url = 'http://www.timliao.com/bbs/forumdisplay.php?fid=18&page='
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
				lady_url, dir_name = self.domain + lady_href, lady.text()

				# start parsing this lady's page
				print('start crawling page {}, inner page {}'.format(page_num, dir_name))
				subprocess.call(['mkdir', dir_name])

				inner_res = requests.get(lady_url)
				inner_res.encoding = inner_res.apparent_encoding
				inner_soup = pq(inner_res.text)
				print('There\'s {} pictures in total'.format(len(list(inner_soup('img.imglimit').items()))))
				for index, img in enumerate(inner_soup('img.imglimit').items()):
					if os.path.exists(os.path.join(dir_name, str(index)+'.jpg')):
						print('already have {}, continue'.format(str(index)+'.jpg'))
						continue

					img_src = img.attr('src')
					filename_extension = '.' + img_src.split('.')[-1][:3]
					if '.jpg' in filename_extension or '.png' in filename_extension:
						try:
							img_binary = requests.get(img_src, stream=True).content
						except requests.ConnectionError as e:
							print('Cannot save pic {}'.format(index))
							continue
						if index == 0:
							file_name = dir_name + filename_extension
						else:
							file_name = str(index) + filename_extension
						with open(os.path.join(dir_name, file_name), 'wb') as f:
							f.write(img_binary)
						print('got image {}'.format(file_name))
		self.stdout.write(self.style.SUCCESS('finish crawling http://www.timliao.com !!!'))