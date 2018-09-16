#!/usr/bin/env python

#The MIT License (MIT)
#Copyright (c) 2016 Massimiliano Patacchiola
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
from pathlib import Path

import cv2
import numpy as np
import face_recognition
import tensorflow as tf
from deepgaze.head_pose_estimation import CnnHeadPoseEstimator
from keras.preprocessing import image as keras_image
from PIL import Image
from scipy.spatial.distance import cosine

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
CONFIG = tf.ConfigProto()
CONFIG.gpu_options.allow_growth = True
SESS = tf.Session(config=CONFIG)
MY_HEAD_POSE_ESTIMATOR = CnnHeadPoseEstimator(SESS) #Head pose estimation object

# Load the weights from the configuration folders
MY_HEAD_POSE_ESTIMATOR.load_roll_variables(os.path.realpath("../../etc/tensorflow/head_pose/roll/cnn_cccdd_30k.tf"))
MY_HEAD_POSE_ESTIMATOR.load_pitch_variables(os.path.realpath("../../etc/tensorflow/head_pose/pitch/cnn_cccdd_30k.tf"))
MY_HEAD_POSE_ESTIMATOR.load_yaw_variables(os.path.realpath("../../etc/tensorflow/head_pose/yaw/cnn_cccdd_30k.tf"))
img_dict = {}

def get_head_pose_estimation(file_name):
    origin_image_numpy = face_recognition.load_image_file(file_name)
    # See also: find_faces_in_picture_cnn.py
    face_locations = face_recognition.face_locations(origin_image_numpy)
    if len(face_locations) != 1:
        # means there are multiple faces in a picture
        # discard this picture
        return None
    else:
        face_location = face_locations[0]
    # Print the location of each face in this image
    top, right, bottom, left = face_location
    # You can access the actual face itself like this:
    face_image_numpy = origin_image_numpy[top:bottom, left:right]
    face_image_pil = Image.fromarray(face_image_numpy).resize((100, 100), Image.BILINEAR)
    face_image_numpy = keras_image.img_to_array(face_image_pil)
    print("Processing image ..... " + file_name)
    # image = cv2.imread(file_name) #Read the image with OpenCV
    # Get the angles for roll, pitch and yaw
    roll = MY_HEAD_POSE_ESTIMATOR.return_roll(face_image_numpy)  # Evaluate the roll angle using a CNN
    pitch = MY_HEAD_POSE_ESTIMATOR.return_pitch(face_image_numpy)  # Evaluate the pitch angle using a CNN
    yaw = MY_HEAD_POSE_ESTIMATOR.return_yaw(face_image_numpy)
    return roll[0, 0, 0], pitch[0, 0, 0], yaw[0, 0, 0]

def cal_sim_of_folder(folder_name):
    for file_name in Path(folder_name).iterdir():
        file_name = str(file_name)
        head_pose = get_head_pose_estimation(file_name)
        if head_pose:
            img_dict[file_name] = head_pose

def most_similar(sim_dict, query):
    return sorted([(key, 1- cosine(value, sim_dict[query])) for key, value in sim_dict.items()], key=lambda x:-x[1])

if __name__ == '__main__':
    class MyEncoder(json.JSONEncoder):
        '''
        use this to encode numpy array into json format
        '''
        def default(self, obj):
            if isinstance(obj, np.floating):
                return float(obj)
            else:
                return super(MyEncoder, self).default(obj)

    cal_sim_of_folder('porn')
    cal_sim_of_folder('林志玲')
    json.dump(img_dict, open('pic_similarity.json', 'w'), cls=MyEncoder)
