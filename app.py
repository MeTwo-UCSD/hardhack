from __future__ import print_function
import os
from flask import Flask, render_template, Response, request, jsonify
from camera import Camera
import Queue
from raven.contrib.flask import Sentry
import time

frameRateLimit = 20

app = Flask(__name__)
sentry = Sentry(app, dsn='https://b705ec878ec74aae84c1b26a4194b612:6288485481504394a071e8ba726a84a4@sentry.io/131345')
command = Queue.Queue()

LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Right': RIGHT,
    'Up': UP,
    'Down': DOWN,
    'Reset': RESET
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


@app.route('/gpio')
def gpio():
	#try:
	lang = request.args.get('proglang', 0, type=str)
	if lang.lower() == 'python':
		return jsonify(result='You are wise')
	else:
		return jsonify(result='Try again.')
	#except Exception as e:
	#	return str(e)

if __name__ == '__main__':
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug = True, processes = 3)
