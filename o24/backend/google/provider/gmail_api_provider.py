from apiclient import errors
import base64
import email
from o24.backend import app
from o24.globals import *
from apiclient import errors
import base64
import email
from o24.backend.google.service.api import GoogleApiService
import o24.backend.google.provider.oauth_provider as oauth_provider
from o24.exceptions.exception_with_code import ErrorCodeException
from datetime import datetime

import traceback

class GmailApiProvider():
    def __init__(self, credentials, credentials_id=None):
        self.credentials_id = credentials_id
        self.credentials = credentials

        if credentials_id:
            self._refresh_credentials()    
        else:
            self._setup_credentials()
    
    def _setup_credentials(self):
        self.service = GoogleApiService.build_gmail_api_service(self.credentials)

    def _refresh_credentials(self):
        self.credentials = oauth_provider.GoogleOauthProvider.check_and_update_credentials(credentials_id=self.credentials_id)

        self.service = GoogleApiService.build_gmail_api_service(self.credentials)

    def _safe_execute(self, request):
        for i in range(2):
            try:
                return request.execute()
            except Exception as e:
                print(e)
                traceback.print_exc()

                if type(e) == errors.HttpError:
                    if (len(e.args) > 0):
                        code = e.args[0].get('status', -1)
                        
                        if i <= 0 and code == 401:
                            self._refresh_credentials()
                            continue
                        else:
                            raise ErrorCodeException(error_code=code, message=str(e))
                
                raise            

    def get_user_profile(self, user_id='me'):
        request = self.service.users().getProfile(userId=user_id) 
        response = self._safe_execute(request=request)
        return response

    def send_message(self, message, user_id='me'):
        request = self.service.users().messages().send(userId=user_id, body=message)

        message = self._safe_execute(request=request)

        return message

    def send_reply_to_thread(self, message, user_id='me'):
        request = self.service.users().messages().send(userId=user_id, body=message)

        response = self._safe_execute(request=request)

        return response



    def get_messages_meta(self, user_id, label_ids, sync_type, history_id=None):
        messages = []

        if sync_type == 'full':
            app.logger.debug('...........starting FULL get_messages_meta user_id:{0} label_ids:{1} sync_type:{2} history_id:{3}'.format(user_id,
                                                                                                                                        label_ids,
                                                                                                                                        sync_type,
                                                                                                                                        history_id))
            messages = self.list_messages_with_labels(user_id=user_id,
                                                    label_ids=label_ids)
        elif sync_type == 'partly':
            app.logger.debug('...........starting PARTLY get_messages_meta user_id:{0} label_ids:{1} sync_type:{2} history_id:{3}'.format(user_id,
                                                                                                                                        label_ids,
                                                                                                                                        sync_type,
                                                                                                                                        history_id))
            messages = self.list_messages_with_labels_history(user_id=user_id,
                                                    label_ids=label_ids,
                                                    history_id=history_id)
        else:
            app.logger.debug('............get_messages_meta strange sync_type:{0}'.format(sync_type))
            messages = []

        return messages
    
    def get_messages_data_full(self, user_id, msg_ids):
        
        messages = []
        for msg_id in msg_ids:
            message = self.get_message_data(msg_id=msg_id,
                                                user_id=user_id,
                                                format='full')
            if message:
                messages.append(message)
        
        return messages


    def get_user_email(self, user_id='me'):
        profile = self.get_user_profile(user_id=user_id)
        return profile['emailAddress']

    def list_labels(self, user_id='me'):
        request = self.service.users().labels().list(userId=user_id)
        
        response = self._safe_execute(request=request)

        return response['labels']
        
    def list_messages_with_labels_history(self, user_id, label_id, history_id, historyTypes="messageAdded"):
        if not label_id:
            app.logger.debug('.........list_messages_with_labels_history not possible for empty label_ids:{1} user_id:{0}'.format(user_id, label_ids))
            raise Exception("Can't list_messages_with_labels_history for empty label_ids")

        request = self.service.users().history().list(userId=user_id,
                                                labelId=label_id,
                                                startHistoryId=history_id,
                                                historyTypes=historyTypes)

        history = self._safe_execute(request=request)

        changes = history['history'] if 'history' in history else []
        while 'nextPageToken' in history:
            page_token = history['nextPageToken']
            request = self.service.users().history().list(userId=user_id,
                                                    labelId=label_id,
                                                    startHistoryId=history_id,
                                                    historyTypes=historyTypes,
                                                    pageToken=page_token)
            history = self._safe_execute(request=request)
            if 'history' in history:
                changes.extend(history['history'])
            else:
                break
                
        return changes

    def list_messages_with_labels(self, label_ids=[], user_id='me'):
        if not label_ids:
            app.logger.debug('.........list_messages_with_labels not possible for empty label_ids:{1} user_id:{0}'.format(user_id, label_ids))
            raise Exception("Can't list_messages_with_labels for empty label_ids")

        request = self.service.users().messages().list(userId=user_id,
                                                labelIds=label_ids)
        
        response = self._safe_execute(request=request)
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            request = self.service.users().messages().list(userId=user_id,
                                                        labelIds=label_ids,
                                                        pageToken=page_token)

            response = self._safe_execute(request=request)
            if 'messages' in response:
                messages.extend(response['messages'])
            else:
                break

        return messages


    def list_messages_matching_query(self, query='', user_id='me'):
        request = self.service.users().messages().list(userId=user_id,
                                                q=query)

        response = self._safe_execute(request=request)
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            request = self.service.users().messages().list(userId=user_id, q=query,
                                                pageToken=page_token)
            
            response = self._safe_execute(request=request)
            if 'messages' in response:
                messages.extend(response['messages'])
            else:
                break

        return messages


    def get_message_data(self, msg_id, user_id='me', format='metadata', metadataHeaders=[]):
        message = ''

        request = None
        if metadataHeaders:
            request = self.service.users().messages().get(userId=user_id, 
                                                    id=msg_id,
                                                    format=format,
                                                    metadataHeaders=metadataHeaders)

        else:
            request = self.service.users().messages().get(userId=user_id, 
                                                    id=msg_id,
                                                    format=format)

        return self._safe_execute(request=request)


    def get_mime_message(self, msg_id, user_id='me', format='full'):
            request = self.service.users().messages().get(userId=user_id, 
                                                        id=msg_id,
                                                        format=format)

            message = self._safe_execute(request=request)

            msg_str = base64.urlsafe_b64decode(message['raw']).decode()

            mime_msg = email.message_from_string(msg_str)

            return mime_msg

    def watch(self, user_id, request):
        request = self.service.users().watch(userId=user_id, 
                                                body=request)

        response = self._safe_execute(request=request)
        return response
  
    def stop_watch(self, user_id):
        request = self.service.users().stop(userId=user_id)
        
        response = self._safe_execute(request=request)
        return response

    def check_reply(self, email_from, after, user_id='me', anywhere=True):
        #example: from:support@hackernoon.com in:anywhere after:2020/05/24 
        #after: should be POSIX TIME, seconds since epoch

        query = "from:{0}".format(email_from)
        if anywhere:
            query = query + " in:anywhere"

        if after:
            after_query = " after:{0}".format(after)
            query = query + after_query

        print("*******")
        print(query)
        request = self.service.users().messages().list(userId=user_id,
                                                q=query)
        response = self._safe_execute(request=request)

        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        return messages


    def _convert_datetime_to_q(self, date):
        if type(date) != datetime:
            message = "gmail_api_provider: date is wrong type: {0}".format(type(date))
            raise Exception(message)

        res = str(date.year)
        res = res + '/' + str(date.month)
        res = res + '/' + str(date.day)

        return res