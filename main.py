#!/usr/bin/python3
import math
from time import sleep
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

NUM_LEDS = 31
USE_LEDS = False

if USE_LEDS:
	import ledstrip

class Color(object):
    def __init__(self):
        self.r = 255
        self.g = 0
        self.b = 0

app = Flask(__name__)
socketio = SocketIO(app)
color = Color()

if USE_LEDS:
	leds = ledstrip.LEDStrip(NUM_LEDS)
	leds.open()
	# Blink test
	leds.all_on()
	sleep(0.5)
	leds.all_off()

def set_color():
	if USE_LEDS:
		arr = [min(max(color.r, 0), 255),
			min(max(color.g, 0), 255),
			min(max(color.b, 0), 255)]
		payload = []
		for _ in range(NUM_LEDS):
			payload.extend(arr)
		leds.write_gc(payload)

def filter_message(msg):
	sep = msg.split(":")
	if len(sep) != 2 or ":" not in msg:
		print("Something is wrong.")
		return
	clr = sep[0].strip()
	val = int(sep[1])
	val = min(max(0, val), 255)
	
	print("r:{0} g:{1} b:{2}".format(color.r, color.g, color.b))
	
	if clr == "red": color.r = val
	elif clr == "grn": color.g = val
	elif clr == "blu": color.b = val
	else: print("what the fuck")

	set_color()

@app.route("/")
def index():
	return render_template("index.html")

@socketio.on("color change", namespace="/socket")
def color_change(message):
	if message is not None and message["data"] is not None:
		filter_message(message["data"])
		emit("sync", { 
			"color": "r:{0}:g:{1}:b:{2}".format(color.r, color.g, color.b)
		}, broadcast=True, include_self=False)
	else:
		print("The message is none but I'm going to ignore it")
	#print(message["data"])

@socketio.on("connect", namespace="/socket")
def test_connect():
    emit("on_connect", {
    		"data": "Connected",
    		"color": "r:{0}:g:{1}:b:{2}".format(color.r, color.g, color.b)
    	})

if __name__ == "__main__":
	try:
		socketio.run(app, host="0.0.0.0", port=5050, debug=True)
		set_color()
		#socketio.run(app)
	except KeyboardInterrupt:
		pass
	except OSError as e:
		print("lol oserror")
	except ConnectionResetError as e:
		print("lol reseterror")