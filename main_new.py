from flask import Flask, render_template, Response, send_file, request
from camera import VideoCamera
import os
import sys
import subprocess
import time
import librosa
import IPython.display as ipd
from IPython.display import Audio
import numpy as np
import warnings
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__, static_folder='static')

# Function to predict emotion from audio
def predict_emotion(audio_file_path):
    # Your speech emotion prediction code here
    # Load model, preprocess audio, make prediction, and return emotion label
    return "Happy"  # Placeholder for actual prediction


# Function to generate frames for video feed
def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/download', methods=['POST'])
def download():
    # Define the path to your Excel file
    excel_file_path = './generated/results.xlsx'
    return send_file(excel_file_path, as_attachment=True, download_name='emotions_results.xlsx')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index.html')
def home1():
    return render_template('index.html')


@app.route('/face.html')
def face_emotion():
    return render_template('face.html')


@app.route('/speech.html')
def speech_emotion():
    return render_template('speech.html')


@app.route('/team.html')
def team():
    return render_template('team.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


# Route to handle video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


# Route to predict speech emotion
@app.route('/predict_speech_emotion', methods=['POST'])
def predict_speech_emotion():
    if request.method == 'POST':
        audio_file = request.files['audio']
        # Save the uploaded audio file temporarily
        audio_file_path = 'temp_audio.wav'
        audio_file.save(audio_file_path)
        # Call the predict_emotion function with the audio file path
        predicted_emotion = predict_emotion(audio_file_path)
        # Remove the temporary audio file
        os.remove(audio_file_path)
        # Return the predicted emotion as a response
        return predicted_emotion


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
