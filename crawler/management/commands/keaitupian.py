from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time
from bs4 import BeautifulSoup
class Command(BaseCommand):
	help = 'use this cmd to crawl hot girl pic from huaban !!!'
	domain = 'http://www.keaitupian.com'
	start_url = 'http://www.keaitupian.com/girl/list_1_1.html'
	def handle(self, *args, **options):
		res = requests.get(self.start_url)
		res.encoding = res.apparent_encoding
		soup = BeautifulSoup(res.text)
		for people in soup.select('#post'):
			dirName = people.select('img')[0]['alt']
			subprocess.call(['mkdir', dirName])
			inner_url = self.domain + people.select('a')[0]['href']
			inner_soup = BeautifulSoup(requests.get(inner_url).text)
			pages = len(inner_soup.select('.pagelist a')) - 3

			for i in range(1, pages+1):			
				for img in inner_soup.select('#post img'):
					imgBinary = requests.get(self.domain + img['src'], stream=True, timeout=10).content
					time.sleep(5)
					filename = img['src'].split('/')[-1]
					with open(os.path.join(dirName, filename), 'wb') as f:
						f.write(imgBinary)
				inner_soup = BeautifulSoup(requests.get(inner_url.replace('.html', '_{}.html'.format(i))).text)
		self.stdout.write(self.style.SUCCESS('finish crawling www.huaban.com !!!'))