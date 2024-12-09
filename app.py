import streamlit as st
from train_model import train_model, evaluate_model
from hyperparameters_db import save_hyperparameters
from cloud_storage import upload_to_gcs
import pickle
import os

st.title("MobileNet Model Training")

# Model Selection
model_version = st.selectbox("Select MobileNet Version", ["MobileNet", "MobileNetV2"])
learning_rate = st.slider("Learning Rate", 0.0001, 0.1, 0.001)
batch_size = st.slider("Batch Size", 8, 64, 32)
epochs = st.slider("Epochs", 1, 50, 10)

if st.button("Train Model"):
    # Load your dataset here
    train_data = ...  # Replace with actual data loading code
    test_data = ...

    # Train model
    model = train_model(model_version, learning_rate, batch_size, epochs, train_data)

    # Evaluate model
    accuracy, cm = evaluate_model(model, test_data)
    st.write(f"Accuracy: {accuracy:.2f}")
    st.write(f"Confusion Matrix: {cm}")

    # Save hyperparameters
    save_hyperparameters(model_version, learning_rate, batch_size, epochs)

    # Save model locally
    model_path = f"{model_version}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    st.download_button("Download Model", model_path)

    # Upload predictions to Cloud Storage
    upload_to_gcs(model_path, model_path)
    st.success("Model and predictions uploaded successfully.")
