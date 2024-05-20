import pandas as pd
import numpy as np
import librosa
import tensorflow as tf
import matplotlib.pyplot as plt
import librosa.display
from sklearn.model_selection import train_test_split
import keras
from keras import Model, Input
from tensorflow.python.keras.layers import Conv1D, Flatten, Dense, Dropout, SpatialDropout1D, GlobalAveragePooling1D
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.optimizers import ExponentialDecay
from tensorflow.python.keras.losses import SparseCategoricalCrossentropy
from tensorflow.python.keras.metrics import SparseCategoricalAccuracy
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from tensorflow.python.keras.callbacks import TensorBoard, ModelCheckpoint
import seaborn as sns

bird_labels = pd.read_csv("Bird Song Dataset/bird_songs_metadata.csv", usecols=['species'])
bird_labels = bird_labels.values
bird_labels[bird_labels == ['bewickii']] = 0
bird_labels[bird_labels == ['polyglottos']] = 1
bird_labels[bird_labels == ['migratorius']] = 2
bird_labels[bird_labels == ['melodia']] = 3
bird_labels[bird_labels == ['cardinalis']] = 4
bird_labels = np.squeeze(bird_labels)

# Creating list of file paths
file_names = pd.read_csv("Bird Song Dataset/bird_songs_metadata.csv", usecols=['filename'])
file_names = np.squeeze(file_names.values)
bird_filepaths = np.array([])
for file in file_names:
    bird_filepaths = np.append(bird_filepaths, 'Bird Song Dataset/wavfiles/'+file)

# Splitting data into training and validation set
bird_filepaths_train, bird_filepaths_val, bird_labels_train, bird_labels_val = train_test_split(
    bird_filepaths, bird_labels, test_size=0.10, random_state=2419)

# Function that reads filepaths
def read_file(path):
    y,_ = librosa.load(path)
    return y

# Converting to db scale
def spec_to_db(y):
    y_db = librosa.amplitude_to_db(y, ref=100)
    return y_db

# Map function that returns spectrograms
def map_function(path_tensor, label):
    y=tf.numpy_function(read_file, inp= [path_tensor], Tout = tf.float32)
    spectrogram = tf.abs(tf.signal.stft(y, frame_length=512, frame_step=64))
    spectrogram_db = tf.numpy_function(spec_to_db, inp = [spectrogram], Tout = tf.float32)
    spectrogram_db = spectrogram_db/80+1
    return spectrogram_db, label

# Function that creates tf.data.Dataset with shuffle, repeat, map and batch
def make_dataset(bird_labels, bird_filepaths, shuffle):
    bird_labels = tf.convert_to_tensor(bird_labels, dtype = tf.int32)
    bird_filepaths = tf.convert_to_tensor(bird_filepaths, dtype = tf.string)

    bird_labels = tf.data.Dataset.from_tensor_slices(bird_labels)
    bird_filepaths = tf.data.Dataset.from_tensor_slices(bird_filepaths)
    dataset = tf.data.Dataset.zip( bird_filepaths, bird_labels)

    if shuffle:
        dataset = dataset.shuffle(buffer_size = dataset.cardinality(), reshuffle_each_iteration=True)
    dataset = dataset.map(map_function, num_parallel_calls = tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size = 32, num_parallel_calls = tf.data.AUTOTUNE, drop_remainder = True)

    return dataset

