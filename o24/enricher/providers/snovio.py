from o24.enricher.models import AuthData
import o24.config as config
import requests
import json
from datetime import datetime  
from datetime import timedelta  
from pytz import timezone
import pytz
import traceback
from o24.globals import *


#Provide enrichment
# - try to find by linkedin
# - try to find by domain
# - return ENRICH_FAILED_TO_FOUND 
class SnovioProvider():
    
    THE_END = 'end_of_actions'
    DELAY_SECS = 30

    PROVIDER_IN_PROGRESS = 1  #we successfully push info to API - COST CREDITS
    PROVIDER_DELAY = 2 #the process still in progress - free
    PROVIDER_DATA_NOT_FOUND = 3 #didn't find data - free
    PROVIDER_DATA_FOUND = 4  #found data - COST CREDITS
    PROVIDER_ACTION_FALSE = 5  #request failed - free

    SPENT_CREDITS_STATUS = [1, 4]

    #IF YOU add actions here be sure to udpate _validate_data and include those actions to CAN_SEARCH
    ACTIONS_MAP = {
        0 : 'add_url',
        1 : 'get_url',
        2 : 'get_url',

        3 : 'get_name',

        4 : 'add_name',
        5 : 'get_name',
        6 : 'get_name',

        7 : 'get_domain'
    }
    OUT_OF_RANGE = 8

    CREDITS = {
        'add_url' : 1,
        'get_url' : 0,
        'get_name' : 1,
        'add_name' : 1,
        'get_domain' : 2
    }

    def __init__(self):
        self.credentials = config.SNOVIO_CREDENTIALS
        if not self.credentials:
            raise Exception("can't create provider - credentials can't be emptu check config.SNOVIO_CREDENTIALS")
        
        self.api_url = config.SNOVIO_API_URL
        if not self.api_url:
            raise Exception("can't create provider - api_url can't be empty check config.SNOVIO_API_URL")

                
    def _next_action(self, result_data, can_search):
        if not can_search:
            raise Exception("No keys that can be enriched")
        
        last_action = result_data.get('last_action', '')
        last_index = result_data.get('last_index', None)

        next_action = self.THE_END
        next_index = self.OUT_OF_RANGE
        for index, action in self.ACTIONS_MAP.items():

            #We need to request only APIes we have data for
            if action not in can_search:
                continue
            
            #If we just started then return the first found match action
            if not last_action:
                next_action = action
                next_index = index
                break
            
            if index <= last_index:
                continue
            
            #if we are here - then we found our next action
            next_action = action
            next_index = index
            break


        return next_action, next_index
    
    def _init_state(self, task):
        task.last_spent = 0
    
    def tick(self, task):
        self._init_state(task)

        result_data = task.result_data
        if not result_data:
            result_data = {}

        input_data = task.input_data
        if not input_data:
            raise Exception("can't enrich for empty data")

        prospect_data, can_search = self._validate_data(input_data)
        task.can_search = str(can_search)

        next_action, next_index = self._next_action(result_data, can_search)

        if next_action == self.THE_END:
            return ENRICH_TRIED_ALL
        
        if next_action == 'add_url':
            res = self.api_add_url(url=prospect_data['linkedin'])
        elif next_action == 'get_url':
            res = self.api_get_url(url=prospect_data['linkedin'])
        elif next_action == 'get_name':
            res = self.api_get_name(prospect_data=prospect_data)
        elif next_action == 'add_name':
            res = self.api_add_name(prospect_data=prospect_data)
        elif next_action == 'get_domain':
            res = self.api_get_domain(prospect_data=prospect_data)


        return self._switch_task(task, 
                                next_action, 
                                next_index,
                                res)
    
    def _delay_task(self, task, seconds):
        task.delay(seconds=seconds)

    def _spend_credits(self, task, action):
        cost = self.CREDITS.get(action, None)
        if cost is None:
            print("Can't find cost of action: {0}".format(action))
            return
        
        task.total_spent = task.total_spent + cost
        task.last_spent = cost
        return cost

    def _switch_task(self, task, last_action, last_index, res):
        task.actions_tried.append(last_action)
        
        result_data = task.result_data
        if not result_data:
            result_data = {}
            result_data['data'] = {}
    
        code = res.get('code', None)
        if code < 0:
            result_data['error'] = res

            task.result_data = result_data
            task.status = FAILED
            task._commit()

            return FAILED

        #IF code < 0 then we don't need to store action as it wasn't success
        result_data['last_action'] = last_action
        result_data['last_index'] = last_index

        if res.get('data', None):
            result_data['data'].update(res.get('data'))

        status = ENRICH_IN_PROGRESS
        if code == self.PROVIDER_DATA_FOUND:
            status = ENRICH_SUCCESS
        elif code == self.PROVIDER_DELAY:
            self._delay_task(task=task, seconds=self.DELAY_SECS)

        #IF the request was successful we need to add credits spent
        if code in self.SPENT_CREDITS_STATUS:
            self._spend_credits(task=task, action=last_action)

        task.result_data = result_data
        task.status = status
        task._commit()

        return status

    def _validate_data(self, input_data):
        if not input_data:
            raise Exception("BROKEN DATA: there is no input_data")
        
        can_search = []

        linkedin_url = input_data.get('linkedin', '')
        if linkedin_url:
            can_search.extend(['add_url', 'get_url'])
        
        domain = input_data.get('company_url', '')
        if domain:
            can_search.extend(['get_domain'])
        
        first_name = input_data.get('first_name', '')
        last_name = input_data.get('last_name', '')
        if first_name and last_name and domain:
            can_search.extend(['add_name', 'get_name'])

        if not can_search:
            raise Exception("There is no key to enrich data: should have linkedin or company domain minimum")
        
        return input_data, can_search

    def get_auth_token(self):
        data, expires = AuthData.get_token(key="snovio")

        if (not data) or (self.is_token_expired(expires)):
            data = self.refresh_auth_token()
                
        return data['access_token']

    def is_token_expired(self, expires):
        if expires <= 0 :
            return True

        now = pytz.utc.localize(datetime.utcnow())
        now_posix = now.timestamp()

        return now_posix >= expires

    #throw exception on error
    #1. request the new token
    #2. calculate posix_expires
    #3. AuthData.save_token
    # RETURN: json data
    def refresh_auth_token(self):
        url = self.api_url + '/oauth/access_token'

        res = requests.post(url, data=self.credentials)
        raw = res.text.encode('ascii','ignore')
        if not raw:
            raise Exception("EMPTY RESPONSE: can't receive access token")

        data = json.loads(raw)
        if not data:
            raise Exception("EMPTY RESPONSE serialization: data can't be ampty")
        
        posix_expires = self._expires_from_now(expires_sec=data['expires_in'])

        AuthData.save_token(key="snovio", data=data, posix_expires=posix_expires)

        return data

    def _expires_from_now(self, expires_sec):
        now = pytz.utc.localize(datetime.utcnow())
        now_posix = now.timestamp()

        return now_posix + expires_sec

    
    #Snov.io api requests
    def _safe_request(self, api_url, params, post=True, headers={}, form=False):
        try:
            res = 'Unknow error'
            if form:
                res = requests.post(api_url, headers=headers, data=params, files=[])
            else:
                if post:
                    res = requests.post(api_url, data=params, headers=headers)
                else:
                    res = requests.get(api_url, data=params, headers=headers)

            res = json.loads(res.text)
            message = res.get('message', '')
            if message:
                if 'ran out of credits' in message:
                    raise Exception("BUDGET ERROR: snovio api stopped: ran out of credits, {0}".format(message))
        except Exception as e:
            return str(e)

        return res

    def api_add_url(self, url):
        api_url = self.api_url + '/add-url-for-search'

        res = {
            'code' : -1
        }
        if not url:
            return res
        
        token = self.get_auth_token()
        
        headers = {
            'Authorization': 'Bearer ' + token
        }
        
        params = {
            'url': url
        }

        api_response = self._safe_request(api_url=api_url, params=params, post=True, headers=headers, form=True)
        if type(api_response) == str:
            res['message'] = api_response
            return res
        
        is_true = api_response.get('success', False)
        message = api_response.get('message', '')
        if not is_true:
            res['message'] = message
            res['code'] = self.PROVIDER_IN_PROGRESS
            return res
        
        res['code'] = self.PROVIDER_IN_PROGRESS
        return res

    def _extract_emails_from_data(self, prospect):
        
        prospect_details = {}
        first_name = prospect.get('firstName', '')
        if first_name:
            prospect_details['first_name'] = first_name
        
        last_name = prospect.get('lastName', '')
        if last_name:
            prospect_details['last_name'] = last_name

        emails = prospect.get('emails', [])
        if emails:
            for email in emails:
                status = email.get('status', None)
                if status == 'valid':
                    prospect_details['email'] = email.get('email', '')
                    break
        
        return prospect_details

    def _convert_from_url_data(self, data):
        if not data:
            return {}
        
        if type(data) == str:
            data = json.loads(data)
        
        prospect_details = {}
        if type(data) == list:
            for prospect in data:
                first_name = prospect.get('firstName', '')
                if first_name:
                    prospect_details['first_name'] = first_name
                
                last_name = prospect.get('lastName', '')
                if last_name:
                    prospect_details['last_name'] = last_name

                emails = prospect.get('emails', [])
                if emails:
                    for email in emails:
                        status = email.get('status', None)
                        if status == 'valid':
                            prospect_details['email'] = email.get('email', '')
                            break

                if first_name and last_name and email:
                    break
        else:
            prospect_details = self._extract_emails_from_data(data)
        
        data['prospect_details'] = prospect_details
        return data

    def api_get_url(self, url):
        api_url = self.api_url + '/get-emails-from-url'

        res = {
            'code' : -1
        }
        if not url:
            return res
        
        token = self.get_auth_token()
        
        headers = {
            'Authorization': 'Bearer ' + token
        }
        
        params = {
            'url': url
        }

        api_response = self._safe_request(api_url=api_url, params=params, post=True, headers=headers, form=True)
        if type(api_response) == str:
            res['message'] = api_response
            return res
        
        is_true = api_response.get('success', False)
        message = api_response.get('message', '')
        if not is_true:
            res['message'] = message
            res['code'] = self.PROVIDER_DATA_NOT_FOUND
            return res
        
        res['code'] = self.PROVIDER_DATA_FOUND
        res['data'] = self._convert_from_url_data(data=api_response.get('data', {}))
        return res
  

    def _convert_from_names_data(self, data):
        if not data:
            return {}
        
        prospect_details = {}
        first_name = data.get('firstName', '')
        if first_name:
            prospect_details['first_name'] = first_name
        
        last_name = data.get('lastName', '')
        if last_name:
            prospect_details['last_name'] = last_name

        emails = data.get('emails', [])
        if emails:
            for email in emails:
                status = email.get('emailStatus', None)
                if status == 'valid':
                    prospect_details['email'] = email.get('email', '')
                    break
        
        data['prospect_details'] = prospect_details
        return data


    def api_get_name(self, prospect_data):
        api_url = self.api_url + '/get-emails-from-names'

        res = {
            'code' : -1
        }
        
        token = self.get_auth_token()
        params = {
            'access_token' : token,
            'domain': prospect_data.get('company_url',''),
            'firstName': prospect_data.get('first_name',''),
            'lastName': prospect_data.get('last_name','')
        }

        api_response = self._safe_request(api_url=api_url, params=params, post=True)
        if type(api_response) == str:
            res['message'] = api_response
            return res

        status = api_response.get('status', None)
        if not status:
            res['code'] = self.PROVIDER_ACTION_FALSE
            return res
        
        identifier = status.get('identifier', None)
        if not identifier:
            res['code'] = self.PROVIDER_ACTION_FALSE
            return res
        
        if identifier == 'in_progress':
            res['code'] = self.PROVIDER_DELAY
        elif identifier == 'not_found':
            res['code'] = self.PROVIDER_DATA_NOT_FOUND
        elif identifier == 'complete':
            res['code'] = self.PROVIDER_DATA_FOUND
            res['data'] = self._convert_from_names_data(data=api_response.get('data', {}))

        return res

    def api_add_name(self, prospect_data):
        api_url = self.api_url + '/add-names-to-find-emails'

        res = {
            'code' : -1
        }
        
        token = self.get_auth_token()
        params = {
            'access_token' : token,
            'domain': prospect_data.get('company_url',''),
            'firstName': prospect_data.get('first_name',''),
            'lastName': prospect_data.get('last_name','')
        }

        api_response = self._safe_request(api_url=api_url, params=params, post=True)
        if type(api_response) == str:
            res['message'] = api_response
            return res

        sent = api_response.get('sent', None)
        if not sent:
            res['code'] = self.PROVIDER_ACTION_FALSE
        else:
            res['code'] = self.PROVIDER_IN_PROGRESS

        return res

    def _convert_from_domain_data(self, data):
        if not data:
            return {}
        
        prospect_details = {}
        emails = data.get('emails', [])
        for email in emails:
            first_name = email.get('firstName', '')
            if first_name:
                prospect_details['first_name'] = first_name

            last_name = email.get('lastName', '')
            if last_name:
                prospect_details['last_name'] = last_name

            email_found = email.get('email', '')
            if email_found:
                prospect_details['email'] = email_found


        data['prospect_details'] = prospect_details
        return data



    def api_get_domain(self, prospect_data, search_type='personal', limit=1, offset=0):
        api_url = self.api_url + '/get-domain-emails-with-info'

        res = {
            'code' : -1
        }
        
        token = self.get_auth_token()
        params = {
            'access_token' : token,
            'domain': prospect_data.get('company_url',''),
            'type' : search_type,
            'limit' : limit,
            'offset' : offset
        }

        api_response = self._safe_request(api_url=api_url, params=params, post=True)
        if type(api_response) == str:
            res['message'] = api_response
            return res

        result = api_response.get('result', None)
        if result is None:
            res['code'] = self.PROVIDER_ACTION_FALSE
        elif int(result) == 0:
            res['code'] = self.PROVIDER_DATA_NOT_FOUND
        elif int(result) > 0:
            res['code'] = self.PROVIDER_DATA_FOUND
            res['data'] = self._convert_from_domain_data(data=api_response)

        return res
