# Imports
import os, sys

import cv2
from socketIO_client import SocketIO
cd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cd)

sys.path.insert(0, os.path.join(cd, 'libs'))

from darkflow.net.build import TFNet

# Server parameters
host = 'localhost'
port = 5000

# Detection and tracking parameters
detection_frequency = 30  # Detects every 30 frames


class ObjectRecognitionBlackbox:
    def __init__(self, io, detector, tracker, detection_frequency):
        self.io = io
        self.detector = detector
        self.tracker = tracker
        self.frame_counter = 0
        self.detection_frequency = detection_frequency
        self.detect = True
        self.players_table = []
        self.current_players = []

    def incrementFrame(self):
        self.detect = self.frame_counter % self.detection_frequency == 0
        self.frame_counter += 1

    def controller(self, data):
        self.incrementFrame()
        if self.detect:
            # print("Detecting boxes")
            boxes = self.detector.detect(data)
            playersBoxes = self.labelBoxes(boxes)
            self.tracker.initialize_track(data, playersBoxes)
        else:
            # print("Tracking boxes")
            ok, screen_players = self.tracker.track(data)
            self.updateCurrentPlayers(screen_players)
        self.io.send(self.current_players)

    def updateCurrentPlayers(self, screen_players):
        for i in range(len(screen_players)):
            self.current_players[i]["box"] = screen_players[i]

    def labelBoxes(self, boxes):
        self.current_players = []
        res = []
        for box in boxes:
            id = self.identifyPlayer(box)
            x = box["topleft"]["x"]
            y = box["topleft"]["y"]
            h = box["bottomright"]["y"] - y
            w = box["bottomright"]["x"] - x
            self.current_players.append(dict({"id": id, "box": (x, y, h, w)}))
            res.append((x, y, h, w))
        return res

    def identifyPlayer(self, box):
        return 1

    def run(self):
        self.io.connect()
        self.io.listen(self.controller)
        self.io.disconnect()


class SocketInputOutput:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socketio = SocketIO(host, port)

    def connect(self):
        self.socketio.on('connect', self.connected_callback)
        self.socketio.on('reconnect', self.reconnected_callback)
        self.socketio.on('disconnect', self.disconnected_callback)
        self.socketio.emit('join', 'OR')

    def disconnect(self):
        self.socketio.emit('leave', 'OR')

    def listen(self, listener):
        self.socketio.on('video_stream', listener)
        self.socketio.wait()

    def send(self, data):
        self.socketio.emit('OR', data)

    def connected_callback(self):
        print("Connected to server: " + self.host + ":" + self.port + "!")

    def reconnected_callback(self):
        print("Reconnected to server: " + self.host + ":" + self.port + "!")

    def disconnected_callback(self):
        print("Disconnected from server: " + self.host + ":" + self.port + "!")


class FileInputOutput:
    def __init__(self, filename):
        self.filename = filename

    def connect(self):
        self.video = cv2.VideoCapture(self.filename)
        if not self.video.isOpened():
            print("Could not open video")
            sys.exit()

    def disconnect(self):
        self.video.release()

    def listen(self, listener):
        while True:
            # Read a new frame
            ok, frame = self.video.read()
            if not ok:
                break
            listener(frame)

    def send(self, data):
        print(data)


class YoloDetector:
    def __init__(self):
        self.options = {
            "model": "yolov2.cfg",
            "load": "yolov2.weights",
            "threshold": 0.35
        }
        self.tfnet = TFNet(self.options)

    def detect(self, imgcv):
        return self.tfnet.return_predict(imgcv)


class OpenCVTracker:
    def __init__(self):
        pass

    def initialize_track(self, image, boxes):
        # return boxes
        self.tracker = cv2.MultiTracker_create()
        for box in boxes:
            self.tracker.add(cv2.TrackerMedianFlow_create(), image, box)

    def track(self, image):
        return self.tracker.update(image)


print(__name__)
if __name__ == '__main__':
    # io = SocketInputOutput(host, port)
    io = FileInputOutput("test1.mp4")
    detector = YoloDetector()
    tracker = OpenCVTracker()
    ObjectRecognitionBlackbox(io, detector, tracker, detection_frequency).run()

cv2.destroyAllWindows()
