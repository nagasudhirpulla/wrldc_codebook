from flask import Blueprint, redirect, request, url_for, session, render_template
import requests
import json
from oauthlib.oauth2 import WebApplicationClient
# from src.config.appConfig import getAppConfig
from src.appConfig import getConfig
import urllib.parse
from src.security.user import User

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)


login_manager = LoginManager()

oauthPage = Blueprint('oauth', __name__,
                      template_folder='templates')

client = None
# # Configuration
# appConfig = getConfig()
# oauth_app_client_id = appConfig["oauth_app_client_id"]
# oauth_app_client_secret = appConfig["oauth_app_client_secret"]
# oauth_provider_discovery_url = (
#     appConfig["oauth_provider_discovery_url"]
# )

# # OAuth2 client setup
# client = WebApplicationClient(oauth_app_client_id)


def initOauthClient():
    global client
    appConfig = getConfig()
    oauth_app_client_id = appConfig["oauth_app_client_id"]
    client = WebApplicationClient(oauth_app_client_id)


def get_oauth_provider_cfg():
    # Configuration
    appConfig = getConfig()
    oauth_provider_discovery_url = (
        appConfig["oauth_provider_discovery_url"]
    )
    return requests.get(oauth_provider_discovery_url, verify=False).json()


@login_manager.user_loader
def load_user(user_id):
    # Flask-Login helper to retrieve a user from our db
    sUser = session['SUSER']
    return User(sUser['id'], sUser['name'], sUser['email'], sUser['roles'])


@oauthPage.route("/login")
def login():
    appConfig = getConfig()
    # oauth_app_client_id = appConfig["oauth_app_client_id"]

    # OAuth2 client setup
    # client = WebApplicationClient(oauth_app_client_id)

    # Find out what URL to hit for Google login
    oauth_provider_cfg = get_oauth_provider_cfg()
    authorization_endpoint = oauth_provider_cfg["authorization_endpoint"]
    # redirectUri = request.base_url
    # if redirectUri[-1] == "/":
    #     redirectUri = redirectUri[:-1]
    # redirectUri = redirectUri + "/callback"

    requestScheme = 'https://' if request.is_secure else 'http://'
    redirectUri = urllib.parse.urljoin(
        requestScheme+request.host, url_for(".callback"))
    if 'x-original-host' in request.headers:
        # https://stackoverflow.com/a/38726543/2746323
        originalHost = request.headers['x-original-host']
        requestScheme = 'https://' if (
            'x-arr-ssl' in request.headers) else 'http://'
        pathForCallback = url_for(".callback")
        redirectUri = urllib.parse.urljoin(
            requestScheme+originalHost, pathForCallback)
    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirectUri,
        scope=["openid", "email", "profile", "roles"],
    )
    return redirect(request_uri)


@oauthPage.route("/login/callback")
def callback():
    appConfig = getConfig()
    oauth_app_client_id = appConfig["oauth_app_client_id"]
    oauth_app_client_secret = appConfig["oauth_app_client_secret"]

    # OAuth2 client setup
    # client = WebApplicationClient(oauth_app_client_id)

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    oauth_provider_cfg = get_oauth_provider_cfg()
    token_endpoint = oauth_provider_cfg["token_endpoint"]

    authResponse = request.url
    redirectUri = request.base_url

    # handle reverse proxy
    if 'x-original-host' in request.headers:
        # manipulate redirectUrl as per reverse proxy host
        originalHost = request.headers['x-original-host']
        originalRequestScheme = 'https://' if (
            'x-arr-ssl' in request.headers) else 'http://'
        pathForCallback = url_for(".callback")
        redirectUri = urllib.parse.urljoin(
            originalRequestScheme+originalHost, pathForCallback)
        # manipulate authResponse as per reverse proxy host
        authResponse.replace(request.host, originalHost)
        if (originalRequestScheme == "https://") and authResponse.startswith("http://"):
            authResponse.replace("http://", "https://")
        if (originalRequestScheme == "http://") and authResponse.startswith("https://"):
            authResponse.replace("https://", "http://")

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=redirectUri,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(oauth_app_client_id, oauth_app_client_secret),
        verify=False,
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = oauth_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(
        uri, headers=headers, data=body, verify=False)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    userInfo = userinfo_response.json()
    if userinfo_response.json().get("email_verified"):
        unique_id = userInfo["sub"]
        users_email = userInfo["email"]
        users_name = userInfo["preferred_username"]
        uRoles = userInfo['resource_access'][oauth_app_client_id]["roles"]
        if not(isinstance(uRoles, list)):
            uRoles = [uRoles]
    else:
        return "User email not available or not verified", 400

    # Create a user in our db with the information provided
    user = User(
        id_=unique_id, name=users_name, email=users_email, roles=uRoles
    )

    session['SUSER'] = {'id': unique_id,
                        'email': users_email, 'name': users_name, 'roles': uRoles}
    # Begin user session by logging the user in
    login_user(user)
    # Send user back to homepage
    return redirect(urllib.parse.urljoin(
            originalRequestScheme+originalHost, url_for("index")))


@oauthPage.route("/logout")
@login_required
def logout():
    # logout from this application
    logout_user()
    appConfig = getConfig()
    oauth_provider_cfg = get_oauth_provider_cfg()
    requestScheme = 'https://' if request.is_secure else 'http://'
    pathForCallback = url_for("index")
    redirectUri = urllib.parse.urljoin(
        requestScheme+request.host, pathForCallback)
    if "id_token" in client.token:
        endSessionEndpoint = oauth_provider_cfg["end_session_endpoint"]
        idToken = client.token["id_token"]
        # handle reverse proxy
        if 'x-original-host' in request.headers:
            # manipulate redirectUrl as per reverse proxy host
            originalHost = request.headers['x-original-host']
            originalRequestScheme = 'https://' if (
                'x-arr-ssl' in request.headers) else 'http://'
            redirectUri = urllib.parse.urljoin(
                originalRequestScheme+originalHost, pathForCallback)
        logoutUrl = "{0}?id_token_hint={1}&post_logout_redirect_uri={2}".format(
            endSessionEndpoint, idToken, redirectUri)
        return redirect(logoutUrl)
        
    else:
        return redirect(redirectUri)