# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, render_template_string
from flask import Flask, jsonify
from o24.backend import db
from o24.backend import app
from o24.backend.dashboard import bp_dashboard
from o24.globals import *
from flask_cors import CORS

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

@bp_dashboard.route('/prospects', methods=['GET', 'POST'])
def prospects():
    return jsonify(PROSPECTS)