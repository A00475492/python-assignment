import os
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import streamlit as st


st.set_option('deprecation.showfileUploaderEncoding', False)
model = tf.keras.models.load_model("digit_classifier_model.h5")



def resize_image(image, size):
    return ImageOps.fit(image, size)


def classify_digit(image):
    image = image.convert('L')  # Convert to grayscale
    image = resize_image(image, (28, 28))
    image = np.array(image, dtype=np.float32)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    prediction = model.predict(image)
    digit = np.argmax(prediction)

    return digit


st.title("Image Classifier")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    digit = classify_digit(image)
    st.write(f"The digit in the image is: {digit}")