import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Suppress OneDNN warnings

import shutil
import os
import math
import glob
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define root path for the dataset
Root = "E:/chrome extention/Brain-Tumer-Detection/dataset"
no_of_img = {}

# Count the number of images in each class
for i in os.listdir(Root):
    no_of_img[i] = len(os.listdir(os.path.join(Root, i)))

# Function to split the dataset
def calculate_for_other(name, split):
    if not os.path.exists('./' + name):
        os.mkdir('./' + name)
        for i in os.listdir(Root):
            os.mkdir(os.path.join('.', name, i))
            for j in np.random.choice(a=os.listdir(Root + "/" + i), size=math.floor((split) * no_of_img[i]) - 5, replace=False):
                O = os.path.join(Root, i, j)
                D = os.path.join('./', name, i)
                shutil.copy(O, D)
    else:
        print("The folder already exists")

# Create train, validation, and test datasets
calculate_for_other('train', 0.7)
calculate_for_other('valid', 0.15)
calculate_for_other('test', 0.15)

# Build CNN model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=(3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(Conv2D(filters=36, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(rate=0.25))
model.add(Dense(units=1, activation='sigmoid'))

model.summary()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Image preprocessing functions
def preprocessingImages1(path):
    image_data = ImageDataGenerator(zoom_range=0.2, shear_range=0.2, rescale=1/255, horizontal_flip=True)
    image = image_data.flow_from_directory(directory=path, target_size=(224, 224), batch_size=32, class_mode='binary')
    return image

path1 = './train'
train_data = preprocessingImages1(path1)

def preprocessingImages2(path):
    image_data = ImageDataGenerator(rescale=1/255)
    image = image_data.flow_from_directory(directory=path, target_size=(224, 224), batch_size=32, class_mode='binary')
    return image

path2 = './test'
test_data = preprocessingImages2(path2)
path3 = './valid'
valid_data = preprocessingImages2(path3)

# Early stopping and model checkpointing
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

es = EarlyStopping(monitor='val_accuracy', min_delta=0.01, patience=5, verbose=1, mode='auto')
mc = ModelCheckpoint(monitor='val_accuracy', filepath='./bestmodel.keras', verbose=1, save_best_only=True, mode='auto')

# Fit model
hs = model.fit(generator=train_data,
               steps_per_epoch=20,
               epochs=30,
               verbose=1,
               validation_data=valid_data,
               validation_steps=10,
               callbacks=[es, mc])

# Plotting
h = hs.history
plt.plot(h['accuracy'], c='red', label='Train Accuracy')
plt.plot(h['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy vs Validation Accuracy')
plt.legend()
plt.show()

plt.plot(h['loss'], c='red', label='Train Loss')
plt.plot(h['val_loss'], label='Validation Loss')
plt.title('Loss vs Validation Loss')
plt.legend()
plt.show()

# Model Evaluation
model = load_model("./bestmodel.keras")
acc = model.evaluate(test_data)[1]
print(f"Our model accuracy is {acc * 100} %")

# Making predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

path = 'c0472761-800px-wm.jpg'
img = load_img(path, target_size=(224, 224))
input_arr = img_to_array(img) / 255
input_arr = np.expand_dims(input_arr, axis=0)

def get_treatment_info():
    return (
        "Treatment for brain tumors may include:\n"
        "- Surgery to remove the tumor\n"
        "- Radiation therapy\n"
        "- Chemotherapy\n"
        "- Targeted therapy\n"
        "- Clinical trials for new therapies\n"
        "Consult a healthcare professional for the best course of action."
    )

pred = model.predict(input_arr)[0][0]
if pred > 0.5:
    print("The MRI image has a tumor")
else:
    print("The MRI image is a healthy image")