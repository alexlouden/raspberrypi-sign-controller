#!/usr/bin/env python2.7
import atexit
import sys
import time
import threading
from Queue import Queue, Empty
from flask import Flask, request, render_template
from sign import Sign


queue = Queue()
stop = threading.Event()
t = None


def do_command(sign, command, args):

    if command == 'change_modes':
        sign.change_modes()
    else:
        sign.mode = 'noop'

        if command == 'off':
            sign.strip.set_colour_rgb(0, 0, 0)

        if command == 'on':
            sign.mode = 'aqua'
            sign.tick()

        elif command == 'red':
            sign.strip.set_colour_rgb(255, 0, 0)

        elif command == 'green':
            sign.strip.set_colour_rgb(0, 255, 0)

        elif command == 'blue':
            sign.strip.set_colour_rgb(0, 0, 255)

        elif command == 'set_rgb':
            sign.strip.set_colour_rgb(*args)


def loop():

    sign = Sign()

    while not stop.is_set():
        try:
            pop = queue.get_nowait()
            command = pop[0]
            args = pop[1:]

            do_command(sign, command, args)

        except Empty:
            pass

        if sign.mode != 'noop':
            sign.tick()

        time.sleep(0.01)

    print('End of loop')


def create_app():
    app = Flask(__name__, template_folder='.')

    t = threading.Thread(target=loop)
    t.daemon = True
    t.start()

    return app


app = create_app()


@app.route("/change_modes")
def change_modes():
    queue.put_nowait(('change_modes', ))
    return "Changing modes!"


@app.route("/off")
def off():
    queue.put_nowait(('off', ))
    return "Bye!"


@app.route("/on")
def on():
    queue.put_nowait(('on', ))
    return "Hey!"


@app.route("/red")
def red():
    queue.put_nowait(('red', ))
    return "Red!"


@app.route("/green")
def green():
    queue.put_nowait(('green', ))
    return "Red!"


@app.route("/blue")
def blue():
    queue.put_nowait(('blue', ))
    return "Red!"


@app.route("/rgb/<r>,<g>,<b>")
def set_rgb(r, g, b):
    queue.put_nowait(('set_rgb', int(r), int(g), int(b)))
    return "Bye!"


@app.route("/")
def home():
    return render_template('index.html', host=request.host)


def die():
    stop.set()


if __name__ == '__main__':
    print('Starting up')
    atexit.register(die)
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print('Shutting down')

        sign = Sign()
        sign.strip.set_colour_rgb(0, 0, 0)
    finally:
        # Trigger stop
        stop.set()
        sys.exit(0)
