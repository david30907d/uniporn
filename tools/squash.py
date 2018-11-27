import os
import shutil
import argparse
from tqdm import tqdm


PARSER = argparse.ArgumentParser(description='Search some files')
PARSER.add_argument('-i', '--input', required=True, dest='input')
ARGS = PARSER.parse_args()
NEW_DIR = ARGS.input + '_squash'
os.makedirs(NEW_DIR, exist_ok=True)

for root, dirs, files in tqdm(os.walk(ARGS.input)):
	if not dirs:
		for f in files:
			new_fname = root.replace('/', '_') + f
			fpath = root + '/' + f
			os.rename(fpath, root + '/' + new_fname)
			shutil.copy(root + '/' + new_fname, NEW_DIR)
