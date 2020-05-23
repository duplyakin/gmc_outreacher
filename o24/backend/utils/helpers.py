from mongoengine.fields import ReferenceField, ListField
import json
import html2text

def convert_email_template_to_plain(template):
    body = template.get('body', None)
    if not body:
        return None
    
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.ignore_images = True
    converter.ignore_tables = True

    plain_template = template.copy()
    html_body = plain_template.get('body')
    
    plain_body = converter.handle(html_body)
    if not plain_body:
        raise Exception("Can't convert html to plain")
    
    plain_template['body'] = plain_body
    return plain_template

#return mapped_templates
def template_key_dict(js_templates, _validate=True):
    res = {}

    email_templates = js_templates.get('email','')
    if email_templates:
        res['email'] = {}
        plain = {}
        for template in email_templates:
            template_key = template.get('template_key')
            if template_key:
                res['email'][template_key] = template

                if _validate:
                    subject = template.get('subject', '')
                    if not subject:
                        message = "Email Subject can't be empty, template:{0}".format(template.get('title', template_key))
                        raise Exception(message)

                    body = template.get('body', '')
                    if not body:
                        message = "Email Body can't be empty, template:{0}".format(template.get('title', template_key))
                        raise Exception(message)


                html = convert_email_template_to_plain(template)
                if html is not None:
                    plain[template_key] = html

        res['plain'] = plain

    linkedin_templates = js_templates.get('linkedin','')
    if linkedin_templates:
        res['linkedin'] = {}
        for template in linkedin_templates:
            template_key = template.get('template_key')
            res['linkedin'][template_key] = template
            
            if _validate:
                linkedin_message = template.get('message', '')
                if not linkedin_message:
                    message = "Linkedin message can't be empty, template:{0}".format(template.get('title', template_key))
                    raise Exception(message)

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
