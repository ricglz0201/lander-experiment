"""Module containing supervised predictor"""
from numpy import array

import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.models import Sequential, load_model

def build_model():
    """Builds tensorflow model"""
    model = Sequential([
        Dense(10, activation='sigmoid', input_shape=(7,)),
        Dense(5, activation='sigmoid'),
        Dense(10, activation='sigmoid'),
        Dense(5, activation='sigmoid'),
        Dense(6, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss=SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    return model

class SupervisedPredictor():
    def __init__(self, filepath=None, scaler=None):
        error_msg = 'Both filepath and scaler must be either None or not None'
        assert not bool(filepath) ^ bool(scaler), error_msg
        self.is_trained = filepath is not None
        self.model = build_model() if filepath is None else load_model(filepath)
        self.scaler = scaler

    def set_scaler(self, scaler):
        """Sets the scaler"""
        self.scaler = scaler

    def fit(self, training_set, validation_data):
        """
        @type training_set: (ndarray, ndarray)
        """
        callback = EarlyStopping()
        self.model.fit(
            training_set[0], training_set[1], batch_size=10,
            epochs=100, validation_data=validation_data, callbacks=[callback]
        )
        self.is_trained = True

    def predict(self, inputs):
        """Makes a prediction using the model based on the inputs"""
        scaled_inputs = self.scaler.transform(array(inputs).reshape(1, -1))
        prediction = self.model.predict(scaled_inputs)[0]
        return tf.math.argmax(prediction)
