from flask import Flask, request, Response, jsonify
import requests




app = Flask(__name__)

def start_app(**kwargs):
    global purpose
    if 'purpose' in kwargs and kwargs['purpose'] in ['router','worker']:
        purpose = kwargs['purpose']
    else:
        purpose = 'worker'
    return app


@app.route('/work')
def work():
    data = {"purpose" : purpose, "message" : "I do work for these params", "params" : request.args}
    callback_url = request.url_root + 'callback/work'
    r = requests.get(callback_url, params = request.args)
    data['callback_response'] = r.json()
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route('/callback/work')
def callbackWork():
    data = {"purpose" : purpose, "message" : "I did your work", "params" : request.args, "answer" : "yes"}
    response = jsonify(data)
    response.status_code = 200
    return response

@app.route('/callback/hereiam')
def callbackHereiam():
    data = {"params" : request.args, "purpose" : purpose}
    response = jsonify(data)
    response.status_code = 200
    return response





if __name__ == '__main__':
    app.debug = True
    my_env = 'sandbox'
    app.run()
else:
    app.debug = True
    my_env = 'production'
