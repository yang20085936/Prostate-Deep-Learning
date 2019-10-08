# -*- coding: utf-8 -*-
"""dalyell_week_5_assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZyIYlQd34W1kIbcMH4qZBMKPVxnlUjcl

# Sasha - Dalyell Group Week 5 Assignment
##The MNIST fashion dataset

Due: 13/09/2019

How to submit: after you finish working, save and download the document as a `.ipynb` file (File - Download .ipynb). Send through the `.ipynb` file. All cells are expected to run without errors. 

Data source: [MNIST Fashion dataset](https://github.com/zalandoresearch/fashion-mnist).

# Downloading the data

! wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz
! wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz
! wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz
! wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz
"""

import os
import gzip
import numpy as np
    
def load_mnist(path, kind='train'):

    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels-idx1-ubyte.gz'
                               %kind)
    images_path = os.path.join(path,
                               '%s-images-idx3-ubyte.gz'
                               %kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels

# Overriding the MNIST data

train_images, train_labels = load_mnist('.', 'train')
test_images, test_labels = load_mnist('.', 't10k')

"""------------------------------------------------"""

import keras # Importing required neural network module

# Preprocessing the data so that they can be provided to the neural network

# Image dimensions
img_rows, img_cols = 28, 28

# 1 since the images are greyscale
train_images = train_images.reshape(train_images.shape[0], img_rows, img_cols, 1)
test_images = test_images.reshape(test_images.shape[0], img_rows, img_cols, 1)

# Importing the pyplot module to view the images
from matplotlib import pyplot as plt

# Let's pick a random image
import random
random_index = random.randint(0, len(train_images[0])) # Choosing a random index
img = train_images[random_index, :, :, 0] # Retrieving the image

# Printing the image dimensions
print("Image dimensions are", img.shape) # 28 x 28

# Creating a list of the image label descriptions
label_desc = ["T-shirt/top",
              "Trouser",
              "Pullover",
              "Dress",
              "Coat",
              "Sandal",
              "Shirt",
              "Sneaker",
              "Bag",
              "Ankle boot"]

# Printing the image's label description
img_label = train_labels[random_index]
print("The image is a", label_desc[img_label])

# Plotting the image
plt.imshow(img)
plt.show()

# Normalise the data (so that they lie between 0 and 1)

train_images = train_images.astype('float32') / 255.0
test_images = test_images.astype('float32') / 255.0

# Checking the dimensions of the training and testing images

print('training shape:', train_images.shape) # (60000, 28, 28, 1)
print('testing shape:', test_images.shape) # (10000, 28, 28, 1)

# Similarly, preprocess the trainging and testing labels

train_labels = keras.utils.to_categorical(train_labels, 10)
test_labels = keras.utils.to_categorical(test_labels, 10)

# Define the deep learning structure

# Initialise the model, it's empty at the beginning
model = keras.models.Sequential()

# Add the first convolutional layer
model.add(keras.layers.Conv2D(32, kernel_size = (3,3), 
                              activation='relu', input_shape = (img_rows, img_cols, 1)))
# Add the first pooling layer
model.add(keras.layers.MaxPooling2D(pool_size = (2,2)))

# Similarly the second convolutional layer
model.add(keras.layers.Conv2D(64, (3,3), activation = 'relu'))
# The second pooling layer
model.add(keras.layers.MaxPooling2D(pool_size = (2,2)))

# Flatten the image (pulled into an array)
model.add(keras.layers.Flatten())
# Feed the array into a densely-connected neural network
model.add(keras.layers.Dense(128, activation = 'relu'))
# Use the softmax to map the output to probabilities
model.add(keras.layers.Dense(10, activation = 'softmax'))

# Configure the training details, e.g. what optimiser to use

model.compile(loss = keras.losses.categorical_crossentropy,
             optimizer = keras.optimizers.Adadelta(),
             metrics = ['accuracy'])

# Fit the model. The loss and accuracy will be outputed by default.

history = model.fit(train_images, train_labels,
          batch_size = 64,
          epochs = 20)

# Evaluate the performance

performance = model.evaluate(test_images, test_labels)
print('The loss is %.3f and the accuracy is %.3f on the test data' 
       % tuple(performance))
