# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Prospects, User, Campaign, ProspectsList, Credentials
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
from o24.backend.utils.helpers import template_key_dict, to_json_deep_dereference
import json
import traceback

import o24.backend.models.shared as shared
from o24.backend.dashboard.serializers import JSCampaignData
import o24.backend.scheduler.scheduler as scheduler
from o24.backend.utils.decors import auth_required



