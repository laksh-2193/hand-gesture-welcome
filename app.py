from flask import Flask, render_template, Response, redirect, url_for
import cv2
from lkhandmapping import handTracker
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)

camera = cv2.VideoCapture(0)

# Fetch the service account key JSON file contents
cred = credentials.Certificate('secretkey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://welcometoatriauniversity-default-rtdb.firebaseio.com/"
})

ref = db.reference('index')
gestureRecognized = ""

@app.route('/')
def index():
    return render_template('index.html',gestureRecognized=gestureRecognized)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = handTracker(frame)
            ret, buffer = cv2.imencode('.jpg', frame[0])
            handlms = frame[1]

            if(len(handlms)>1):
                fingerTips = [8, 12, 16, 20]
                fingersUp = [0, 0, 0, 0, 0]
                if (handlms[4][2] < handlms[3][2]):
                    fingersUp[0] = 1

                for i in fingerTips:
                    if (handlms[i][1] > handlms[i - 2][1]):
                        fingersUp[(handlms[i][0] // 4) - 1] = 1
                if(fingersUp[0]==1 and fingersUp.count(0)==4):
                    ref.child("welcome").set("1")
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
