import tensorflow as tf
from tensorflow.keras.applications import MobileNet, MobileNetV2
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

def train_model(model_version, learning_rate, batch_size, epochs, train_data):
    base_model = (
        MobileNet(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
        if model_version == "MobileNet"
        else MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    )
    base_model.trainable = False
    model = tf.keras.Sequential(
        [
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1024, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(train_data, epochs=epochs, batch_size=batch_size)
    return model

def evaluate_model(model, test_data):
    predictions = model.predict(test_data)
    y_true = np.concatenate([y for x, y in test_data])
    y_pred = np.argmax(predictions, axis=1)
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    return accuracy, cm
