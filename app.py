import streamlit as st
import tensorflow as tf
from train_model import train_model, evaluate_model
from hyperparameters_db import save_hyperparameters
from cloud_storage import upload_to_gcs
import pickle
import os
from PIL import Image
import zipfile
import numpy as np
from sklearn.model_selection import train_test_split

st.title("MobileNet Model Training")

# Model Selection
model_version = st.selectbox("Select MobileNet Version", ["MobileNet", "MobileNetV2"])
learning_rate = st.slider("Learning Rate", 0.0001, 0.1, 0.001)
batch_size = st.slider("Batch Size", 8, 64, 32)
epochs = st.slider("Epochs", 1, 50, 10)

# Dataset Upload
uploaded_file = st.file_uploader("Upload a zip of images", type=["zip"])
train_data = None
test_data = None

if uploaded_file is not None:
    # Extract images from the zip file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("/tmp/images")  # Extract images to a temporary directory
        image_files = zip_ref.namelist()  # List of image files in the zip
        st.write(f"Extracted {len(image_files)} images.")
    
    # Process the images (resize and normalize)
    image_data = []
    labels = []  # If you have labels, make sure to add them (e.g., from filenames or another file)
    
    for image_file in image_files:
        try:
            img = Image.open(os.path.join("/tmp/images", image_file))
            img = img.resize((224, 224))  # Resize image to match MobileNet input size
            img = np.array(img)  # Convert to numpy array
            img = img / 255.0  # Normalize to [0, 1]
            image_data.append(img)
            
            # Add labels (this assumes you have labels available)
            # For example, using the file name to determine the label
            label = 0  # Replace with actual label logic based on your dataset
            labels.append(label)
        except Exception as e:
            st.write(f"Error processing image {image_file}: {e}")
    
    # Convert to numpy arrays
    image_data = np.array(image_data)
    labels = np.array(labels)

    # Split the data into training and testing sets (80% training, 20% testing)
    train_data, test_data = train_test_split(list(zip(image_data, labels)), test_size=0.2)
    st.write(f"Training data: {len(train_data)} images, Testing data: {len(test_data)} images")

# Start training when the button is clicked
if st.button("Train Model"):
    if uploaded_file is not None and train_data is not None and test_data is not None:
        # Separate the images and labels
        X_train, y_train = zip(*train_data)
        X_test, y_test = zip(*test_data)

        # Convert to numpy arrays
        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        # Train model
        model = train_model(model_version, learning_rate, batch_size, epochs, (X_train, y_train))

        # Evaluate model
        accuracy, cm = evaluate_model(model, (X_test, y_test))
        st.write(f"Accuracy: {accuracy:.2f}")
        st.write(f"Confusion Matrix: {cm}")

        # Save hyperparameters to the database
        save_hyperparameters(model_version, learning_rate, batch_size, epochs)

        # Save model locally as a .pkl file
        model_path = f"{model_version}_model.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        st.download_button("Download Model", model_path)

        # Upload model and predictions to Google Cloud Storage
        upload_to_gcs(model_path, model_path)  # Make sure your cloud_storage.py implements this function
        st.success("Model and predictions uploaded successfully.")
    else:
        st.error("Please upload a zip file with images first.")
