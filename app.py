import streamlit as st
import numpy as np
import tensorflow as tf
import librosa
import matplotlib.pyplot as plt
import librosa.display

# Function to read audio file
def read_file(path):
    y, _ = librosa.load(path)
    return y

# Function to convert to dB scale
def spec_to_db(y):
    y_db = librosa.amplitude_to_db(y, ref=100)
    return y_db

# Function to preprocess audio file
def preprocess_audio(audio_path):
    # Read audio file
    y = read_file(audio_path)
    
    # Compute spectrogram
    spectrogram = tf.abs(tf.signal.stft(y, frame_length=512, frame_step=64))
    
    # Convert to dB scale
    spectrogram_db = spec_to_db(spectrogram)
    spectrogram_db = spectrogram_db / 80 + 1
    
    # Expand dimensions to match model input shape
    spectrogram_db = np.expand_dims(spectrogram_db, axis=0)
    
    return spectrogram_db

# Load the trained model
model = tf.keras.models.load_model("model.h5")

# Dictionary to map predicted class indices to bird species names
class_names = {
    0: "Bewick's Wren",
    1: "Northern Mockingbird",
    2: "American Robin",
    3: "Song Sparrow",
    4: "Northern Cardinal"
}

# Streamlit app
st.title("Bird Species Classification from Audio")

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

predict_button = st.button("Predict")

# Perform inference when file is uploaded
if uploaded_file is not None and predict_button:
    # Preprocess the uploaded audio file
    audio_data = preprocess_audio(uploaded_file)
    
    # Display audio player
    st.audio(uploaded_file, format='audio/wav', start_time=0)
    
    # Display spectrogram
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.specshow(audio_data[0], sr=22050, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    st.pyplot(fig)
    
    # Perform inference using the model
    prediction = model.predict(audio_data)
    
    # Get the predicted class index
    predicted_class_index = np.argmax(prediction)
    
    # Get the predicted bird species name
    predicted_species = class_names[predicted_class_index]
    
    # Display the predicted bird species
    st.write(f"Predicted Bird Species: {predicted_species}")
