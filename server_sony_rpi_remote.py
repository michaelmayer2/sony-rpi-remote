#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bottle import post, route, request, run
import os, time

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def release():
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(23, True)
    time.sleep(0.5)
    GPIO.output(25, True)
    time.sleep(0.5)
    GPIO.output(25, False)
    GPIO.output(23, False)

@route('/')
@route('/', method='POST')
def release_control():
    if (request.POST.get("shutter_release")):
        release()
    if (request.POST.get("number")):
        i = 1
        number = int(request.forms.get('number'))
        interval = int(request.forms.get('interval'))
        while (i <= number):
            release()
            time.sleep(interval)
            i = i + 1
    if (request.POST.get("shutdown")):
        os.system("sudo halt")
    return """
    <title>SONY Raspberry Pi Remote</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <form method="POST" action="/">
    <div id="content"><p><input id="btn" name="shutter_release" type="submit" value="Shutter Release"></p>
    <p>Photos: <input name="number" type="text" size="3"/> Interval: <input name="interval" type="text" size="3"/> sec.</p>
    <p><input id="btn" value="Start" type="submit" /></p>
    <p><input id="btn" class="warning" name="shutdown" value="Shutdown" type="submit" /></p>
    </form></div>
    <style>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,600,700' rel='stylesheet' type='text/css'>
    body {
        font: 15px/25px 'Open Sans', sans-serif;
    }
    #content {
        font: 15px/25px 'Open Sans', sans-serif;
        margin: 0px auto;
        text-align: center;
    }
    #btn {
        width: 11em;  height: 2em;
        background: #3399ff;
        border-radius: 5px;
        color: #fff;
        font-family: 'Open Sans', sans-serif; font-size: 25px; font-weight: 900;
        letter-spacing: 3px;
        border:none;
    }
    #btn.warning {
        background: #cc0000;
    }
    </style>
    """
run(host="0.0.0.0",port=8080, debug=True, reloader=True)
