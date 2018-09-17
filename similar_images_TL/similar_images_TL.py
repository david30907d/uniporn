"""

 similar_images_tl.py  (author: Anson Wong / Chang Tai Wei)

 We find similar images in a database by using transfer learning
 via a pre-trained VGG image classifier. We plot the 5 most similar
 images for each image in the database, and plot the tSNE for all
 our image feature vectors.

"""
import os
from pathlib import Path

import numpy as np

import face_recognition
import keras
import tensorflow as tf
import tqdm
import subprocess
import pickle
from keras.applications.inception_resnet_v2 import (InceptionResNetV2,
                                                    preprocess_input)
from keras.preprocessing import image as keras_image
from PIL import Image
from src.kNN import kNN
from src.plot_utils import plot_query_answer
from src.sort_utils import find_topk_unique
from src.tSNE import plot_tsne

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
CONFIG = tf.ConfigProto()
CONFIG.gpu_options.allow_growth = True
SESS = tf.Session(config=CONFIG)
keras.backend.set_session(SESS)


def extract_face_feature(dirpath='db'):
    '''
    A script which can visualize picture's embedding
    '''
    # ================================================
    # Load pre-trained model and remove higher level layers
    # ================================================
    print("Loading inception_resnet_v2 pre-trained model...")
    model = InceptionResNetV2(weights='imagenet', include_top=False) 

    # ================================================
    # Read images and convert them to feature vectors
    # ================================================
    img_list, filename_heads = [], []
    print("Reading images from '{}' directory...\n".format(dirpath))
    for file_path in tqdm.tqdm(Path(dirpath).iterdir()):
        # Process filename
        if file_path.suffix.lower() not in [".jpg", ".jpeg"]:
            continue
        # also maintain filename list
        filename_heads.append(file_path)

        # Read image file
        # numpy format
        origin_image_numpy = face_recognition.load_image_file(file_path)
        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model
        # and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        face_locations = face_recognition.face_locations(origin_image_numpy)
        # face_locations = face_recognition.face_locations(origin_image_numpy, model='cnn')
        if len(face_locations) != 1:
            # means there are multiple faces in a picture
            # discard this picture
            continue
        else:
            face_location = face_locations[0]
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        # You can access the actual face itself like this:
        face_image_numpy = origin_image_numpy[top:bottom, left:right]
        face_image_pil = Image.fromarray(face_image_numpy).resize((98, 98), Image.BILINEAR)
        # Pre-process for model input
        face_image_numpy = keras_image.img_to_array(face_image_pil)

        # append data to list
        face_image_numpy = np.expand_dims(face_image_numpy, axis=0)
        if len(img_list) > 0:
            img_list = np.concatenate((img_list, face_image_numpy))
        else:
            img_list = face_image_numpy

    img_list = preprocess_input(img_list)
    predicts = model.predict(img_list).reshape(len(img_list), -1)
    pickle.dump(dict(zip(filename_heads, predicts)), open('face_features-{}.pkl'.format(dirpath), 'wb'))

extract_face_feature('林志玲')
extract_face_feature('porn')