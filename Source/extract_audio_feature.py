import librosa
import numpy as np
import os
import csv


def extract_audio_feature(path):
    y, sr = librosa.load(path, mono=True, sr=None)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    features = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
    for e in mfcc:
        features += f' {np.mean(e)}'
    return features


def preprocess_ravdess():
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()

    file = open('../Output/data.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    emotions = 'neutral calm happy sad angry fearful disgust surprised'.split()
    channels = 'Song Speech'.split()
    for channel in channels:
        for actor in os.listdir(f'../AudioData/Audio_{channel}_Actors_01-24'):
            for file in os.listdir(f'../AudioData/Audio_{channel}_Actors_01-24/{actor}'):
                audio_path = f'../AudioData/Audio_{channel}_Actors_01-24/{actor}/{file}'
                to_append = f'{file}'
                features = extract_audio_feature(audio_path)
                to_append += f' {features}'
                emotion = emotions[int(file.split('-')[2]) - 1]
                to_append += f' {emotion}'
                file = open('../Output/data.csv', 'a', newline='')
                with file:
                    writer = csv.writer(file)
                    writer.writerow(to_append.split())


if __name__ == '__main__':
    preprocess_ravdess()
