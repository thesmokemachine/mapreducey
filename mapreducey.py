from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

@app.route('/work')
def work():
    data = {"message" : "I do work for these params", "params" : request.args}
    callback_url = 'http://' + app.config['SERVER_NAME'] + '/callback/work'
    r = requests.get(callback_url, params = request.args)
    data['callback_response'] = r.json()
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route('/callback/work')
def callbackWork():
    data = {"message" : "I did your work", "params" : request.args, "answer" : "yes"}
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route('/callback/hereiam')
def callbackHereiam():
    data = {"params" : request.args}
    response = jsonify(data)
    response.status_code = 200
    return response





if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'localhost:5000'
    my_env = 'sandbox'
    app.debug = True
    app.run()
else:
    if app.config['SERVER_NAME'] is None:
        app.config['SERVER_NAME'] = 'localhost:5000'
    app.debug = True
    my_env = 'production'
