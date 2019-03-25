import turicreate as tc
from os.path import basename

MODEL_PATH = '../Output/AudioEmotion.model'


def train():
    # Load the audio data and meta data.
    data = tc.load_audio('../AudioData')

    # Join the audio data and the meta data.
    emotions = 'neutral calm happy sad angry fearful disgust surprised'.split()
    data['label'] = data['path'].apply(lambda p: emotions[int(basename(p).split('-')[2]) - 1])

    # Make a train-test split, just use the first fold as our test set.
    train_set, test_set = data.random_split(0.8)

    # Create the model.
    model = tc.sound_classifier.create(train_set, target='label', feature='audio', batch_size=256, max_iterations=50)

    # Evaluate the model and print the results
    metrics = model.evaluate(test_set)
    print(metrics)

    # Save the model for later use in Turi Create
    model.save(MODEL_PATH)

    # Export for use in Core ML
    model.export_coreml('../Output/AudioEmotion.mlmodel')


def predict(audio):
    model = tc.load_model(MODEL_PATH)
    data = tc.load_audio(audio)
    predictions = model.predict(data, 'probability_vector')
    return predictions


if __name__ == '__main__':
    train()
