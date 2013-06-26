import mapreducey
from google.appengine.ext.webapp.util import run_wsgi_app


app = mapreducey.start_app(purpose = 'worker')
run_wsgi_app(app)
