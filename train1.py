import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# Set image dimensions
IMG_SIZE = 48
BATCH_SIZE = 16
EPOCHS = 40

# Data generator for grayscale images
datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixels to [0, 1]
    validation_split=0.2  # Use 20% of data for validation
)

# Load training and validation data from directories
train_data = datagen.flow_from_directory(
    r'C:\Users\vaibh\Desktop\Work\stress\Train\Harsh&Aditya',
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='grayscale',  # Force grayscale mode
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    r'C:\Users\vaibh\Desktop\Work\stress\Train\Harsh&Aditya',
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='grayscale',  # Force grayscale mode
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Build the model (CNN)
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')  # 10 emotions
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_data, validation_data=val_data, epochs=EPOCHS)

# Save the model to file
model.save('emotion_model2.h5')
