from flask import Flask, render_template, Response, send_file, request
from camera import VideoCamera
import os, signal, subprocess,time

app = Flask(__name__, static_folder='static')

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/download',methods=['POST'])
def download():
    #Initiate server shutdown process
    #os.kill(os.getpid(), signal.SIGINT)

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


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

