# Import flask dependencies
from flask import Blueprint, request, jsonify, render_template, \
                  flash, g, session, redirect, url_for, render_template_string, Response
from werkzeug.security import check_password_hash, generate_password_hash
from o24.backend.dashboard.models import User, Credentials

from jinja2 import TemplateNotFound
from mongoengine.queryset.visitor import Q

import o24.backend.scheduler.models as scheduler_models

from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
import o24.backend.models.inbox.mailbox as mailbox
import base64
import json
import traceback 

b64_image = base64.b64decode("R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")

@bp_dashboard.route('/ot/<string:code>/<string:track_event>', methods=['GET'])
def track_open(code, track_event):
    pixel_data = b64_image

    try:
        prospect_id, campaign_id = mailbox.TrackEvents.track_event(code=code, event=track_event)
        if not prospect_id or not campaign_id:
            raise Exception("track_open ERROR: Both should exist prospect_id={0} campaign_id={1}".format(prospect_id, campaign_id))
        
        scheduler_models.TaskLog.track_email_open(prospect_id=prospect_id, campaign_id=campaign_id)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

    return Response(pixel_data, mimetype="image/gif")