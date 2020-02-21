from __future__ import absolute_import, division, print_function, unicode_literals

# # TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
tf.get_logger().setLevel('INFO')

# Helper libraries
import os
import cv2
import shutil  
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import image

# CONSTANTS
PATH = os.getcwd()
DATASET = os.path.join(PATH, "dataset")
CATEGORIES = [folder for folder in os.listdir(DATASET)]
INDEX_VALUES = [i for i in range(30)]

# Creates a folder for each individual's pictures
def normalize_dataset():
    for file in os.listdir("dataset"):
        try:
            os.mkdir(f"dataset/{file[5:7]}")
            
        except FileExistsError:
            print("Directory ", file[5:7], " already exists")

        shutil.move(os.getcwd() + f"/dataset/{file}", os.getcwd() + f"/dataset/{file[5:7]}/{file}")

# Generate the trainig data (image, label)
def create_training_data():
    _images = []
    _labels = []
    for category in CATEGORIES:
        class_num = CATEGORIES.index(category)
        new_path = os.path.join(DATASET, category)
        for img in os.listdir(new_path):
            img_array = cv2.imread(os.path.join(new_path, img), cv2.IMREAD_GRAYSCALE)
            _images.append(img_array)
            _labels.append(class_num)
    return (_images, _labels)


def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(77, 68)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(30)
    ])

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    return model

# Create a callback that saves the model's weights
def train_model(model):
    checkpoint_path = "model/model.ckpt"
    
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                    save_weights_only=True,
                                                    verbose=1)

    # Train the model with the new callback
    model.fit(x=np.array(training_images), 
            y=np.array(training_labels),  
            epochs=10,
            validation_data=(np.array(training_images),np.array(training_labels)),
            callbacks=[cp_callback])  # Pass callback to training

    return model

# Display the model's architecture
def model_architecture():
    model = train_model(create_model())
    model.summary()

# Visualize the data
def visualize_individual_picture():
    plt.figure()
    plt.imshow(training_images[0])
    plt.colorbar()
    plt.grid(False)
    plt.show()

def reevaluate_model():
    checkpoint_path = "model/model.ckpt"
    # Create a basic model instance
    model = create_model()

    # Evaluate the model
    loss, acc = model.evaluate(x=np.array(training_images),  y=np.array(training_labels), verbose=2)
    print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

    # Loads the weights
    model.load_weights(checkpoint_path)

    # Re-evaluate the model
    loss,acc = model.evaluate(x=np.array(training_images),  y=np.array(training_labels), verbose=2)
    print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
    

if __name__ == "__main__":
    (training_images, training_labels) = create_training_data()
    training_images = np.array(training_images)
    training_images = training_images / 255.0

    # visualize_random_pictures()

    print("create and train the model \n")
    train_model(create_model())

    # print("model architecture \n")
    # model_architecture()

    # print("reevaluation of the saved model \n")
    # reevaluate_model()