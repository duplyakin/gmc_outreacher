# Import flask dependencies
from flask import Blueprint, request, jsonify, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials
from jinja2 import TemplateNotFound
from mongoengine.queryset.visitor import Q

from o24.backend.google.provider.oauth_provider import GoogleOauthProvider
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *

import json
import traceback
from o24.backend.utils.decors import auth_required


@bp_dashboard.route('/dashboard/gmail-oauth', methods=['GET', 'POST'])
#@auth_required
def dashboard_oauth_button():
    #TODO: for test purpose only TEST-REMOVE
    user_id = request.args.get('user_id', None)
    if not user_id:
        return jsonify(msg='No user_id'), 403
    
    user = User.objects(id=user_id).get()
    if not user:
        return jsonify(msg='No such user'), 403
    else:
        g.user = user

    current_user = g.user

    provider = GoogleOauthProvider()

    current_state = current_user.new_oauth_state()

    auth_url, state = provider.get_gmail_auth_url(current_state=current_state)

    return redirect(auth_url)


@bp_dashboard.route('/oauth/callback', methods=['GET', 'POST'])
def dashboard_oauth_callback():
    
    #TODO: for test purpose only TEST-REMOVE
    state = request.args.get('state', None)
    if not state:
        return jsonify(msg='No state'), 403

    current_user = User.get_by_state(state=state)
    if not current_user:
        return jsonify(msg='No such user'), 403


    provider = GoogleOauthProvider()

    current_state = current_user.current_oauth_state

    if not provider.valid_state(state, current_state):
        raise GoogleOauthError("session ouath_state and user state are not equal")

    access_credentials, email, expiry = provider.set_gmail_auth_credentials(request.url, current_state)

    GMAIL_TYPE = 'api'
    if '@gmail.com' in email:
        GMAIL_TYPE = 'smtp'

    medium = 'email'
    modification = GMAIL_TYPE
    data = {
        'email' : email,
        'account' : email,
        'credentials' : access_credentials,
        'expiry' : expiry,
        'sender' : GMAIL_TYPE
    }
    Credentials.create_credentials(owner=current_user.id,
                                    medium=medium,
                                    modification=modification,
                                    new_data=data)

    return '<script type="text/javascript">window.close();</script>'
    #return render_template('dashboard/oauth-callback.html')
