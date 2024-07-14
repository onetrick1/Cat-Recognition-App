import tensorflow 
from matplotlib import pyplot as plt
import cv2 as cv
import caer
import numpy as np
import os

def predicts(path):
    IMAGE_SIZE = (80,80)
    char_path = r'C:\Users\johnj\OneDrive\Desktop\Coding\Cat Recognition APP\Cat Images\Training Images' #the path where the data is imported


    characters = []
    for char in os.listdir(char_path):
        characters.append(char)

    model = tensorflow.keras.models.load_model('final_model.h5')

    img = cv.imread(path)

    def prepare(img):
        img = cv.resize(img, IMAGE_SIZE)
        img = caer.reshape(img, IMAGE_SIZE, 1)
        return img

    predictions = model.predict(prepare(img))
    final_predictions = predictions.tolist()
    final_predictions2 = final_predictions[0]

    temp1 = max(final_predictions2)
    temp2 = final_predictions2.index(temp1)
    cat_breed = characters[temp2]

    return cat_breed
