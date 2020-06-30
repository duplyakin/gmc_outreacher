import json
from o24.backend.utils.helpers import template_key_dict
from bson.objectid import ObjectId

class JSObject():
    ATTR_PREFIX = '_js_'
    RAW_ATTR_PREFIX = '_raw_'
    
    STR_FIELDS = ['title', 'gmail_include_granted_scopes', 'active']

    def __init__(self, raw_data):
        try:
            self.raw_data = raw_data

            self.data_dict = json.loads(raw_data)
            if not self.data_dict:
                raise Exception("JS Data can't be empty")

            for key, value in self.data_dict.items():
                if value:
                    attr_name = self.ATTR_PREFIX + key
                    attr_name_raw = self.RAW_ATTR_PREFIX + key

                    des_value = value

                    #trying to parse json
                    if key not in self.STR_FIELDS and isinstance(des_value, str):
                        try:
                            des_value = json.loads(value)
                        except:
                            des_value = value
                    
                    setattr(self, attr_name_raw, des_value)
                    if isinstance(des_value, list):
                        # is that a dict of objectIDs - check first ellement
                        if len(des_value) > 0:
                            el_0 = des_value[0]
                            if isinstance(el_0, dict) and el_0.get('_id', None):
                                lst = []
                                for v in des_value:
                                    get_id = v['_id']['$oid']
                                    if not get_id:
                                        raise Exception("Id can't be empty for field:{0}".format(key))

                                    o_id = ObjectId(get_id)
                                    lst.append(o_id)
                                setattr(self, attr_name, lst)
                            else:
                                setattr(self, attr_name, des_value)
                        else:
                            setattr(self, attr_name, des_value)
                    elif isinstance(des_value, dict):
                        if des_value.get('_id', None):
                            get_id = des_value['_id']['$oid']
                            if not get_id:
                                raise Exception("Id can't be empty for field:{0}".format(key))
                            
                            o_id = ObjectId(get_id)
                            setattr(self, attr_name, o_id)
                        else:
                            setattr(self, attr_name, des_value)
                    else:
                        setattr(self, attr_name, des_value)

        except Exception as e:
            error_message = "Data serialization error: {0}".format(str(e))
            raise Exception(error_message)


    def _custom_attr(self, attr, default=None, raw=False):
        attr_name = self.ATTR_PREFIX + attr
        if raw:
            attr_name = self.RAW_ATTR_PREFIX + attr

        if not hasattr(self, attr_name):
            return default

        val = getattr(self, attr_name)
        if val is None:
            return default

        return val

    def get_field(self, field, default=None):
        return self._custom_attr(attr=field, default=default)

class JSCredentialsData(JSObject):
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def get_type(self):
        return self._custom_attr(attr='credentials_type', default='Unknown')

    def get_data(self):
        return self._custom_attr(attr='data', default={})

    def get_medium(self):
        return self._custom_attr(attr='medium', default=None)

    def get_limit_per_day(self):
        return self._custom_attr(attr='limit_per_day', default=None)
    
    def get_modification(self):
        return self._custom_attr(attr='modification', default=None)

    def __str__(self):
        return str(self.__dict__)

class JSUserData(JSObject):
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def get_email(self):
        return self._custom_attr(attr='email', default=None)

    def get_password(self):
        return self._custom_attr(attr='password', default=None)
    
    def get_repeat_password(self):
        return self._custom_attr(attr='repeat_password', default=None)

    def get_invite_code(self):
        return self._custom_attr(attr='invite_code', default='')


class JSProspectData(JSObject):
    def __init__(self, raw_data):
        super().__init__(raw_data)

    def assign_to_list(self):
        return self._custom_attr(attr='assign_to_list', default=None)

    def data(self):
        return self._custom_attr(attr='data', default={})

class JSGoogleAppSettingsData(JSObject):
    def __init__(self, raw_data):
        super().__init__(raw_data)

class JSLimitsData(JSObject):
    def __init__(self, raw_data):
        super().__init__(raw_data)

class JSCampaignData(JSObject):
    def __init__(self, raw_data):
        try:
            self.raw_data = raw_data

            self.data_dict = json.loads(raw_data)
            if not self.data_dict:
                raise Exception("Campaign Data can't be empty")
            
            for key, value in self.data_dict.items():
                if value:
                    attr_name = self.ATTR_PREFIX + key
                    attr_name_raw = self.RAW_ATTR_PREFIX + key

                    des_value = value

                    #trying to parse json
                    if key not in self.STR_FIELDS and isinstance(des_value, str):
                        try:
                            des_value = json.loads(value)
                        except:
                            des_value = value
                        
                    if key == 'title':
                        setattr(self, attr_name, des_value)
                        continue
                    elif key == 'templates':                               
                        templates = des_value
                        mapped_templates = template_key_dict(templates)
                        if not mapped_templates:
                            raise Exception("Wrong templates format")

                        templates = mapped_templates
                        setattr(self, attr_name, templates)
                        #print("...Serialized key:{0} value:{1}".format(attr_name, templates))
                    elif key == 'from_hour':
                        hour, minutes = des_value.split(':')

                        from_minutes = self.ATTR_PREFIX + 'from_minutes'
                        setattr(self, attr_name, int(hour))
                        #print("...Serialized key:{0} value:{1}".format(attr_name, hour))
                        setattr(self, from_minutes, int(minutes))
                        #print("...Serialized key:{0} value:{1}".format(from_minutes, minutes))
                    elif key == 'to_hour':
                        hour, minutes = des_value.split(':')

                        to_minutes = self.ATTR_PREFIX + 'to_minutes'
                        setattr(self, attr_name, int(hour))
                        #print("...Serialized key:{0} value:{1}".format(attr_name, hour))
                        setattr(self, to_minutes, int(minutes))
                        #print("...Serialized key:{0} value:{1}".format(to_minutes, minutes))
                    else:                        
                        setattr(self, attr_name_raw, des_value)
                        if isinstance(des_value, list):
                            # is that a dict of objectIDs
                            if len(des_value) > 0:
                                el_0 = des_value[0]
                                if isinstance(el_0, dict) and el_0.get('_id', None):
                                    lst = []
                                    for v in des_value:
                                        get_id = v['_id']['$oid']
                                        if not get_id:
                                            raise Exception("Id can't be empty for field:{0}".format(key))

                                        o_id = ObjectId(get_id)
                                        lst.append(o_id)
                                    setattr(self, attr_name, lst)
                                else:
                                    setattr(self, attr_name, des_value)
                            else:
                                setattr(self, attr_name, des_value)
                        
                        elif isinstance(des_value, dict):
                            if des_value.get('_id', None):
                                get_id = des_value['_id']['$oid']
                                if not get_id:
                                    raise Exception("Id can't be empty for field:{0}".format(key))
                                
                                o_id = ObjectId(get_id)
                                setattr(self, attr_name, o_id)
                                #print("...Serialized key:{0} value:{1}".format(attr_name, get_id))
                            else:
                                setattr(self, attr_name, des_value)
                        else:
                            setattr(self, attr_name, des_value)
                            #print("...Serialized key:{0} value:{1}".format(attr_name, value))



        except Exception as e:
            error_message = "Campaign Data serialization error: {0}".format(str(e))
            raise Exception(error_message)
    
    def title(self):
        return self._custom_attr(attr='title', default='')
    
    def funnel(self):
        return self._custom_attr(attr='funnel', default=None)

    def credentials(self):
        return self._custom_attr(attr='credentials', default=[])

    def prospects_list(self):
        return self._custom_attr(attr='list_selected', default=None)

    def templates(self):
        return self._custom_attr(attr='templates', default={})

    def custom_delays(self):
        return self._custom_attr(attr='custom_delays', default={})

    def sending_days(self):
        return self._custom_attr(attr='sending_days', default={})

    def from_hour(self):
        return self._custom_attr(attr='from_hour', default=0)

    def from_minutes(self):
        return self._custom_attr(attr='from_minutes', default=0)

    def to_hour(self):
        return self._custom_attr(attr='to_hour', default=0)

    def to_minutes(self):
        return self._custom_attr(attr='to_minutes', default=0)

    def time_zone(self):
        return self._custom_attr(attr='time_zone', default='')

    def campaign_type(self):
        return self._custom_attr(attr='campaign_type', default=None)

    def get_list_title(self):
        return self._custom_attr(attr='list_title', default='')

    def __str__(self):
        return str(self.__dict__)

