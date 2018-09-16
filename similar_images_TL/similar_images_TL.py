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


def main():
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
    img_list, filename_heads, origin_image_list = [], [], []
    path = "db"
    print("Reading images from '{}' directory...\n".format(path))
    for index, file_path in enumerate(tqdm.tqdm(Path(path).iterdir())):
        if index == 50:
            break
        # Process filename
        head, ext = file_path.name, file_path.suffix
        if ext.lower() not in [".jpg", ".jpeg"]:
            continue
        # also maintain filename list
        filename_heads.append(head)

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

        # use origin image to do visualization
        origin_image_pil = Image.fromarray(origin_image_numpy).resize((224, 224), Image.BILINEAR)
        origin_image_numpy = keras_image.img_to_array(origin_image_pil)

        # append data to list
        face_image_numpy = np.expand_dims(face_image_numpy, axis=0)
        origin_image_numpy = np.expand_dims(origin_image_numpy, axis=0)
        if len(img_list) > 0:
            img_list = np.concatenate((img_list, face_image_numpy))
            origin_image_list = np.concatenate((origin_image_list, origin_image_numpy))
        else:
            img_list = face_image_numpy
            origin_image_list = origin_image_numpy

    img_list = preprocess_input(img_list)
    predicts = model.predict(img_list).reshape(len(img_list), -1)
    origin_image_list = origin_image_list.astype('uint8')
    print("origin_image_list.shape = {}".format(origin_image_list.shape))
    print("predicts.shape = {}\n".format(predicts.shape))

    # ===========================
    # Find k-nearest images to each image
    # ===========================
    n_neighbours = 5 + 1  # +1 as itself is most similar
    knn = kNN()  # kNN model
    knn.compile(n_neighbors=n_neighbours, algorithm="brute", metric="cosine")
    knn.fit(predicts)

    # ==================================================
    # Plot recommendations for each image in database
    # ==================================================
    output_rec_dir = Path('output', 'rec')
    if not output_rec_dir.exists():
        output_rec_dir.mkdir()
    sample_num = 10
    _, ypixels, xpixels, _ = origin_image_list.shape
    for ind_query in range(sample_num):
        # Find top-k closest image feature vectors to each vector
        print("[{}/{}] Plotting similar image recommendations \
        for: {}".format(ind_query+1, sample_num, filename_heads[ind_query]))
        distances, indices = knn.predict(np.array([predicts[ind_query]]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, n_neighbours)

        # Plot recommendations
        rec_filename = Path(output_rec_dir, "{}_rec.png".format(filename_heads[ind_query]))
        x_query_plot = origin_image_list[ind_query].reshape((-1, ypixels, xpixels, 3))
        x_answer_plot = origin_image_list[indices].reshape((-1, ypixels, xpixels, 3))
        print('==================')
        print(filename_heads[ind_query])
        print([filename_heads[i] for i in indices[0]])
        # face_swap(filename_heads, ind_query, indices)
        plot_query_answer(x_query=x_query_plot,
                          x_answer=x_answer_plot[1:],  # remove itself
                          filename=str(rec_filename))

    # # ===========================
    # # Plot tSNE
    # # ===========================
    # output_tsne_dir = Path("output")
    # if not output_tsne_dir.exists():
    #     output_tsne_dir.mkdir()
    # tsne_filename = Path(output_tsne_dir, "tsne.png")
    # print("Plotting tSNE to {}...".format(tsne_filename))
    # plot_tsne(origin_image_list, predicts, str(tsne_filename))

def face_swap(filename_heads, ind_query, indices):
    for i in indices[0]:
        subprocess.call(['python', '../../FaceSwap/main.py', '--src', Path('db', filename_heads[ind_query]+'.jpg'), '--dst',Path('db', filename_heads[i]+'.jpg'), '--out', Path('output', 'faceswap', filename_heads[ind_query]+'.jpg'), '--correct_color'])

# Driver
if __name__ == "__main__":
    main()
