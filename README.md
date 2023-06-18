# mcivor-windtunnel-control-api

This is designed to work with `jamesmcfarland/mcivor-windtunnel-control` and run on a raspberry pi to control a set of fans for a wind tunnel.

This is simply a backend which takes the desired fan speeds and sends the signals to the controller, and returns the current speed of the fans.

It uses `flask`, `flask-cors` and `RPI.GPIO`.

## Installation

Install Dependancies:
`pip install -r requirements.txt`

Run the app: `flask run`
