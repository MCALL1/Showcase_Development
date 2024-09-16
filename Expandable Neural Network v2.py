# -*- coding: utf-8 -*-
"""
Michael Call 
Created on Sat Aug 12 14:47:02 2023



from keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.models import Sequential

class ExpandableNN:
    def __init__(self, input_shape, output_shape):
        self.model = Sequential()
        self.input_shape = input_shape
        self.output_shape = output_shape

    def add_dense_layer(self, units, activation='relu'):
        """Add a fully connected dense layer."""
        self.model.add(Dense(units, activation=activation))

    def add_convolutional_layer(self, filters, kernel_size, activation='relu'):
        """Add a convolutional layer (for image data)."""
        self.model.add(Conv2D(filters, kernel_size, activation=activation))

    def add_maxpooling_layer(self, pool_size):
        """Add a max pooling layer (for image data)."""
        self.model.add(MaxPooling2D(pool_size=pool_size))

    def add_flatten_layer(self):
        """Add a flatten layer to connect convolutional layers to dense layers."""
        self.model.add(Flatten())

    def add_dropout_layer(self, rate):
        """Add a dropout layer for regularization."""
        self.model.add(Dropout(rate))

    def compile_model(self, optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']):
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    def fit(self, x_train, y_train, validation_data, epochs=10, batch_size=32):
        self.model.fit(x_train, y_train, validation_data=validation_data, epochs=epochs, batch_size=batch_size)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

    def load_data(self, path):
        """Load data from a specified path or create logic to generate data."""
        # Implement the logic to load or create the data based on your specific needs
        # e.g., loading from CSV files, images, etc.
        x_train, y_train, x_val, y_val, x_test, y_test = ...
        return x_train, y_train, x_val, y_val, x_test, y_test
