"""
flask + ffmpeg
"""

from __future__ import print_function
import os
from flask import *
import time
import queue as Queue
import threading
from multiprocessing import Process
import random
from camera_ff import Camera

frameRateLimit = 20
commandQueue = Queue.Queue(maxsize=0)

app = Flask(__name__)

LEFT, RIGHT, FORWARD, BACKWARD, PAUSE, STOP = "left", "right", "forward", "backward", "pause", "stop"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Right': RIGHT,
    'Forward': FORWARD,
    'Backward': BACKWARD,
    'Pause': PAUSE,
    'Stop': STOP
}


@app.route('/')
def index():
    return render_template('index2.html', commands=AVAILABLE_COMMANDS)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/gpio')
def gpio():
    try:
        lang = request.args.get('command', 0, type=str)
        lang = lang.lower()
        if lang == LEFT:
            commandQueue.put(lang)
            return jsonify(result='left')
        elif lang == RIGHT:
            commandQueue.put(lang)
            return jsonify(result='right')
        elif lang == FORWARD:
            commandQueue.put(lang)
            return jsonify(result='forward')
        elif lang == BACKWARD:
            commandQueue.put(lang)
            return jsonify(result='backward')
        elif lang == PAUSE:
            commandQueue.put(lang)
            return jsonify(result='pause')
        elif lang == STOP:
            return jsonify(result='Stop')
        else:
            return jsonify(result='Try again.')
    except Exception as e:
        return str(e)

@app.route('/live/<path:filename>')
def send_live(filename):
    return send_from_directory('live', filename)

def start_server(app):
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(
        os.getenv('PORT', 8080)), threaded=True)

if __name__ == '__main__':
    _hash = random.getrandbits(128)
    # start live stream in new process so there is no IO
    live_cam = Camera()
    live_proc = Process(target=live_cam.run, args=("%032x"%_hash,), daemon=True)
    live_proc.start()
    # start server in new thread so that it can end properly?
    server_thread = threading.Thread(target=start_server, args=(app, ))
    server_thread.start()
