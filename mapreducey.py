from flask import Flask, request, Response, jsonify
import requests




app = Flask(__name__)

def start_app(**kwargs):
    global work
    work = ['image_resize']

    global workers
    workers = ['mapreducey-1.appspot.com', 'mapreducey-1.herokuapp.com']
    #workers = ['localhost:8080','localhost:5000']

    global purpose
    if 'purpose' in kwargs and kwargs['purpose'] in ['router','worker']:
        purpose = kwargs['purpose']
    else:
        purpose = 'worker'
    return app


@app.route('/work')
def work():
    import random
    data = {}
    params = request.args.to_dict()
    if not (params['work'] and params['work'] in work):
        response = {"message": "Work type %s not found." % params['work'], "viable_work" : work}
        response = jsonify(response)
        response.status_code = 501
        return response
    elif purpose == 'worker' or 'routed' in params.keys():
        data['response'] = globals()[params['work']](**params)
        response = jsonify(data)
        response.status_code = 200
        return response        
    elif purpose == 'router':
        worker = random.choice(workers)
        callback_url = 'http://' + worker + '/work'
        params['routed'] = True
        r = requests.get(callback_url, params = params)
        data['response'] = r.json()
        data['worker_url'] = worker
        data['router_url'] = request.url_root[7:-1]
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


def image_resize(**kwargs):
    vars = ['img_url', 'width', 'height']
    intersection = set(kwargs.keys()) & set(vars)
    if len(vars) != len(intersection):
        return "Please pass these vars: %s. I received: %s" % (sorted(vars), sorted(list(intersection)))

    return "<img src='%s' width='%s' height='%s'>" % (kwargs['img_url'], kwargs['width'], kwargs['height'])



if __name__ == '__main__':
    app.debug = True
    my_env = 'sandbox'
    app.run()
else:
    app.debug = True
    my_env = 'production'
