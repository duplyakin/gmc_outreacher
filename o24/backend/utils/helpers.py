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
