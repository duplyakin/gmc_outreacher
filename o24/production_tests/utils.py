from o24.backend.dashboard.models import User, Team, Credentials, Campaign, Prospects, ProspectsList
import json
from pprint import pprint

from o24.backend.utils.decors import get_token
import string
import random


TEST_USER_EMAIL = '1@email.com'

def get_current_user():
    return User.objects(email=TEST_USER_EMAIL).first()

def random_num(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def post_with_token(user, client, url, data, follow_redirects=False):
    token = get_token(user)
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    print("Sending request to url:{0}".format(url))
    pprint(data)
    
    r = None
    if data:        
        r = client.post(url, data=data, content_type='multipart/form-data', headers=headers, follow_redirects=follow_redirects)
    else:
        r = client.post(url, content_type='multipart/form-data', headers=headers, follow_redirects=follow_redirects)

    return r
