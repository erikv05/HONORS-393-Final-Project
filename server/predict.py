import tensorflow as tf
import librosa
import numpy as np
from convert_to_wav import convert_to_wav
import re

# Function to read a wavefile and convert it to a normalized spectrogram
def preprocess_wavefile(filepath: str, start: float):
    if (filepath[-4:] != ".wav"):
        pattern = r'[^\/]+(?=\.)'
        convert_to_wav(filepath)
        filename = re.findall(pattern, filepath)[0]
        filepath = "converted_wavfiles/" + filename + ".wav"
    y, _ = librosa.load(filepath, offset=start, duration=3)
    spectrogram = tf.abs(tf.signal.stft(y, frame_length=512, frame_step=64))
    spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=100)
    spectrogram_db = spectrogram_db / 80 + 1
    return spectrogram_db

def predict(filepath, start: float):
    # Load the saved model
    loaded_model = tf.saved_model.load('topmodel')

    # Get the concrete function from the model
    infer = loaded_model.signatures['serving_default']

    # Preprocess the wavefile
    spectrogram_db = preprocess_wavefile(filepath, start)

    # Ensure the input shape matches the model's input shape
    # The model expects a batch of inputs, so we need to expand the dimensions
    input_data = tf.expand_dims(spectrogram_db, axis=0)

    # Pad or trim the input data to match the model's expected input shape if necessary
    expected_shape = (1026, 257)
    input_data = tf.image.resize(input_data, expected_shape)

    # Make a prediction
    predictions = infer(input_data)

    # Get the predicted class
    predicted_class = np.argmax(predictions['12_Dense'], axis=-1)

    # Map the predicted class to the bird species
    species_mapping = {0: 'bewickii', 1: 'polyglottos', 2: 'migratorius', 3: 'melodia', 4: 'cardinalis'}
    predicted_species = species_mapping[predicted_class[0]]

    return predicted_species