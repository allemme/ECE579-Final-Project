# -*- coding: utf-8 -*-
"""final_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I6kqv3cqjOc629Zvt_EfsECJ_gVqTpzT

#Load Data

## <font color = 'blue'> The dataset is too large to send through a file, please access it thought the link below:

 https://drive.google.com/drive/folders/1WL6aoW7ZacY5_hQ2bRr1XttLr7Ku6FD7?usp=drive_link

Please upload the data files to the files in google colab before executing code
"""

# Commented out IPython magic to ensure Python compatibility.
!unzip /content/Negative_Images.zip
# %ls

# Commented out IPython magic to ensure Python compatibility.
!unzip /content/Small_Positive_Images.zip
# %ls

"""#CNN"""

from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential

# Set the paths to the vehicle and non-vehicle image folders
vehicle_folder = "/content/Small_Positive_Images"
non_vehicle_folder = "/content/Negative_Images"

# Load the images and labels
vehicle_images = []
non_vehicle_images = []

for filename in os.listdir(vehicle_folder):
    img = cv2.imread(os.path.join(vehicle_folder, filename))
    img = cv2.resize(img, (64, 64))  # Resize the image to a suitable size
    vehicle_images.append(img)

for filename in os.listdir(non_vehicle_folder):
    img = cv2.imread(os.path.join(non_vehicle_folder, filename))
    img = cv2.resize(img, (64, 64))  # Resize the image to a suitable size
    non_vehicle_images.append(img)

# Create labels for the images
vehicle_labels = np.ones(len(vehicle_images))
non_vehicle_labels = np.zeros(len(non_vehicle_images))

# Combine the vehicle and non-vehicle data
images = np.concatenate([vehicle_images, non_vehicle_images])
labels = np.concatenate([vehicle_labels, non_vehicle_labels])

# Split the data into training and testing sets
train_images, test_images, train_labels, test_labels = train_test_split(
    images, labels, test_size=0.2, random_state=42)

# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,  # Randomly rotate the images
    width_shift_range=0.1,  # Randomly shift the images horizontally
    height_shift_range=0.1,  # Randomly shift the images vertically
    horizontal_flip=True)  # Randomly flip the images horizontally

# Train the model
model.fit(datagen.flow(train_images, train_labels, batch_size=32),
          steps_per_epoch=len(train_images) // 32, epochs=15)

# Evaluate the model
loss, accuracy = model.evaluate(test_images, test_labels)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

# Save the model
model.save('vehicle_detection_model.h5')

# Make predictions
#new_images = [...]  # Load or capture new images
#new_images = np.array(new_images)
#new_images = np.resize(new_images, (len(new_images), 64, 64, 3))
#predictions = model.predict(new_images)

# Convert predictions to class labels
#class_labels = ['Non-vehicle', 'Vehicle']
#predicted_labels = [class_labels[int(prediction)] for prediction in predictions]

#print('Predictions:', predicted_labels)

"""#DNN"""

from google.colab import drive
drive.mount('/content/drive')

import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential

# Set the paths to the vehicle and non-vehicle image folders
vehicle_folder = '/content/Small_Positive_Images'
non_vehicle_folder = '/content/Negative_Images'

# Load the images and labels
vehicle_images = []
non_vehicle_images = []

for filename in os.listdir(vehicle_folder):
    img = cv2.imread(os.path.join(vehicle_folder, filename))
    img = cv2.resize(img, (64, 64))  # Resize the image to a suitable size
    vehicle_images.append(img)

for filename in os.listdir(non_vehicle_folder):
    img = cv2.imread(os.path.join(non_vehicle_folder, filename))
    img = cv2.resize(img, (64, 64))  # Resize the image to a suitable size
    non_vehicle_images.append(img)

# Create labels for the images
vehicle_labels = np.ones(len(vehicle_images))
non_vehicle_labels = np.zeros(len(non_vehicle_images))

# Combine the vehicle and non-vehicle data
images = np.concatenate([vehicle_images, non_vehicle_images])
labels = np.concatenate([vehicle_labels, non_vehicle_labels])

# Split the data into training and testing sets
train_images, test_images, train_labels, test_labels = train_test_split(
    images, labels, test_size=0.2, random_state=42)

train_images.shape

blob = cv2.dnn.blobFromImages(test_images, 1.0/127.5, (64, 64), [127.5, 127.5, 127.5])

# path to the weights and model files.   (LOAD FILES FROM DESKTOP FOLDER)
weights = "frozen_inference_graph.pb"
model = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
# load the MobileNet SSD model trained  on the COCO dataset
net = cv2.dnn.readNetFromTensorflow(weights, model)

# load the class labels the model was trained on
class_names = []
with open("coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

# pass the blog through our network and get the output predictions
net.setInput(blob)
output = net.forward()  # shape: (1, 1, 100, 7)

"""# The model might take couple hrs to run with some issues, you may skip the next code."""

# path to the weights and model files.   (LOAD FILES FROM DESKTOP FOLDER)
weights = "frozen_inference_graph.pb"
model = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
# load the MobileNet SSD model trained  on the COCO dataset
net = cv2.dnn.readNetFromTensorflow(weights, model)

# load the class labels the model was trained on
class_names = []
with open("coco_names.txt", "r") as f:
    class_names = f.read().strip().split("\n")

# pass the blog through our network and get the output predictions
net.setInput(blob)
output = net.forward()  # shape: (1, 1, 100, 7)

correct = 0
wrong = 0
for i in range(len(test_images)):
    img = test_images[i]
    label = test_labels[i]

    blob = cv2.dnn.blobFromImages(test_images, 1.0/127.5, (64, 64), [127.5, 127.5, 127.5])

    # Run inference
    net.setInput(blob)
    output = net.forward()
    prediction = np.argmax(output)
    if prediction == label:
        correct += 1
    else:
        wrong += 1

print("count of test samples:", len(test_images))
print("accuracy:", (correct/(correct+wrong)))

"""#SVM"""

!pip install Cython
!pip install scikit-learn
!pip install sklearn
import numpy as np
import sklearn.model_selection
import sklearn.externals
import joblib

from skimage.feature import hog
from skimage.transform import pyramid_gaussian
from skimage.io import imread
#from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from skimage import color
from imutils.object_detection import non_max_suppression
import imutils
import numpy as np
import argparse
import cv2
import os
import glob
from PIL import Image # This will be used to read/modify images (can be done via OpenCV too)
from numpy import *

# define parameters of HOG feature extraction
orientations = 9
pixels_per_cell = (8, 8)
cells_per_block = (2, 2)
threshold = .3

Positive_File = r"/content/Small_Positive_Images"
Negative_File = r"/content/Negative_Images"

pos_im_listing = os.listdir(Positive_File) # it will read all the files in the positive image path (so all the required images)
neg_im_listing = os.listdir(Negative_File)
num_pos_samples = size(pos_im_listing) # simply states the total no. of images
num_neg_samples = size(neg_im_listing)
print(num_pos_samples) # prints the number value of the no.of samples in positive dataset
print(num_neg_samples)

from sklearn.model_selection import train_test_split

train_positive, test_positive = train_test_split(
    pos_im_listing, test_size=0.2, random_state=42)

train_negative, test_negative = train_test_split(
    neg_im_listing, test_size=0.2, random_state=42)

data_train= []
data_test= []
labels_train = []
labels_test = []
# compute HOG features and label them:

for file in train_positive: #this loop enables reading the files in the pos_im_listing variable one by one
    img = Image.open(Positive_File + '/' + file) # open the file
    #img = img.resize((64,128))
    gray = img.convert('L') # convert the image into single channel i.e. RGB to grayscale
    # calculate HOG for positive features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True)# fd= feature descriptor
    data_train.append(fd)
    labels_train.append(1)

for file in test_positive: #this loop enables reading the files in the pos_im_listing variable one by one
    img = Image.open(Positive_File + '/' + file) # open the file
    #img = img.resize((64,128))
    gray = img.convert('L') # convert the image into single channel i.e. RGB to grayscale
    # calculate HOG for positive features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True)# fd= feature descriptor
    data_test.append(fd)
    labels_test.append(1)

# Same for the negative images
for file in train_negative:
    img= Image.open(Negative_File + '/' + file)
    #img = img.resize((64,128))
    gray= img.convert('L')
    # Now we calculate the HOG for negative features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True)
    data_train.append(fd)
    labels_train.append(0)

# Same for the negative images
for file in test_negative:
    img= Image.open(Negative_File + '/' + file)
    #img = img.resize((64,128))
    gray= img.convert('L')
    # Now we calculate the HOG for negative features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True)
    data_test.append(fd)
    labels_test.append(0)


# encode the labels, converting them from strings to integers
le = LabelEncoder()
labels_train = le.fit_transform(labels_train)
labels_test = le.fit_transform(labels_test)

labels_test

trainData = data_train
trainLabels = labels_train
testData = data_test
testLabels = labels_test

trainData

#%%
# Partitioning the data into training and testing splits, using 80%
# of the data for training and the remaining 20% for testing
#print(" Constructing training/testing split...")
#(trainData, testData, trainLabels, testLabels) = train_test_split(
	#np.array(data), labels, test_size=0.20, random_state=42)
#%% Train the linear SVM
#print(" Training Linear SVM classifier...")
model = LinearSVC()
model.fit(trainData, trainLabels)
#%% Evaluate the classifier
print(" Evaluating classifier on test data ...")
predictions = model.predict(testData)
print(classification_report(testLabels, predictions))


# Save the model:
#%% Save the Model
joblib.dump(model, 'hog_svm.npy')

"""Visualization of Histogram of oriented gradients"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:53:18 2017

@author: Samyakh Tukra
"""
#%%
import matplotlib.pyplot as plt
from skimage import io
from skimage.feature import hog
from skimage import data, color, exposure
from PIL import Image
#%%
img = io.imread(r"/content/drive/MyDrive/ECE 579 Intelligent Systems/Project/Sample_Pos/host-a010_cam0_1232314667250886006.jpeg")
#im= Image.open(r"Insert\Image\Path\Here.jpg")
image = color.rgb2gray(img)

fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualize=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

ax1.axis('off')
ax1.imshow(image, cmap=plt.cm.gray)
ax1.set_title('Input image')
ax1.set_adjustable('box')

# Rescale histogram for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

ax2.axis('off')
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title('Histogram of Oriented Gradients')
ax1.set_adjustable('box')
plt.show()