# AudioEmotion

Recognize Audio Emotion.

Eight emotions: neutral, calm, happy, sad, angry, fearful, disgust and surprised.

## Article

[音频情绪识别](http://yulingtianxia.com/blog/2019/03/30/Audio-Emotion-Recognition/)

## Usage

Create "AudioData", "Output/logs", "Output/mlmodels" folders.
Download RAVDESS dataset and put it in "AudioData" folder. 

### Turicreate

1. Replace some Turicreate source files by "Source/Turicreate_Fix/*.py"
2. Train model using `turicreate_classifier.py`.
3. run "iOSSample/AudioEmotion.xcodeproj" on iOS 12(or higher). You can also run `predict_audio_emotion.py` on your Mac/PC.

### Keras

1. run `extract_audio_feature.py`
2. run `train_audio.py`
3. run `predict_audio_emotion.py`



