from flask import Flask, request, Response, jsonify, make_response, send_file, json
import requests




app = Flask(__name__)

def start_app(**kwargs):
    global work, work_type, workers

    work = ['image_resize', 'mushroom_ify']
    work_type = {'image_resize' : 'json', 'mushroom_ify' : 'image/png'}
    #workers = ['mapreducey-1.herokuapp.com', 'mapreducey-2.herokuapp.com']
    workers = ['localhost:5000', 'localhost:5000']

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
        if 'callback_url' in params:
            import threading
            threading.Thread(target=globals()[params['work']], kwargs=params).start()
            data['response'] = "You should receive an answer at %s" % params['callback_url']
        else:
            data['response'] = globals()[params['work']](**params)

        if work_type[params['work']] != 'json' and 'callback_url' not in params:
            return send_file(data['response'], mimetype = work_type[params['work']])
        response = jsonify(data)
        response.status_code = 200
        return response        
    elif purpose == 'router':
        worker = random.choice(workers)
        callback_url = 'http://' + worker + '/work'
        params['routed'] = True
        r = requests.get(callback_url, params = params)
        if work_type[params['work']] != 'json' and 'callback_url' not in params:
            import cStringIO
            return send_file(cStringIO.StringIO(r.content), mimetype = work_type[params['work']])
        data['response'] = r.json()
        data['worker_url'] = worker
        data['router_url'] = request.url_root[7:-1]
        response = jsonify(data)
        response.status_code = 200
        return response

@app.route('/callback/work', methods=['GET','POST'])
def callbackWork():
    if request.method == 'POST':
        with open("callback_log.txt", "a") as myfile:
            print request.data
            myfile.write(json.dumps(request.data) + "\n")
        return jsonify(items=request.data)
    else:
        params = request.args.to_dict()
        data = {"purpose" : purpose, "message" : "I did your work", "params" : params, "answer" : "yes"}
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

    result = "<img src='%s' width='%s' height='%s'>" % (kwargs['img_url'], kwargs['width'], kwargs['height'])
    if 'callback_url' not in kwargs:
        return result
    requests.post(kwargs['callback_url'], result)

def mushroom_ify(**kwargs):
    from PIL import Image
    import cStringIO

    if 'url2' not in kwargs:
        kwargs['url2'] = 'http://www.details.com/blogs/daily-details/hopper_mugshot_460.jpg'


    background = Image.open('mushroom-cloud.jpg', 'r')
    img1 = None
    bg_w,bg_h=background.size

    result = Image.new("RGBA", (bg_w, bg_h))
    result.paste(background)
    background = None

    img2 = cStringIO.StringIO(requests.get(kwargs['url2']).content)
    img=Image.open(img2,'r')
    img2 = None
    img_w,img_h=img.size
    offset=((bg_w-img_w)/2,(bg_h-img_h)/2)
    result.paste(img,offset)
    img = None

    output = cStringIO.StringIO()
    result.save(output, format="PNG")
    output.seek(0)
    result = None

    if 'callback_url' not in kwargs:
        return output
    print "post return value to callback_url"

    #result = output.getvalue().encode("base64")
    #output.close()
    #result = '<img src="data:image/png;base64,' + result + '" />'
    #return result




if __name__ == '__main__':
    app.debug = True
    my_env = 'sandbox'
    start_app()
    app.run()
else:
    app.debug = True
    my_env = 'production'
