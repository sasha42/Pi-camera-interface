from flask import Flask, request, render_template
import subprocess

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def camera_control():
    if request.method == 'POST':
        subprocess.call(["raspivid","-o", "test2.mp4"])
        return render_template('camera-interface.html')
    else:
        return render_template('camera-interface.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
