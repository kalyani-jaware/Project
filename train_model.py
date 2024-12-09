import tensorflow as tf
from tensorflow.keras.applications import MobileNet, MobileNetV2
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


def train_model(model_version, learning_rate, batch_size, epochs, data):
    X_train, y_train = data

    # Load the model based on the selected version
    base_model = (
        MobileNet(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        if model_version == "MobileNet"
        else MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    )
    base_model.trainable = False
    
    # Define the model architecture
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),  # Adjust number of classes as needed
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    
    # Train the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    
    return model


def evaluate_model(model, data):
    X_test, y_test = data

    predictions = model.predict(X_test)
    y_pred = np.argmax(predictions, axis=1)
    
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    return accuracy, cm
