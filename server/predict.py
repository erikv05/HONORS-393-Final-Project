import tensorflow as tf
import librosa
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from convert_to_wav import convert_to_wav
import re

# Function to read a wavefile and convert it to a normalized spectrogram
def preprocess_wavefile(filepath: str, start: float):
    pattern = r'[^\/]+(?=\.)'
    filename = re.findall(pattern, filepath)[0]
    if (filepath[-4:] != ".wav"):
        convert_to_wav(filepath)
        filepath = "converted_wavfiles/" + filename + ".wav"
    output_image_path = f"spect/{filename}.png"
    y, _ = librosa.load(filepath, offset=start, duration=3)
    spectrogram = tf.abs(tf.signal.stft(y, frame_length=512, frame_step=64))
    spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=100)
    spectrogram_db = spectrogram_db / 80 + 1

    # Plot the spectrogram and save it as an image
    matplotlib.use("Agg")
    plt.figure(figsize=(10, 4))
    plt.imshow(spectrogram, aspect='auto', origin='lower')
    plt.axis('off')  # No axes for the image

    # Save the spectrogram image
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return spectrogram_db, output_image_path

def predict(filepath, start: float):
    # Load the saved model
    loaded_model = tf.saved_model.load('topmodel')

    # Get the concrete function from the model
    infer = loaded_model.signatures['serving_default']

    # Preprocess the wavefile
    spectrogram_db, out_path = preprocess_wavefile(filepath, start)

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

    return predicted_species, out_path