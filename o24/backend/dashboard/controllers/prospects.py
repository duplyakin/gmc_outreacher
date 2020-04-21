# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard.models import Prospects, User, ProspectsList, Campaign
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS
import o24.config as config
from o24.backend.utils.serialize import JSONEncoder
import json

PROSPECTS = [
    {
        'id' : 1,
        'email' : 'ks.shilov@gmail.com',
        'name' : 'Kirill1'
    },
    {
        'id' : 2,
        'email' : 'ksshilov@yandex.ru',
        'name' : 'Kirill2'
    },
    {
        'id' : 3,
        'email' : 'ks.shilov+1@gmail.com',
        'name' : 'Kirill3'
    },
    {
        'id' : 4,
        'email' : 'ks.shilov+2@gmail.com',
        'name' : 'Kirill4'
    },

]

CORS(app, resources={r'/*': {'origins': '*'}})

def get_current_user():
    user = User.objects(email='1@email.com').first()
    if not user:
        raise Exception('No such user')
    
    return user


@bp_dashboard.route('/prospects', defaults={'page': 1})
@bp_dashboard.route('/prospects/<int:page>', methods=['GET', 'POST'])
#@login_required
def list_prospects(page):

    current_user = get_current_user()
    result = {
        'lists' : '',
        'campaigns' : '',
        'prospects' : '',
        'columns' : '["Email", "First name", "Last name", "Linkedin", "Campaign", "List"]'
    }
    list_filter = {}

    if request.method == 'GET':
        lists = ProspectsList.async_lists(owner=current_user.id)
        if lists:
            result['lists'] = lists.to_json()

        campaigns = Campaign.async_campaigns(owner=current_user.id)
        if campaigns:
            result['campaigns'] = campaigns.to_json()


    prospects = Prospects.async_prospects(owner=current_user.id,
                                        list_filter=list_filter,
                                        page=page)    
    if prospects:
        result['prospects'] = prospects.to_json()

    return jsonify(result)

@bp_dashboard.route('/prospects/remove/<prospect_id>', methods=['GET', 'POST'])
#@login_required
def remove_prospect(prospect_id):
    return jsonify(PROSPECTS)

@bp_dashboard.route('/prospects/edit/<prospect_id>', methods=['GET', 'POST'])
#@login_required
def edit_prospect(prospect_id):
    return jsonify(PROSPECTS)


@bp_dashboard.route('/prospects/add', methods=['GET', 'POST'])
#@login_required
def add_prospect():
    return jsonify(PROSPECTS)

@bp_dashboard.route('/prospects/upload', methods=['GET', 'POST'])
#@login_required
def upload_prospects ():
    return jsonify(PROSPECTS)

@bp_dashboard.route('/list/create', methods=['GET', 'POST'])
#@login_required
def create_list():
    return jsonify(PROSPECTS)