from functools import wraps
from flask import g, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import o24.backend.dashboard.models as models

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = models.User.objects().get(id=user_id)
        
        if not user:
            return jsonify(msg='No such user'), 403
        else:
            g.user = user
            return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_identity()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper
