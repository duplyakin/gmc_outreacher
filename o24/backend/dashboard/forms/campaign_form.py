import o24.backend.models as models

class CampaignForm():
    FORM_NAME = 'campaign_form'
    def __init__(self, form_session):
        self.form_session = form_session

    @classmethod
    def get_form(cls, user_id):
        form_session = models.FormSession.objects(owner=user_id, 
                                            form_name=cls.FORM_NAME).first()
        if not form_session:
            form_session = models.FormSession(owner=user_id,
                                        form_name=cls.FORM_NAME)
            form_session._commit(_reload=True)


        form = cls(form_session=form_session)
        return form

    def init_form(self):
        form_data = {
            'current_step' : 'step1',
            'step1' : {
                'action' : 'next',
                'next_step' : 'step2'
            }
        }
        
        self.form_session.data = form_data
        self._commit(_reload=True)
        return form_data

    def next_step(self):
        current_step = self.form_session.data.get('current_step', None)
        if not current_step:
            raise Exception("Wrong step")
        
        return self.form_session.data.get(current_step)
        
    def save_step(self, step, data):
        validate = getattr(self, '_validate_' + str(step))
        if not validate:
            raise Exception("No such step {0}".format(step))

        return validate(data=data)
        
    def _validate_step1(data):
        current_step = 'step1'
        self.form_session.data['current_step'] = current_step
        
        self.form_session.data[current_step] = {
            'action' : 'next',
            'next_step' : 'step2',
            'data' : data
        }
        
        self._commit(_reload=True)

    def _validate_step2(data):
        current_step = 'step2'

        self.form_session.data['current_step'] = current_step
        self.form_session.data[current_step] = {
            'action' : 'next',
            'next_step' : 'step3',
            'data' : data
        }
        
        self._commit(_reload=True)

    def _validate_step3(data):
        current_step = 'step3'

        self.form_session.data['current_step'] = current_step
        self.form_session.data[current_step] = {
            'action' : 'finish',
            'data' : data
        }
        
        self._commit(_reload=True)

    def submit_campaign(self, campaign):
        pass

    def _commit(self, _reload=False):
        self.form_session._commit(_reload=_reload)