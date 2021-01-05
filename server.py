'''
This is the web server that acts as a service that creates outages raw data
'''
from src.appConfig import getConfig
from src.routeControllers.oauth import login_manager, oauthPage
from src.security.errorHandlers import page_forbidden, page_not_found, page_unauthorized
from flask import Flask, request, jsonify, render_template
from waitress import serve
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from typing import Any, cast
import os
import pandas as pd

# set this variable since we are currently not running this app on SSL
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# get application config
appConfig = getConfig()

appPrefix = appConfig["appPrefix"]
if pd.isna(appPrefix):
    appPrefix = ""

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# limit max upload file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# User session management setup
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('home.html.j2')
    # return "Hello"


app.register_error_handler(401, page_unauthorized)
app.register_error_handler(403, page_forbidden)
app.register_error_handler(404, page_not_found)
app.register_blueprint(oauthPage, url_prefix='/oauth')

hostedApp = Flask(__name__)

cast(Any, hostedApp).wsgi_app = DispatcherMiddleware(NotFound(), {
    appPrefix: app
})

if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        hostedApp.run(host="0.0.0.0", port=int(
            appConfig['flaskPort']), debug=True)
        # app.run(host="0.0.0.0", port=int(
        #     appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(
            appConfig['flaskPort']), url_prefix=appPrefix, threads=1)
