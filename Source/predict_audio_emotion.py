import pyaudio
import wave
from extract_audio_feature import extract_audio_feature
import numpy as np
import train_audio
import turicreate_classifier


WAVE_OUTPUT_FILENAME = "../Output/output.wav"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
RECORD_SECONDS = 5


def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def predict_emotion():
    audio_features = extract_audio_feature(WAVE_OUTPUT_FILENAME).split()
    result1 = train_audio.predict(np.array(audio_features, dtype=float))
    result2 = turicreate_classifier.predict(WAVE_OUTPUT_FILENAME)

    for i in range(0, result1.shape[0]):
        emotion, confidence = handle_onehot(result1[i])
        print('custom model result:[emotion:', emotion, ', confidence:', confidence, ']')
    for i in range(0, result2.shape[0]):
        emotion, confidence = handle_onehot(np.array(result2[i]))
        print('turicreate result:[emotion:', emotion, ', confidence:', confidence, ']')


def handle_onehot(onehot):
    emotions = 'neutral calm happy sad angry fearful disgust surprised'.split()
    confidence = max(onehot)
    itemindex = np.where(onehot == confidence)[0][0]
    emotion = emotions[itemindex]
    return emotion, confidence


if __name__ == '__main__':
    record_audio()
    predict_emotion()
