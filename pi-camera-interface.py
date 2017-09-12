from flask import Flask, request, render_template, send_from_directory
import subprocess
import time
import os

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def camera_control():
    if request.method == 'POST':
        timestamp = int(time.time())
        subprocess.call(["raspivid","-o", "recordings/pi-{}.h264".format(timestamp)])
        subprocess.call(["MP4Box", "-add", "recordings/pi-{}.h264".format(timestamp), "recordings/pi-{}.mp4".format(timestamp)])
        subprocess.call(["ffmpeg", "-i", "recordings/pi-{}.mp4".format(timestamp), "-vframes", "1", "-o", "thumbs/pi-{}.mp4.jpg".format(timestamp)])
        subprocess.call(["rm", "recordings/pi-{}.h264".format(timestamp)])
        return render_template('camera-interface.html')
    else:
        saved_recordings = os.listdir('recordings')
        return render_template('camera-interface.html', saved_recordings=saved_recordings)

@app.route('/recordings/<path:filename>')
def serve_video(filename):
    return send_from_directory('recordings', filename=filename, mimetype='video/mp4')

@app.route('/thumbs/<path:filename>')
def serve_thumbnail(filename):
    return send_from_directory('thumbs', filename=filename, mimetype='img/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
