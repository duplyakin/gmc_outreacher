USERS = [
    {'email' : '1@email.com',
     'password' : 'password1',
     'invited_by' : 'test_invite',
     'invite_code' : 'test_invite',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp', 'account' : 'ks.shilov@gmail.com'},
         'medium' : 'email'
         },
        {
         'data' : { 'sender' : 'api', 'account' : 'ks.shilov@howtotoken.com'},
         'medium' : 'email'
         },
         {
         'data' : { 'sender' : 'linkedin', 'account' : 'linkedin.com/ksshilov', 'password' : 'linkedin1-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '2@email.com',
     'password' : 'password2',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
        {
         'data' : { 'sender' : 'api'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin2-email', 'password' : 'linkedin2-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]
    },
    {'email' : '3@email.com',
     'password' : 'password3',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin3-email', 'password' : 'linkedin3-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
     ]

    },
    {'email' : '4@email.com',
     'password' : 'password4',
     'active' : True,
      'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin4-email', 'password' : 'linkedin4-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    
    {'email' : '5@email.com',
     'password' : 'password5',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin5-email', 'password' : 'linkedin5-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '6@email.com',
     'password' : 'password6',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin6-email', 'password' : 'linkedin6-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '7@email.com',
     'password' : 'password7',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin7-email', 'password' : 'linkedin7-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '8@email.com',
     'password' : 'password8',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin8-email', 'password' : 'linkedin8-password'},
         'medium' : 'linkedin'
         },
   {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]
    },
    {'email' : '9@email.com',
     'password' : 'password9',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin9-email', 'password' : 'linkedin9-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },
      ]

    },
    {'email' : '10@email.com',
     'password' : 'password10',
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'smtp'},
         'medium' : 'email'
         },
         {
         'data' : { 'email' : 'linkedin10-email', 'password' : 'linkedin10-password'},
         'medium' : 'linkedin'
         },
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         },         
      ]

    },
    {
        'email' : '11@email.com',
        'password' : 'password11',
        'active' : True,
        'credentials' : []
    }
]

TEAMS = [
    {
        'admin' : '3@email.com',
        'title' : 'team1-3@email.com',
        'members' : ['4@email.com', '5@email.com', '6@email.com']
    },
    {
        'admin' : '7@email.com',
        'title' : 'team2-7@email.com',
        'members' : ['8@email.com', '9@email.com', '10@email.com']
    }
]

# 0 - Actions with limit
# 1 - Delays
# 2 - Sync Events
# 3 - Async Events
# 4 - FINISHED
# 5 - SUCCESS
ACTIONS = [
    {
        'action_type' : 0,
        'data' : {
            'what' : 'parse-linkedin'
        },
        'medium' : 'linkedin',
        'key' : 'parse-linkedin'
    },

    {
        'action_type' : 0,
        'data' : {
            'what' : 'visit-profile'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-visit-profile'
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'connect'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-connect'
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-send-message'
    },
    

    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'email',
        'key' : 'email-send-message'
    },


    {
        'action_type' : 1,
        'data' : {
            'what' : 'delay'
        },
        'medium' : 'special-medium',
        'key' : 'delay-linkedin'
    },

     {
        'action_type' : 1,
        'data' : {
            'what' : 'delay'
        },
        'medium' : 'special-medium',
        'key' : 'delay-email'
    },

    {
        'action_type' : 4,
        'data' : {
            'what' : 'FINISHED'
        },
        'medium' : 'special-medium',
        'key' : 'finished'
    },
    
    {
        'action_type' : 5,
        'data' : {
            'what' : 'SUCCESS'
        },
        'medium' : 'special-medium',
        'key' : 'success'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-accept'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-check-accept'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'linkedin',
        'key' : 'linkedin-check-reply'
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'email',
        'key' : 'email-check-reply'
    }
]

FUNNELS = [
    {
        'root' : {
            'key' : 'parse-linkedin',
            'title' : 'Parse linkedin funnel',
            'root' : True,
            'templates_required' : {
                'search_url' : True
            },
            'if_true' : 'success',
            'if_false' : 'finished',
        },

        'finished' : {
            'key' : 'finished'
        },

        'success' : {
            'key' : 'success'
        }
    },

    {
        'root' : {
            'key' : 'email-send-message',
            'title' : 'Email only 4 emails sequence',
            'template_key' : 'intro_email',
            'root' : True,
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                    'email_followup_1' : {
                        'title' : 'Follow up email - 1',
                        'template_key' : 'email_followup_1',
                        'order' : 1
                    },
                    'email_followup_2': {
                        'title' : 'Follow up email - 2',
                        'template_key' : 'email_followup_2',
                        'order' : 2
                    },
                    'email_followup_3': {
                        'title' : 'Follow up email - 3',
                        'template_key' : 'email_followup_3',
                        'order' : 3
                    },

                }
            },
            'if_true' : 'wait-email-intro',
            'if_false' : 'wait-email-intro',
        },

        'wait-email-intro' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'check-reply-intro',
            'if_false' : 'check-reply-intro'
        },

        'check-reply-intro' : {
            'key' : 'email-check-reply',
            'if_true' : 'success',
            'if_false' : 'email-followup-1'
        },

        'email-followup-1' :  {
            'key' : 'email-send-message',
            'template_key' : 'email_followup_1',
            'if_true' : 'wait-followup-1',
            'if_false' : 'wait-followup-1'
        },

        'wait-followup-1' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'check-reply-followup-1',
            'if_false' : 'check-reply-followup-1'
        },

        'check-reply-followup-1' : {
                'key' : 'email-check-reply',
                'if_true' : 'success',
                'if_false' : 'email-followup-2'
        },

        'email-followup-2' :  {
            'key' : 'email-send-message',
            'template_key' : 'email_followup_2',
            'if_true' : 'wait-followup-2',
            'if_false' : 'wait-followup-2'
        },

        'wait-followup-2' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'check-reply-followup-2',
            'if_false' : 'check-reply-followup-2'
        },

        'check-reply-followup-2' : {
                'key' : 'email-check-reply',
                'if_true' : 'success',
                'if_false' : 'email-followup-3'
        },

        'email-followup-3' :  {
            'key' : 'email-send-message',
            'template_key' : 'email_followup_3',
            'if_true' : 'wait-followup-3',
            'if_false' : 'wait-followup-3'
        },

        'wait-followup-3' : {
            'key' : 'delay-email',
            'data' : { 'delay' : 10},
            'if_true' : 'check-reply-followup-3',
            'if_false' : 'check-reply-followup-3'
        },

        'check-reply-followup-3' : {
                'key' : 'email-check-reply',
                'if_true' : 'success',
                'if_false' : 'finished'
        },

        'finished' : {
            'key' : 'finished'
        },

        'success' : {
            'key' : 'success'
        }

    },

    {
        'root' : {
            'key' : 'linkedin-connect',
            'title' : 'Linkedin + email funnel',
            'root' : True,
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                    'email_followup_1' : {
                        'title' : 'Follow up email - 1',
                        'template_key' : 'email_followup_1',
                        'order' : 1
                    },
                    'email_followup_2': {
                        'title' : 'Follow up email - 2',
                        'template_key' : 'email_followup_2',
                        'order' : 2
                    }
                },
                'linkedin' : {
                    'intro_linkedin' : {
                        'title' : 'Intro linkedin message',
                        'template_key' : 'intro_linkedin',
                        'order' : 0
                    },
                    'linkedin_followup_1' : {
                        'title' : 'Follow up linkedin - 1',
                        'template_key' : 'linkedin_followup_1',
                        'order' : 1
                    }
                }
            },
            'if_true' : 'wait-1',
            'if_false' : 'wait-1',
        },

        'wait-1' : {
            'key' : 'delay-linkedin',
            'data' : { 'delay' : 10},
            'if_true' : 'check-connect-1',
            'if_false' : 'check-connect-1'
        },

        'check-connect-1' : {
            'key' : 'linkedin-check-accept',
            'if_true' : 'connect-approve-1',
            'if_false' : 'connect-deny-1'
        },

                'connect-approve-1' : {
                    'key' : 'linkedin-send-message',
                    'template_key' : 'intro_linkedin',
                    'if_true' : 'wait-2',
                    'if_false' : 'wait-2'
                },

                'wait-2' : {
                    'key' : 'delay-linkedin',
                    'data' : { 'delay' : 10},
                    'if_true': 'check-reply-1',
                    'if_false': 'check-reply-1'
                },

                'check-reply-1' : {
                    'key' : 'linkedin-check-reply',
                    'if_true' : 'success',
                    'if_false' : 'linkedin-send-followup-1'
                },

                'linkedin-send-followup-1' : {
                    'key' : 'linkedin-send-message',
                    'template_key' : 'linkedin_followup_1',
                    'if_true' : 'wait-linkedin-followup-1',
                    'if_false' : 'wait-linkedin-followup-1'
                },

                'wait-linkedin-followup-1' : {
                    'key' : 'delay-linkedin',
                    'data' : { 'delay' : 10},
                    'if_true': 'check-reply-followup-1',
                    'if_false': 'check-reply-followup-1'
                },
                'check-reply-followup-1' : {
                    'key' : 'linkedin-check-reply',
                    'if_true' : 'success',
                    'if_false' : 'connect-deny-1'
                },

        'connect-deny-1' : {
            'key' : 'email-send-message',
            'template_key' : 'intro_email',
            'if_true' : 'wait-22',
            'if_false' : 'wait-22'
        },

                'wait-22' : {
                    'key' : 'delay-email',
                    'data' : { 'delay' : 10},
                    'if_true' : 'check-reply-intro',
                    'if_false' : 'check-reply-intro'
                },

                'check-reply-intro' : {
                    'key' : 'email-check-reply',
                    'if_true' : 'success',
                    'if_false' : 'email-followup-1'
                },

                'email-followup-1' :  {
                    'key' : 'email-send-message',
                    'template_key' : 'email_followup_1',
                    'if_true' : 'wait-3',
                    'if_false' : 'wait-3'
                },

                'wait-3' : {
                    'key' : 'delay-email',
                    'data' : { 'delay' : 10},
                    'if_true' : 'check-reply-followup-1',
                    'if_false' : 'check-reply-followup-1'
                },

                    'check-reply-followup-1' : {
                        'key' : 'email-check-reply',
                        'if_true' : 'success',
                        'if_false' : 'email-followup-2'
                },

                'email-followup-2' :  {
                    'key' : 'email-send-message',
                    'template_key' : 'email_followup_2',

                    'if_true' : 'wait-4',
                    'if_false' : 'wait-4'
                },

                'wait-4' : {
                    'key' : 'delay-email',
                    'data' : { 'delay' : 10},
                    'if_true' : 'check-reply-followup-2',
                    'if_false' : 'check-reply-followup-2'
                },

                'check-reply-followup-2' : {
                        'key' : 'email-check-reply',
                        'if_true' : 'success',
                        'if_false' : 'finished'
                },

        'finished' : {
            'key' : 'finished'
        },

        'success' : {
            'key' : 'success'
        }

    }
]

CAMPAIGNS = [
    {
        'title' : 'campaign-1',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    },

    {
        'title' : 'campaign-11',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    },
    {
        'title' : 'campaign-111',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    },
    {
        'title' : 'campaign-2',
        'owner' : '3@email.com',
        'medium' : ['linkedin', 'email', 'special-medium']
    }   
]

LISTS = [
    {
        'owner' : '1@email.com',
        'title' : 'List-1 1@email.com'
    },
    {
        'owner' : '1@email.com',
        'title' : 'List-2 1@email.com'
    },
    {
        'owner' : '1@email.com',
        'title' : 'List-3 1@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-1 3@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-2 3@email.com'
    },
    {
        'owner' : '3@email.com',
        'title' : 'List-3 3@email.com'
    },
]

PROSPECTS = [
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-1',
        'email_name' : 'ksshilov',
        'email_domain' : '@yandex.ru',
        'assign_to_list' : 'List-1 1@email.com'
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-11',
        'email_name' : 'ks.shilov',
        'email_domain' : '@gmail.ru',
        'assign_to_list' : 'List-2 1@email.com',
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-111',
        'email_name' : 'ks_shilov',
        'email_domain' : '@gmail.com',
    },
    {
        'owner' : '3@email.com',
        'amount' : 10,
        'assign_to' : 'campaign-2',
        'email_name' : 'yana.shilov',
        'email_domain' : '@gmail.ru',
    }
]



GOOGLE_APP_SETTINGS = [{
    'title': 'Outreacher24 - web app credentials - development local',
    'credentials': {"web":{"client_id":"606646624276-qcedt5p3vdad7h6aie2l5s75mg59at7t.apps.googleusercontent.com","project_id":"outreacher24","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Gn-M_96r8PTML9SQaLxAqqWD","redirect_uris":["http://127.0.0.1:5000/oauth/callback"],"javascript_origins":["http://127.0.0.1:5000"]}},
    'redirect_uri': 'http://127.0.0.1:5000/oauth/callback',

    'gmail_scopes': ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.metadata'],
    'gmail_access_type': 'offline',
    'gmail_include_granted_scopes': 'true',

    'gmail_api_name': 'gmail',
    'gmail_api_version': 'v1',

    'active' : True
}]
