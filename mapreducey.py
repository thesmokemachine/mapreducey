from flask import Flask
from flask import request

import json


app = Flask(__name__)

@app.route('/work')
def work():
    return "I do work for these params: " + json.dumps(request.args)

@app.route('/callback/work')
def callbackWork():
    return "I accept updates on completed work from workers. my_env: " + my_env

@app.route('/callback/hereiam')
def callbackHereiam():
    return "I accept heartbeats from workers if I am a router."


if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'localhost:5000'
    my_env = 'sandbox'
    app.debug = True
    app.run()
else:
    my_env = 'production'
