#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import requests, os, tqdm, re, pathlib, time
from pyquery import PyQuery as pq
from PIL import Image
from bs4 import BeautifulSoup

class Command(BaseCommand):
	help = 'Use this script to crawl suit pic from https://www.efshop.com.tw'
	domain = 'https://www.efshop.com.tw/'
	# 352: 季節精選 > 條紋系列
	# 229 : 品牌嚴選 > 百搭基本款
	# 9  : 上衣類 > 長版上衣
	# 13 : 上衣類 > 印圖上衣
	# 11 : 上衣類 > 洋裝
	# 208: 上衣類 > 襯衫
	# 18 : 上衣類 > 外套
	start_url = ['https://www.efshop.com.tw/category/352/1', 
				'https://www.efshop.com.tw/category/229/1', 
				'https://www.efshop.com.tw/category/9/1', 
				'https://www.efshop.com.tw/category/13/1', 
				'https://www.efshop.com.tw/category/11/1', 
				'https://www.efshop.com.tw/category/208/1', 
				'https://www.efshop.com.tw/category/18/1']
	pic_type = 'suit_efshop'
	pathlib.Path(pic_type).mkdir(parents=True, exist_ok=True)
	def handle(self, *args, **options):
		name_dict = {}
		for url in self.start_url:
			res = requests.get(url)
			soup = BeautifulSoup(res.text, 'lxml')
			if soup.select('.pageTag a'):
				max_page = int(soup.select('.pageTag a')[-2].text)
			else:
				max_page = 1
			print('max_page:', max_page)
			for page in range(1, max_page+1):
				page_url = url[:-1]+str(page)
				page_res = requests.get(page_url)
				page_soup = BeautifulSoup(page_res.text, 'lxml')
				print('start crawling page', page_url)
				for img in page_soup.select('.pro_img img'):
					img_name = img['alt']
					img_url = img['src']
					img_res = requests.get(img_url)
					filename = ''
					if img_name not in name_dict:
						name_dict[img_name] = 0
						filename = img_name+'.jpg'
					else:
						name_dict[img_name] += 1
						filename = img_name+'_{}.jpg'.format(name_dict[img_name])
					with open(self.pic_type+'/'+filename, 'wb') as file:
						file.write(img_res.content)
						print('got image', filename)
		self.stdout.write(self.style.SUCCESS('finish crawling https://www.efshop.com.tw !!!'))