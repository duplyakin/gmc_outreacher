from apiclient import errors
import base64
import email
from o24.backend import app
from apiclient import errors
import base64
import email
from o24.backend.google.service.api import GoogleApiService

class GmailApiProvider():
    def __init__(self, credentials):
        self.service = GoogleApiService.build_gmail_api_service(credentials)

    def get_user_profile(self, user_id='me'):
        response = self.service.users().getProfile(userId=user_id).execute()
        return response

    def send_message(self, message, user_id='me'):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message)
               .execute())

            return message
        except errors.HttpError as error:
            print("An error occurred: {0}".format(error))



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
        response = self.service.users().labels().list(userId=user_id).execute()
        return response['labels']
        
    def list_messages_with_labels_history(self, user_id, label_id, history_id, historyTypes="messageAdded"):
        if not label_id:
            app.logger.debug('.........list_messages_with_labels_history not possible for empty label_ids:{1} user_id:{0}'.format(user_id, label_ids))
            raise Exception("Can't list_messages_with_labels_history for empty label_ids")

        history = self.service.users().history().list(userId=user_id,
                                                labelId=label_id,
                                                startHistoryId=history_id,
                                                historyTypes=historyTypes).execute()

        changes = history['history'] if 'history' in history else []
        while 'nextPageToken' in history:
            page_token = history['nextPageToken']
            history = self.service.users().history().list(userId=user_id,
                                                    labelId=label_id,
                                                    startHistoryId=history_id,
                                                    historyTypes=historyTypes,
                                                    pageToken=page_token).execute()
            if 'history' in history:
                changes.extend(history['history'])
            else:
                break
                
        return changes

    def list_messages_with_labels(self, label_ids=[], user_id='me'):
        if not label_ids:
            app.logger.debug('.........list_messages_with_labels not possible for empty label_ids:{1} user_id:{0}'.format(user_id, label_ids))
            raise Exception("Can't list_messages_with_labels for empty label_ids")

        response = self.service.users().messages().list(userId=user_id,
                                                labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId=user_id,
                                                        labelIds=label_ids,
                                                        pageToken=page_token).execute()
            if 'messages' in response:
                messages.extend(response['messages'])
            else:
                break

        return messages


    def list_messages_matching_query(self, query='', user_id='me'):
        response = self.service.users().messages().list(userId=user_id,
                                                q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId=user_id, q=query,
                                                pageToken=page_token).execute()
            if 'messages' in response:
                messages.extend(response['messages'])
            else:
                break

        return messages


    def get_message_data(self, msg_id, user_id='me', format='metadata', metadataHeaders=[]):
        message = ''
        if metadataHeaders:
            message = self.service.users().messages().get(userId=user_id, 
                                                    id=msg_id,
                                                    format=format,
                                                    metadataHeaders=metadataHeaders).execute()

        else:
            message = self.service.users().messages().get(userId=user_id, 
                                                    id=msg_id,
                                                    format=format).execute()

        return message


    def get_mime_message(self, msg_id, user_id='me', format='full'):
            message = self.service.users().messages().get(userId=user_id, 
                                                        id=msg_id,
                                                        format=format).execute()

            msg_str = base64.urlsafe_b64decode(message['raw']).decode()

            mime_msg = email.message_from_string(msg_str)

            return mime_msg

    def watch(self, user_id, request):
        response = self.service.users().watch(userId=user_id, 
                                                body=request).execute()
        return response
  
    def stop_watch(self, user_id):
        response = self.service.users().stop(userId=user_id).execute()
        return response
