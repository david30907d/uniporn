from django.core.management.base import BaseCommand, CommandError
import subprocess, os, tqdm, pathlib, shutil

class Command(BaseCommand):
	help = 'use this cmd tar all folder we crawled from web !!!'
	ignore_folder = ['./.git', './.gitignore', './gan', './crawler', './README.md', './manage.py', './requirements.txt', './web', './venv', './uniporn']

	def add_arguments(self, parser):
	    parser.add_argument('pic_type', type=str)

	def handle(self, *args, **options):
		tar_name = options['pic_type']+'.tar.gz'
		# remove the folder first
		shutil.rmtree(options['pic_type'])
		# create a folder for this kind of pics.
		pathlib.Path(options['pic_type']).mkdir(parents=True, exist_ok=True)

		for (dir_path, dir_names, file_names) in tqdm.tqdm(os.walk('.')):
			if not dir_names and not {dir_path for ig in self.ignore_folder if ig in dir_path} and dir_path.startswith('./'+options['pic_type']):
				for file_name in file_names:
					subprocess.call(['cp', os.path.join(dir_path, file_name), options['pic_type']])

		subprocess.call(['tar', 'zcvf', tar_name, options['pic_type']])
		self.stdout.write(self.style.SUCCESS('compress {} finish !!!'.format(tar_name)))