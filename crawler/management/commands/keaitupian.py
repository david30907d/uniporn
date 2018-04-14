from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time
from bs4 import BeautifulSoup
class Command(BaseCommand):
	help = 'use this cmd to crawl hot girl pic from huaban !!!'
	domain = 'http://www.keaitupian.com'
	start_urls = ['http://www.keaitupian.com/girl/list_1_1.html', 'http://www.keaitupian.com/meinv/qingchun/list_47_1.html']
	def handle(self, *args, **options):
		for start_url in self.start_urls:
			res = requests.get(start_url)
			soup = BeautifulSoup(res.text)
			maxPageNum = int(soup.select('strong')[0].text)
			print('There is {} pages in total'.format(maxPageNum))

			for pageNum in tqdm.tqdm(range(1, maxPageNum + 1)):
				print('===============================')
				print('page No.{}'.format(pageNum))
				print('===============================')
				res = requests.get(start_url.replace('_1.html', '_{}.html'.format(pageNum)))
				res.encoding = res.apparent_encoding
				soup = BeautifulSoup(res.text)

				for people in soup.select('#post'):
					dirName = people.select('img')[0]['alt']
					print('Crawling page {} now'.format(dirName))
					subprocess.call(['mkdir', dirName])
					inner_url = self.domain + people.select('a')[0]['href']
					inner_soup = BeautifulSoup(requests.get(inner_url).text)
					inner_pages = len(inner_soup.select('.pagelist a')) - 3

					for i in range(1, inner_pages+1):
						if i != 1:		
							inner_soup = BeautifulSoup(requests.get(inner_url.replace('.html', '_{}.html'.format(i))).text)
						for img in inner_soup.select('#post img'):
							filename = img['src'].split('/')[-1]
							if os.path.exists(os.path.join(dirName, filename)): 
								print('already has this img, continue')
								continue

							imgBinary = requests.get(self.domain + img['src'], stream=True, timeout=10).content
							# time.sleep(5)
							with open(os.path.join(dirName, filename), 'wb') as f:
								f.write(imgBinary)
								print('got Image:{}'.format(os.path.join(dirName, filename)))
		self.stdout.write(self.style.SUCCESS('finish crawling http://www.keaitupian.com !!!'))