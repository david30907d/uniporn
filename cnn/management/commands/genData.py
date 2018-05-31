from django.core.management.base import BaseCommand, CommandError
from cnn import *
import scipy
from glob import glob
from PIL import Image
import numpy as np
from os import listdir, mkdir
import cv2


class Command(BaseCommand):
    help = 'use this cmd to generate Training Datasets or testing Datasets !!!'

    def add_arguments(self, parser):
        parser.add_argument('--p2n', type=int, default=1)

    @staticmethod
    def pilmerge(output_im, input_im, num, path):
        list_im = [output_im, input_im]
        imgs    = [ Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        # save that beautiful picture
        imgs_comb = Image.fromarray( imgs_comb)
        imgs_comb.save(path + '/' + str(num) + '.jpg')

    def handle(self, *args, **options):
        pcr = NNPCR()
        pcr.loadModel('nnmodel.bin')
        flag = int(options['p2n'])

        files = listdir(".")
        files_list = []
        for ele in files:
            if 'hybrid' in ele:
                files_list.append(ele)
        
        for file in files_list:
            print(file)       
            images_path = listdir(file)
            nonporn_list = []
            porn_list = []
   
            for image in images_path:
                if '.JPEG' in image or '.PNG' in image:
                    image_path = file + "/" + image
                    
                    image = Image.open(image_path)                   #將圖片轉成RGB
                    if image.mode != 'RGB':
                        image = image.convert('RGB').save(image_path)
                      
                    result = pcr.predict([image_path])[0]

                    if result == 1:
                        porn_list.append(image_path)
                    else:
                        nonporn_list.append(image_path)

            
            if len(porn_list) == 0 or len(nonporn_list) == 0:
                continue
                
            if flag : newpath = "p2n" + file.split('hybrid')[1]
            else : newpath = "n2p" + file.split('hybrid')[1]
            try:
                mkdir(newpath)
            except:
                print('already has {} this dir'.format(newpath))

            num = 0
            for nonporn in nonporn_list:
                for porn in porn_list:
                    if flag : self.pilmerge(nonporn, porn, num, newpath)
                    else : self.pilmerge(porn, nonporn, num, newpath)
                    num += 1


        self.stdout.write(self.style.SUCCESS('finish generating Datasets'))
