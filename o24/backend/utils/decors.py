from functools import wraps
from flask import g, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token
import o24.backend.dashboard.models as models

def get_token(user):
    return create_access_token(identity=str(user.id))

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
        
            user = models.User.objects().get(id=user_id)
            
            if not user:
                return jsonify(msg='No such user'), 403
            else:
                g.user = user
                return fn(*args, **kwargs)
        except:
                return jsonify(msg='No such user'), 403
  
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            user = models.User.objects().get(id=user_id)
            if not user or user.role != 'admin':
                return jsonify(msg='Admins only!'), 403
            else:
                g.user = user
                return fn(*args, **kwargs)
        except:
            return jsonify(msg='No such user'), 403

    return wrapper
