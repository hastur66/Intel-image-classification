import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img


model = tf.keras.models.load_model('intel_image_classifier_mobilenetv2.h5')

def trans_img(image_path):
    img = load_img(image_path)

    img_numpy_array = img_to_array(img)

    image_resize = np.resize(img_numpy_array, (300, 300, 3))

    image = np.expand_dims(image_resize, axis=0)

    return image


labels = {0: 'buildings', 1: 'forest', 2: 'glacier', 3: 'mountain', 4: 'sea', 5: 'street'}

def predictor(image, lables):
    model.predict(image)
    pred = model.predict(image)
    pred = np.argmax(pred)

    for key, value in labels.items():
        if pred == key:
            #print('The image is a ', value)
            msg = 'The image is a', value
            return msg