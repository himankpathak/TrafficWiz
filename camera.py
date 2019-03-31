import cv2
import threading

first = True;
class VideoCamera(object):
    def __init__(self,path):
        self.video = cv2.VideoCapture(path)
        self.is_record = False
        self.recordingThread = None
        self.new = False;

    def __del__(self):
        self.stop_record()
        self.video.release()

    def get_frame(self,callback):
        global first
        self.new = True;
        success, image = self.video.read()
        image = callback(image)
        self.curimage = image;
        print(image.shape)
        if first is True:
            first = False
            self.start_record();
        ret, jpeg = cv2.imencode('.jpg', image)
        self.new = False
        return jpeg.tobytes()

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

class RecordingThread (threading.Thread):
    def __init__(self, name, videocamera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.cam = videocamera
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.out = cv2.VideoWriter('./static/video5.avi',fourcc, 60.0, (1920,1080))

    def run(self):
        while self.isRunning:
            frame = self.cam.curimage;
            # self.out.write(frame) #comment to stop saving
        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()
