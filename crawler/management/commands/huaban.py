from django.core.management.base import BaseCommand, CommandError
import subprocess, requests, os, tqdm, time, json

class Command(BaseCommand):
	help = 'use this cmd to crawl hot girl pic from huaban !!!'
	increment = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
	headers = {
	  "Host": "huaban.com",
	  "Connection": "keep-alive",
	  "Accept": "application/json",
	  "X-Requested-With": "XMLHttpRequest",
	  "X-Request": "JSON",
	  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
	  "Referer": "http://huaban.com/explore/qingchunkeaimeinv/",
	  "Accept-Encoding": "gzip, deflate",
	  "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
	  "Cookie": "_uab_collina=152317268727852028701332; referer=https%3A%2F%2Fwww.google.com.tw%2F; sid=58C6GmwHuj61Pa9hTefcqOBTm21.SJEE7BQ2%2BSoCo2Yp66kfuPqVP%2FaPqljYkG99459lxdk; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAC3UlEQVRYR%2BWVvWtUQRTFfzfamCABiSI2FlYhjYovIhb7tAiIohYhRRrRmMVGUiSg%2F4CgECTBQtmoYBMk2CiKEFB3iSBmJZ0oBkUNdkFiE%2FGDHbmzM8vkZT%2FytUZwqvfum5l3z7nn3CsYYwAa5%2BcZ6e0lk06TS6U0ZJcRuQI8FsiVgkt4MNACDAN9ArNLOFJ1y9DXIZtnpSX%2FHRDgNfAQeK8sO7Z3AcccS%2FptP%2FAyiGlF9NwlYBTodXtHgG7gE3AEOADcArqAfmC7xgXe%2BAosuyLdo%2Fq%2FRStWaRlQzaVdQo1eOsBxPSFw28BllWIAPAPcBTT5J44ITfKigTOJc7EjoXTfioFU84iBVuA8MKC2Cj1giu%2BeaU1IK1HyiCPBArDeKwK%2BAPSEBDjCSgD%2FKhCgDbjjZHIqqEgSiErxhfuu%2B%2FR9QSXXA0gEaEdTj2iFbGdLSMsCAeaBQeCa84NP3jIfSC%2BzKiC%2B9Xp%2FxNks%2BSiy7TjwTE%2FwQzWqmkkZVfNPANcDZ3kTbwOyLh76zMf8ESVEZabnrjpJ6jd7Rh%2BWbPbKDVpktTNgLc7XDYjJ5qeAPS7JBxJHJ0zuVQcFM4bQDNhYCMI8mxxEpB%2FDNxqkS1L7xpMgK%2B0JgWz5sYmTH9qYbp5lYsdHe0VpIK6kIg7MTJiwyU32YaRL4ujgAhBFkBkaJA2F1uXuCYF0T%2B9m6%2Fcmplq%2BrBGQIsOHJY72%2BqQto8rQoXZtAKVlsvn7Nq6Vez7Zxm%2B5h5gbkmrXhmBXtT1JaSmYmaa5NQJSJiGTzY8jMpiUja2eMU89wOS7A1JxT12BLGJR5WPMgMRRxyLt%2F%2FNAip44x0bTyS9Ol5NVLbYDaa1jRQJ5YeRoOVnV0v%2B6e2ShwaUT4V05WVkgYdcqFDqSTaLWnrp7JEhgDMzNZLeqNUeKXU7O%2BrlSbo5o7OeGQv%2BjnW%2F5vHkO3371bt%2BCVzVHKs6eOnyo22SvQ65Vr6wF5A8JEnU3FTJQBgAAAABJRU5ErkJggg%3D%3D%2CWin32.1920.1080.24; __auc=88b27c2b162a42abdec77a7bcc6; _ga=GA1.2.1469391108.1523172687; UM_distinctid=162a42abf5123-0f024daeb8a58d-b34356b-1fa400-162a42abf5622; CNZZDATA1256903590=1012126087-1523172432-null%7C1523172432; md_href=http%3A%2F%2Fhuaban.com%2Fboards%2F15729161%2F%3Fmd%3Dnewbn%26beauty%3D; md=newbn; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1523173248056%26md%7Cnewbn%7C1523173249056"
	}
	if not os.path.exists('id_table.json'):
		json.dump({}, open('id_table.json', 'w'))
	id_table = json.load(open('id_table.json', 'r'))

	@classmethod
	def incrementStr(cls, string):
		bstr = bytearray(string, encoding='utf-8')
		result = []
		for i in bstr[::-1]:
			if i == 122:
				i = 48
				result.insert(0, i)
			else:
				i = cls.increment[cls.increment.index(i)+1]
				result.insert(0, i)
				break
		return bytes([i for i in  bstr[:len(bstr)-len(result)]]+result).decode()
	
	def handle(self, *args, **options):
		for i in tqdm.tqdm(range(2, 300)):
			dirName = 'huaban'+str(i)
			subprocess.call(['mkdir', dirName])
			if len(os.listdir(dirName)) == 20:
				print('already crawl {}, continue crawling !!!'.format(dirName))
				continue
			code = 'jfqv3nj8'

			while True:
				try:
					pics = requests.get('http://huaban.com/explore/qingchunkeaimeinv/?{}&page={}&per_page=20&wfl=1'.format(code, i), headers=self.headers, timeout=10).json()['pins']
					break
				except requests.exceptions.RequestException as e:  # This is the correct syntax
					time.sleep(10)
					continue
					
			code = self.incrementStr(code)
			for pic in pics:
				filename = str(pic['file']['id'])+'.jpg'
				pic_id = pic['file']['key']
				if self.id_table.get(pic_id, 0) == 3:
					break
				else:
					self.id_table[pic_id] = self.id_table.setdefault(pic_id, 0) + 1

				while True:
					try:
						imgBinary = requests.get('http://img.hb.aicdn.com/' + pic_id, stream=True, timeout=10).content
						break
					except requests.exceptions.RequestException as e:  # This is the correct syntax
						time.sleep(10)
						continue

				with open(os.path.join(dirName, filename), 'wb') as f:
					f.write(imgBinary)
				json.dump(self.id_table, open('id_table.json', 'w'))
				time.sleep(30)
		self.stdout.write(self.style.SUCCESS('build KCM success!!!'))