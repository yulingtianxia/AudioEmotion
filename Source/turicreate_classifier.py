import turicreate as tc
from os.path import basename
import time

MODEL_PATH = '../Output/AudioEmotion.model'


def train():
    # Load the audio data and meta data.
    data = tc.load_audio('../AudioData')

    # Calculate the deep features just once.
    data['deep_features'] = tc.sound_classifier.get_deep_features(data['audio'])

    # Join the audio data and the meta data.
    emotions = 'neutral calm happy sad angry fearful disgust surprised'.split()
    data['label'] = data['path'].apply(lambda p: emotions[int(basename(p).split('-')[2]) - 1])

    # Make a train-test split, just use the first fold as our test set.
    train_set, test_set = data.random_split(0.8)

    # Create the model.
    batch_size = 128
    max_iterations = 100
    model = tc.sound_classifier.create(train_set,
                                       target='label',
                                       feature='deep_features',
                                       custom_layer_sizes=[512, 256, 128],
                                       batch_size=batch_size,
                                       max_iterations=max_iterations)

    # Evaluate the model and print the results
    metrics = model.evaluate(test_set)
    print(metrics)

    format_string = "%Y-%m-%d %H:%M:%S"
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    fo = open(f'../Output/logs/batch_size_{batch_size}-max_iterations_{max_iterations}-{str_date}.txt', 'x')
    fo.write(str(metrics))
    fo.close()

    # Save the model for later use in Turi Create
    model.save(MODEL_PATH)

    # Export for use in Core ML
    model.export_coreml(f'../Output/mlmodels/AudioEmotion_{str_date}.mlmodel')


def predict(audio):
    model = tc.load_model(MODEL_PATH)
    data = tc.load_audio(audio)
    predictions = model.predict(data, 'probability_vector')
    return predictions


if __name__ == '__main__':
    train()
