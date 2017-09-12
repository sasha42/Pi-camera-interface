from flask import Flask, request, render_template, send_from_directory
import subprocess
import time
import os

app = Flask(__name__)
os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()

@app.route('/')
def camera_control():
    saved_recordings = os.listdir('recordings')
    return render_template('camera-interface.html', saved_recordings=saved_recordings)

@app.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == 'POST':
        timestamp = time.strftime('%H-%M-%S_%Y-%m-%d')
        subprocess.call(["raspivid","-o", "recordings/pi-{}.h264".format(timestamp)])
        subprocess.call(["MP4Box", "-add", "recordings/pi-{}.h264".format(timestamp), "recordings/pi-{}.mp4".format(timestamp)])
        subprocess.call(["ffmpeg", "-i", "recordings/pi-{}.mp4".format(timestamp), "-vframes", "1", "thumbs/pi-{}.mp4.jpg".format(timestamp)])
        subprocess.call(["rm", "recordings/pi-{}.h264".format(timestamp)])
        return render_template('processing.html')
    else:
        return render_template('processing.html')

@app.route('/recordings/<path:filename>')
def serve_video(filename):
    return send_from_directory('recordings', filename=filename, mimetype='video/mp4')

@app.route('/thumbs/<path:filename>')
def serve_thumbnail(filename):
    return send_from_directory('thumbs', filename=filename, mimetype='img/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
