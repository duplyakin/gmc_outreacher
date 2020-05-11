# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from werkzeug.security import check_password_hash, generate_password_hash
from flask_user import login_required, current_user
from o24.backend.dashboard.models import User, Credentials
from jinja2 import TemplateNotFound
from mongoengine.queryset.visitor import Q

from o24.backend.google.provider.oauth_provider import GoogleOauthProvider
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import json
import traceback

CORS(app, resources={r'/*': {'origins': '*'}})


def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


@bp_dashboard.route('/test', methods=['GET', 'POST'])
@login_required
def dashboard_main():
    return 'Hello world'

@bp_dashboard.route('/dashboard/gmail-oauth', methods=['GET', 'POST'])
#@login_required
def dashboard_oauth_button():
    #TODO: for test purpose only TEST-REMOVE
    current_user = get_current_user()

    provider = GoogleOauthProvider()

    current_state = current_user.get_oauth_state()

    auth_url, state = provider.get_gmail_auth_url(current_state=current_state)

    session['oauth_state'] = state

    return redirect(auth_url)


@bp_dashboard.route('/oauth/callback', methods=['GET', 'POST'])
#@login_required
def dashboard_oauth_callback():
    
    #TODO: for test purpose only TEST-REMOVE
    current_user = get_current_user()

    provider = GoogleOauthProvider()

    state = session['oauth_state']
    current_state = current_user.get_oauth_state()

    if not provider.valid_state(state, current_state):
        raise GoogleOauthError("session ouath_state and user state are not equal")

    access_credentials, email = provider.set_gmail_auth_credentials(request.url, current_state)

    GMAIL_TYPE = 'api'
    if '@gmail.com' in email:
        GMAIL_TYPE = 'smtp'

    medium = 'email'
    data = {
        'email' : email,
        'account' : email,
        'credentials' : access_credentials,
        'sender' : GMAIL_TYPE
    }
    Credentials.create_credentials(owner=current_user.id,
                                    medium=medium,
                                    new_data=data)

    return '<script type="text/javascript">window.close();</script>'
    #return render_template('dashboard/oauth-callback.html')
