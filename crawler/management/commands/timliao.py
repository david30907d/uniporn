#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time
from pyquery import PyQuery as pq

class Command(BaseCommand):
	help = 'Use this script to crawl hot pic from http://www.timliao.com'
	domain = 'http://www.timliao.com/bbs'
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
				print('start crawling inner page {}'.format(dir_name))
				subprocess.call(['mkdir', dir_name])
				inner_res = requests.get(lady_url)
				res.encoding = res.apparent_encoding
				inner_dom = pq(inner_res.text)
				for index, img in enumerate(inner_dom('.imglimit')):
					img_binary = requests.get(img.attr('src'), stream=True)
					with open(os.join(dir_name, str(index)+'.jpg'), 'wb') as f:
						f.write(img_binary)


		self.stdout.write(self.style.SUCCESS('finish crawling http://www.keaitupian.com !!!'))