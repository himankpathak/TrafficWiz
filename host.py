import main, ocrTesseract
from flask import Flask, render_template, Response
from camera import VideoCamera
from ImageLoader import ImageLoader
import camera
import time

frame = None
play = True

def gen(camera,callback):
    global frame,play;
    while True:
        if play:
            frame = camera.get_frame(callback)
        else:
            time.sleep(1)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pause')
def pause():
    global play
    play = False;
    return 'Paused';

@app.route('/play')
def play():
    global play
    play = True;
    return 'Playing';

@app.route('/stream')
def stream():
    return render_template('stream.html',value=str(main.getVcount()))

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/ocr')
def ocr():
    return render_template('ocr.html')

@app.route('/nextimage/<index>')
def nextimage(index):
    data = imloader.next(index);
    return data;

cam = VideoCamera(main.videopath)
imloader = ImageLoader('./static/Saved')

@app.route('/video_feed')
def video_feed():
    global play,cam
    return Response(gen(cam,main.process),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
