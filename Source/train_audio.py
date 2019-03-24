import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from keras import models
from keras import layers
from keras import callbacks
from keras import losses

MODEL_FILE_PATH = '../Output/audio_emotion.h5'


def create_model():
    model = models.Sequential()
    model.add(layers.BatchNormalization(input_shape=(26,), axis=1))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.BatchNormalization(axis=1))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.BatchNormalization(axis=1))
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.BatchNormalization(axis=1))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.BatchNormalization(axis=1))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.5))

    model.add(layers.BatchNormalization(axis=1))
    model.add(layers.Dense(8, activation='softmax'))
    return model


def train():
    model = create_model()
    model.compile(optimizer='adam',
                  loss=losses.sparse_categorical_crossentropy,
                  metrics=['accuracy'])
    checkpointer = callbacks.ModelCheckpoint(filepath="../Output/checkpoint.hdf5", verbose=1, save_best_only=True)
    x_train, x_test, y_train, y_test = load_audio_data()
    model.fit(x_train,
              y_train,
              epochs=1000,
              batch_size=1024,
              validation_split=0.2,
              callbacks=[checkpointer])
    results = model.evaluate(x_test, y_test)
    print('test_results: ', results)

    model.save(MODEL_FILE_PATH)


def load_trained_model():
    model = models.load_model(MODEL_FILE_PATH)
    return model


def predict(x):
    model = load_trained_model()
    # scaler = StandardScaler()
    x = x.reshape(1, -1)
    # x = scaler.fit_transform(x)
    return model.predict(x)


def load_audio_data():
    data = pd.read_csv('../Output/data.csv')
    data = data.drop(['filename'], axis=1)

    emotion_list = data.iloc[:, -1]
    encoder = LabelEncoder()
    y = encoder.fit_transform(emotion_list)
    x = np.array(data.iloc[:, :-1], dtype=float)
    # scaler = StandardScaler().fit(x)
    # x = scaler.transform()

    return train_test_split(x, y, test_size=0.2)


if __name__ == '__main__':
    train()
