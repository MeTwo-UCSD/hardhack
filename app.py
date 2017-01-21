from __future__ import print_function
import os
from flask import Flask, render_template, Response, request, jsonify
from camera import Camera
from buttonScannerHandler import buttonScannerHandler
from raven.contrib.flask import Sentry
import time
import threading


frameRateLimit = 20

app = Flask(__name__)
sentry = Sentry(app, dsn='https://b705ec878ec74aae84c1b26a4194b612:6288485481504394a071e8ba726a84a4@sentry.io/131345')

LEFT, RIGHT, UP, DOWN, STOP = "left", "right", "up", "down", "stop"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Right': RIGHT,
    'Up': UP,
    'Down': DOWN,
    'stop': STOP
}

@app.route('/')
def hello():
		return render_template('index.html', commands=AVAILABLE_COMMANDS)

def gen(camera):
	while True:
		time.sleep(1/10)
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()),
		mimetype='multipart/x-mixed-replace; boundary=frame')

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
		if lang == 'left':
			command_queue.put(lang)
			return jsonify(result='left')
		elif lang == 'right':
			command_queue.put(lang)
			return jsonify(result='right')
		elif lang == 'forward':
			command_queue.put(lang)
			return jsonify(result='up')
		elif lang == 'backward':
			command_queue.put(lang)
			return jsonify(result='down')
		elif lang == 'pause':
			command_queue.put(lang)
			return jsonify(result='stop')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	t = threading.Thread(target=buttonScannerHandler, args=(command_queue,))
	t.start()
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug = True, threaded=True)
