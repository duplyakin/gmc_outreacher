from mongoengine.fields import ReferenceField, ListField
import json

def template_key_dict(js_templates):
    res = {}

    email_templates = js_templates.get('email','')
    if email_templates:
        res['email'] = {}
        for template in email_templates:
            template_key = template.get('template_key')
            res['email'][template_key] = template
    
    linkedin_templates = js_templates.get('linkedin','')
    if linkedin_templates:
        res['linkedin'] = {}
        for template in linkedin_templates:
            template_key = template.get('template_key')
            res['linkedin'][template_key] = template

    return res


def to_json_deep_dereference(obj, restricted=['owner']):
    obj_dict = json.loads(obj.to_json())

    for key, val in obj._fields.items():
        if key in restricted:
            continue

        if isinstance(val, ReferenceField):
            if obj[key] == None:
                continue

            if key in obj_dict.keys():
                obj_dict[key] = json.loads(obj[key].to_json())
        if isinstance(val, ListField):
            if isinstance(val.field, ReferenceField):
                lst = []
                list_field = obj[key]
                for field in list_field:
                    lst.append(json.loads(field.to_json()))
                if lst:
                    obj_dict[key] = lst

    return obj_dict
