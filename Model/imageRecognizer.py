import numpy as np
import tensorflow as tf
import os
import cv2 as cv

#Declaring variables
IMG_Size = (30, 30)
char_path = 'numbers'

characters = []
IMG = []
VAL = []
for char in os.listdir(char_path):
    characters.append(char)
    path = os.path.join(char_path, char)
    for img in os.listdir(path):
        img_path = os.path.join(path, img)

        img_array = cv.imread(img_path)
        resized = cv.resize(img_array, IMG_Size, interpolation=cv.INTER_AREA)
        img_ = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)

        img_ = np.array(img_)
        img_ = np.reshape(img_, (30,30,1))

        IMG.append(img_)
        VAL.append(characters.index(char))

IMG = np.array(IMG)
IMG = IMG/255.0

print(IMG[0])
print(IMG.shape)

VAL = tf.keras.utils.to_categorical(VAL, len(characters))

from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(
    IMG, VAL, test_size=0.2, random_state=42, shuffle=True
)

#defining model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(30,30,1)),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(characters), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#training the model
history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    batch_size=32,
    epochs=100
)

#saving the model for future use
model.save("recognizer.h5")