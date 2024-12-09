import os
import zipfile
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image

def preprocess_data(df):
    # Assuming 'df' contains columns 'image_path' and 'label'
    image_paths = df['image_path'].values
    labels = df['label'].values

    images = [load_and_preprocess_image(image_path) for image_path in image_paths]
    images = np.array(images)
    labels = np.array(labels)

    # Split dataset into train and test (80-20 split)
    split_idx = int(0.8 * len(images))
    train_images, test_images = images[:split_idx], images[split_idx:]
    train_labels, test_labels = labels[:split_idx], labels[split_idx:]

    return (train_images, train_labels), (test_images, test_labels)

def preprocess_images(img):
    # Process individual images if uploaded (Resize and normalize)
    img = img.resize((224, 224))  # Resize to (224, 224)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Normalize the image
    return img_array, None  # No labels for a single image

def load_and_preprocess_image(img_path):
    # Load and preprocess a single image from disk
    img = Image.open(img_path)
    img = img.resize((224, 224))  # Resize to (224, 224)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Normalize the image
    return img_array
