import os

import tensorflow as tf
from tensorflow import keras

from keras import models, layers
from keras.applications import VGG16
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

from pykopt.KerasOptimizer import KerasOptimizer
from pykopt.Strategy import Strategy

import keras
from keras.datasets import mnist
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.models import Sequential, Model
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.optimizers import SGD, Adam, RMSprop
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from imutils import paths
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
import random
import cv2
import os
import numpy as np
from keras import backend as K
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers
from keras import optimizers
import ssl


# %% [code]
def custom_model():
    vgg = VGG16(weights='imagenet', classes=2, include_top=False, input_shape=(224, 224, 3))

    # Create the model
    model = models.Sequential()

    # Add the vgg convolutional base model
    model.add(vgg)

    model.add(layers.Flatten())
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.summary()

    return model


# %% [code]
def train_model(hyperparams):
    train_data = "/kaggle/input/covidct/Covid-CT/Train"
    validation_data = "/kaggle/input/covidct/Covid-CT/Test"

    batch_size = hyperparams["batch_size"]
    EPOCHS = hyperparams["epochs"]
    INIT_LR = hyperparams["learning_rate"]
    decay_rate = hyperparams["decay"]
    momentum = hyperparams["momentum"]
    width = 224
    height = 224

    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(rescale=1. / 255)

    # this is a generator that will read pictures found in
    # subfolers of 'data/train', and indefinitely generate
    # batches of augmented image data
    train_generator = train_datagen.flow_from_directory(
        train_data,
        target_size=(width, height),
        color_mode='rgb',
        batch_size=batch_size,
        shuffle=True,
        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels

    # this is the augmentation configurationw e will use for testing:
    # only rescaling
    validation_datagen = ImageDataGenerator(rescale=1. / 255)

    # this is a similar generator, for test data
    validation_generator = validation_datagen.flow_from_directory(
        validation_data,
        target_size=(width, height),
        batch_size=batch_size,
        color_mode='rgb',
        shuffle=False,
        class_mode='binary')

    nb_train_samples = len(train_generator.filenames)
    nb_validation_samples = len(validation_generator.filenames)

    # initialize the model
    print("[INFO] compiling model...")
    model = custom_model()
    opt = SGD(lr=INIT_LR, decay=decay_rate, momentum=momentum, nesterov=True)
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=EPOCHS,
        shuffle=True,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size)

    return history.history['val_accuracy']


# %% [code]
def run():
    optimizer = KerasOptimizer(max_iteration=10, initial_population=10, mutation_probability=0.01, crossover_prob=0.7)

    optimizer.select_optimizer_strategy(Strategy.MAXIMIZE)
    optimizer.add_hyperparameter('batch_size', [16, 32, 64, 128])
    optimizer.add_hyperparameter('epochs', [1, 5, 10, 20])
    optimizer.add_hyperparameter('learning_rate', [0.001, 0.01, 0.1])
    optimizer.add_hyperparameter('decay', [1e-6, 1e-7])
    optimizer.add_hyperparameter('momentum', [0.9, 0.0])
    optimizer.show_graph_on_end(show=False)
    optimizer.run(custom_model, train_model)


if __name__ == '__main__':
    run()