from o24.globals import *

USERS = [
    {'email' : '1@email.com',
     'password' : 'password1',
     'role' : 'admin',
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

TEST_CREDENTIALS = {
    'test_email_handlers' : {
        'owner' : '1@email.com',
        'title' : 'test_email_handlers',
        'medium' : 'email',
        'data' : {
               "email" : "ks.shilov@gmail.com",
                "account" : "ks.shilov@gmail.com",
                "credentials" : {
                        "token" : "ya29.a0AfH6SMCeBPkFvS4bb2zH8rCylKsEsiAhz3DuZZ_p5A9qP7MmMTrb2ck2gwqjEqb_RMi7Ww6VQ5wZczeZ2rzHpL1-0DRTq3AJ_5w9w_6EMwhUM0vErMpBw1voV1ypZ-an7j6U1Yb3emtdWTvTKWNSN3v4htzcrPuXO6Nt",
                        "refresh_token" : "null",
                        "token_uri" : "https://oauth2.googleapis.com/token",
                        "client_id" : "606646624276-qcedt5p3vdad7h6aie2l5s75mg59at7t.apps.googleusercontent.com",
                        "client_secret" : "Gn-M_96r8PTML9SQaLxAqqWD",
                        "scopes" : [
                                "https://mail.google.com/",
                                "https://www.googleapis.com/auth/gmail.send",
                                "https://www.googleapis.com/auth/gmail.modify",
                                "https://www.googleapis.com/auth/gmail.metadata"
                        ]
                },
                "sender" : "smtp"
        }
    },
    'test_linkedin_handlers' : {
        'owner' : '1@email.com',
        'title' : 'test_linkedin_handlers',
        'medium' : 'linkedin',
        'data' : {
            'email' : 'grinnbob@rambler.ru',
            'password' : 'linked123'
        }
    }
}

# 0 - Actions with limit
# 1 - Delays
# 2 - Sync Events
# 3 - Async Events
# 4 - FINISHED
# 5 - SUCCESS
ACTIONS = [
    {
        'action_type' : 0,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_SEARCH_ACTION 
    },
    {
        'action_type' : 0,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_PARSE_PROFILE_ACTION 
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'visit-profile'
        },
        'medium' : 'linkedin',
        'key' : LINKEDIN_VISIT_PROFILE_ACTION
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'connect'
        },
        'medium' : 'linkedin',
        'key' : LINKEDIN_CONNECT_ACTION
    },
    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'linkedin',
        'key' : LINKEDIN_SEND_MESSAGE_ACTION
    },
   {
        'action_type' : 2,
        'data' : {
            'what' : 'check-accept'
        },
        'medium' : 'linkedin',
        'key' : LINKEDIN_CHECK_ACCEPT_ACTION
    },

    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'linkedin',
        'key' : LINKEDIN_CHECK_REPLY_ACTION
    },    

    {
        'action_type' : 0,
        'data' : {
            'what' : 'send-message'
        },
        'medium' : 'email',
        'key' : EMAIL_SEND_MESSAGE_ACTION
    },
    {
        'action_type' : 2,
        'data' : {
            'what' : 'check-reply'
        },
        'medium' : 'email',
        'key' : EMAIL_CHECK_REPLY_ACTION
    },

    {
        'action_type' : 1,
        'data' : {
            'what' : 'delay'
        },
        'medium' : 'special-medium',
        'key' : DELAY_ACTION
    },
    {
        'action_type' : 4,
        'data' : {
            'what' : 'FINISHED'
        },
        'medium' : 'special-medium',
        'key' : FINISHED_ACTION
    },
    {
        'action_type' : 5,
        'data' : {
            'what' : 'SUCCESS'
        },
        'medium' : 'special-medium',
        'key' : SUCCESS_ACTION
    }
]

FUNNELS = [
    {
        'root' : {
            'key' : LINKEDIN_SEARCH_ACTION,
            'funnel_type' : LINKEDIN_PARSING_FUNNEL_TYPE,
            'title' : 'Linkedin Parsing Funnel',
            'templates_required' : {'dummy' : 1},
            'root' : True,
            'if_true' : FINISHED_ACTION,
            'if_false' : FINISHED_ACTION,
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        }
    },
    {
        'root' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'title' : 'test_email_handler_funnel',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'template_key' : 'intro_email',
            'root' : True,
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                }
            },
            'if_true' : FINISHED_ACTION,
            'if_false' : FINISHED_ACTION,
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        } 
    },


    {
        'root' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'title' : 'test_linkedin_handler_funnel',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'template_key' : 'intro_linkedin',
            'root' : True,
            'templates_required' : {
                'linkedin' : {
                    'intro_linkedin' : {
                        'title' : 'Intro linkedin message',
                        'template_key' : 'intro_linkedin',
                        'order' : 0
                    }
                }
            },
            'if_true' : 'step1',
            'if_false' : 'step1',
        },
        'step1' :  {
            'key' : 'linkedin-check-reply',
            'if_true' : 'step2',
            'if_false' : 'step2'
        },

        'step2' : {
            'key' : 'linkedin-check-accept',
            'if_true' : 'step3',
            'if_false' : 'step3'
 
        },

        'step3' : {
            'key' : 'linkedin-connect',
            'if_true' : 'step4',
            'if_false' : 'step4'
        },

        'step4' : {
            'key' : 'linkedin-parse-profile',
            'if_true' : FINISHED_ACTION,
            'if_false' : FINISHED_ACTION

        },

        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        }
    },



    {
        'root' : {
            'key' : LINKEDIN_PARSE_PROFILE_ACTION,
            'funnel_type' : LINKEDIN_ENRICHMENT_FUNNEL_TYPE,
            'templates_required' : {'dummy' : 1},
            'title' : 'Linkedin enrichment funnel',
            'root' : True,
            'if_true' : FINISHED_ACTION,
            'if_false' : FINISHED_ACTION,
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        }
    },

    {
        'root' : {
            'key' : 'email-send-message',
            'title' : 'Email only 4 emails sequence',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
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
            'key' : DELAY_ACTION,
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
            'key' : DELAY_ACTION,
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
            'key' : DELAY_ACTION,
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
            'key' : DELAY_ACTION,
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
            'funnel_type' : GENERAL_FUNNEL_TYPE,
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
            'key' : DELAY_ACTION,
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
                    'key' : DELAY_ACTION,
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
                    'key' : DELAY_ACTION,
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
                    'key' : DELAY_ACTION,
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
                    'key' : DELAY_ACTION,
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
                    'key' : DELAY_ACTION,
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
        'title' : 'test_email_handler_campaign',
        'owner' : '1@email.com',
        'funnel' : 'test_email_handler_funnel',
        'credentials' : 'test_email_handlers'
    },
    {
        'title' : 'test_linkedin_handler_campaign',
        'owner' : '1@email.com',
        'funnel' : 'test_linkedin_handler_funnel',
        'credentials' : 'test_linkedin_handlers'
    },

    {
        'title' : 'real_test',
        'owner' : '1@email.com',
        'medium' : ['linkedin', 'email', 'special-medium'],
        'funnel' : 'Linkedin + email funnel'
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
        'title' : 'real_test_list'
    },
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
        'owner' : '1@email.com',
        'title' : 'assign_to_none_1'
    },
    {
        'owner' : '1@email.com',
        'title' : 'assign_to_none_2'
    },
    {
        'owner' : '1@email.com',
        'title' : 'assign_to_none_3'
    },
    {
        'owner' : '1@email.com',
        'title' : 'assign_to_none_4'
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

    #### REAL DATA
    {
        'owner' : '1@email.com',
        'assign_to' : 'test_email_handler_campaign',
        'data' : {
            'email' : 'ks.shilov+1@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/kirill-shilov-25aa8630/',
            'first_name' : 'Kirill',
            'company' : 'Outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'test_linkedin_handler_campaign',
        'data' : {
            'test_action' : LINKEDIN_SEND_MESSAGE_ACTION,
            'email' : 'ks.shilov+3@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/kirill-shilov-25aa8630/',
            'first_name' : 'Kirill',
            'company' : 'outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },

    {
        'owner' : '1@email.com',
        'assign_to' : 'test_linkedin_handler_campaign',
        'data' : {
            'test_action' : 'linkedin-connect',
            'email' : 'ks.shilov+3@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/barry-magennis-768a0a1aa/',
            'first_name' : 'Barry',
            'company' : 'Boostlabs',
            'url' : 'Boostlabs.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'test_linkedin_handler_campaign',
        'data' : {
            'test_action' : 'linkedin-check-accept',
            'email' : 'ks.shilov+3@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/barry-magennis-768a0a1aa/',
            'first_name' : 'Barry',
            'company' : 'Boostlabs',
            'url' : 'Boostlabs.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'test_linkedin_handler_campaign',
        'data' : {
            'test_action' : 'linkedin-check-reply',
            'email' : 'ks.shilov+3@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/kirill-shilov-25aa8630/',
            'first_name' : 'Kirill',
            'company' : 'outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },

    {
        'owner' : '1@email.com',
        'assign_to' : 'test_linkedin_handler_campaign',
        'data' : {
            'test_action' : 'linkedin-parse-profile',
            'linkedin' : 'https://www.linkedin.com/in/barry-magennis-768a0a1aa/',
        },
        'assign_to_list' : 'real_test_list'
    },


    {
        'owner' : '1@email.com',
        'assign_to' : 'real_test',
        'data' : {
            'email' : '2400394@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/alexander-savinkin-3ba99614/',
            'first_name' : 'Alexander',
            'company' : 'outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'real_test',
        'data' : {
            'email' : 'grinnbob@rambler.ru',
            'linkedin' : 'https://www.linkedin.com/in/grigoriy-polyanitsin/',
            'first_name' : 'Grigory',
            'company' : 'outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'real_test',
        'data' : {
            'email' : 'grifon12358@gmail.com',
            'linkedin' : 'https://www.linkedin.com/in/grigoriy-polyanitsin/',
            'first_name' : 'Grigory',
            'last_name' : 'Pol',
            'company' : 'outreacher24',
            'url' : 'outreacher24.com'
        },
        'assign_to_list' : 'real_test_list'
    },
    {
        'owner' : '1@email.com',
        'assign_to' : 'real_test',
        'data' : {
            'email' : 'Clients@boostlabs.co.uk',
            'linkedin' : 'https://www.linkedin.com/in/barry-magennis-768a0a1aa/',
            'first_name' : 'Barry',
            'company' : 'Boostlabs',
            'url' : 'boostlabs.co.uk'
        }
    },
    #### END OF REAL DATA

    
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
        'email_name' : 'kss.shilov',
        'email_domain' : '@gmail.ru',
        'assign_to_list' : 'assign_to_none_1',
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'email_name' : 'ksss.shilov',
        'email_domain' : '@gmail.ru',
        'assign_to_list' : 'assign_to_none_2',
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'email_name' : 'kssss.shilov',
        'email_domain' : '@gmail.ru',
        'assign_to_list' : 'assign_to_none_3',
    },
    {
        'owner' : '1@email.com',
        'amount' : 10,
        'email_name' : 'ksssss.shilov',
        'email_domain' : '@gmail.ru',
        'assign_to_list' : 'assign_to_none_4',
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




########################################################################
########################################################################
###################### REQUESTS TO HANDLERS ############################
########################################################################

CAMPAIGN_LINKEDIN_PARSING_CREATE = {
    'title': 'Linkedin parse test campaign - XX-{0}',
    'list_title' : 'Linkedin parse test list title - XX-{0}',
    'data' : {
        'search_url': 'https://linkedin/com?search=&dsfsdf',
        'total_pages': 100,
        'interval_pages': 10,
    },
    'credentials': [],
    'from_hour': '10:00',
    'to_hour': '21:00',
    'time_zone': {
        'label': "(GMT+00:00) United Kingdom Time",
        'value': "Europe/London",
        'offset': 0
    },
    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": False,
        "6": False
    }
}


CAMPAIGN_LINKEDIN_EDIT = {
    'title': 'EDIT - Linkedin parse test campaign - XX-{0}',
    'data' : {
        'search_url': 'https://linkedin/com?search=&dsfsdf-new_one-{0}',
        'total_pages': 103,
        'interval_pages': 14,
    },
    'from_hour': '00:00',
    'to_hour': '21:45',
    'time_zone': {
        'label': "(GMT+07:00) Western Indonesia Time - Pontianak",
        'value': "Asia/Pontianak",
        'offset': 420
    },
    'sending_days': {
        "0": False,
        "1": False,
        "2": False,
        "3": True,
        "4": True,
        "5": True,
        "6": False
    }
}


CAMPAIGN_LINKEDIN_ENRICHMENT_CREATE = {
    'title': 'Linkedin enrichment test campaign - XX-{0}',
    'list_selected' : {},
    'credentials': [],
    'from_hour': '10:00',
    'to_hour': '21:00',
    'time_zone': {
        'label': "(GMT+00:00) United Kingdom Time",
        'value': "Europe/London",
        'offset': 0
    },
    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": False,
        "6": False
    }
}


ADMIN_GOOGLE_SETTINGS_CREATE = {
    'title': 'Create test settings XX-{0}',
    'credentials': '{"web":{"client_id":"606646624276-qcedt5p3vdad7h6aie2l5s75mg59at7t.apps.googleusercontent.com","project_id":"outreacher24","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Gn-M_96r8PTML9SQaLxAqqWD","redirect_uris":["http://127.0.0.1:5000/oauth/callback"],"javascript_origins":["http://127.0.0.1:5000"]}}',
    'redirect_uri': 'http://127.0.0.1:5000/oauth/callback',
    'gmail_scopes': '["https://mail.google.com/", "https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/gmail.metadata"]',
    'gmail_access_type': "offline",
    'gmail_include_granted_scopes': 'true',
    'gmail_api_name': "gmail",
    'gmail_api_version': "v1",
    'active' : "0"
}

ADMIN_GOOGLE_SETTINGS_EDIT = {
    'title': 'Edited Create test settings XX-{0}',
    'credentials': '{"web":{"client_id":"adsfadsfasdfasdfgoogleusercontent.com","project_id":"outreacher24","auth_uri":"https://google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Gn-M_96r8PTML9SQaLxAqqWD","redirect_uris":["http://127.0.0.1:5000/oauth/callback"],"javascript_origins":["http://outreacher24.com"]}}',
    'redirect_uri': 'http://127.0.0.1:5000/oauth',
    'gmail_scopes': '["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/gmail.metadata"]',
    'gmail_access_type': "offline",
    'gmail_include_granted_scopes': 'true',
    'gmail_api_name': "spreadsheet",
    'gmail_api_version': "v2",
    'active' : "1"
}


ADMIN_CREDENTIALS_EDIT = {
    'status' : '-1', 
    'error_message' : "Random error text", 
    'medium' : 'my-test-medium', 
    'next_action' : "2021-05-22T10:1:2.475Z",
    'limit_per_day' : "1000", 
    'limit_per_hour' : "2000", 
    'limit_interval' : "22020202",
    'current_daily_counter' : "123", 
    'current_hourly_counter' : "123"
}

CAMPAIGNS_CREATE = {
    'list_selected': {},
    'title': "Create test campaign XX-{0}",
    'funnel': {},
    'credentials': [],
    'templates': {
        'email': [
            {
                'title' : 'Intro email',
                'template_key' : 'intro_email',
                'order' : 0,
                'subject' : 'Some subject',
                'body' : 'Some body on create'
            },
            {
                'title' : 'Follow up email - 1',
                'template_key' : 'email_followup_1',
                'order' : 1,
                'subject': 'Hello this is me',
                'body' : '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
Hi {first_name}<br /><br />My name is Kirill - I'm a blockchain developer and writer. Since early 2017 I’ve worked hard to become the top blockchain contributor for Hacker Noon - you can check my signature for published topics and my Linkedin and Hacker Noon profiles.<br /><br />With my team, 2020 marks the launch of a new global blockchain PR project - and I’d love <strong>if {{url}} would join us.</strong> <br /><br />During 2020 I will ask blockchain founders for their predictions on the blockchain industry - 2 questions per month, 24 total (you can participate once, or each time, your choice). <br /><br />All answers will be published as a Roundup topic on Hacker Noon and other top-tier crypto publications. At the end of 2020, those answers that were the closest with their predictions to the actual situation will be featured on the main page of Hacker Noon.<br /><br />Also, there is a weekly format where we will explain your project’s key news and distribute it throughout many major channels: 4M+ Hacker Noon website + 40K newsletter and Cryptopanic’s 400K trader community.<br /><br /><br /><span style="color: #e74c3c;"><strong>March 2020 - PR opportunities:</strong></span><br />1. <strong>Hackernoon.com Roundup</strong> - “<span style="color: #e74c3c;">Which top 3 industries will dominate blockchain tech utilization by the end of 2020, why?</span>“<br />      * Deadline for sending a <span style="text-decoration: underline;"><span style="color: #e74c3c; text-decoration: underline;">quote - March 16</span></span>.<br />      * Managing <span style="color: #e74c3c;">fee: $220</span> <br /><br />2. <strong>Hackernoon.com Weekly Matter</strong> - Weekly news published on the front page of Hackernoon where our team will explain your project’s news and tell the audience why it matters to your industry. <br />       * Deadline for sending your news — <span style="text-decoration: underline;"><span style="color: #e74c3c; text-decoration: underline;">each week by Thursday</span></span> (the nearest: March 5, then March 12)<br />       * Managing <span style="color: #e74c3c;">fee: $250</span><br /><br />3. <strong>AmbCrypto.com Roundup article</strong> - “How can blockchain improve online businesses in 2020? (Tell us about your niche)”<br />       * Deadline for sending your <span style="text-decoration: underline;"><span style="color: #e74c3c; text-decoration: underline;">quote - March 23</span></span><br />       * Managing <span style="color: #e74c3c;">fee: $190</span><br /><br />If you participate in 2 or more formats there will be a 20% discount.<br /><br />If you are interested in one or both of these formats and need to know the statistics of the previous sessions, just let me know and I’ll send them your way.<br /><br />P.S.<br />If you’re not interested, just let me know.<br />For faster communication we could chat on <span style="color: #e74c3c;">telegram: ksshilov</span><br /><br /><br />Thanks,<br />Kirill Shilov,<br />Hackernoon.com contributor (https://hackernoon.com/@ks.shilov)<br />Telegram: @ksshilov<br />Linkedin: https://www.linkedin.com/in/kirill-shilov-25aa8630/
</body>
</html>
'''
            },
            {
                'title' : 'Follow up email - 2',
                'template_key' : 'email_followup_2',
                'order' : 2,
                'subject' : 'Some subject - 2',
                'body' : 'Some body on create - 2'
            },
        ],
        'linkedin': [
            {
                'title' : 'Intro linkedin message',
                'template_key' : 'intro_linkedin',
                'order' : 0,
                'message' : 'Some linkedin message'
            },
            {
                'title' : 'Follow up linkedin - 1',
                'template_key' : 'linkedin_followup_1',
                'order' : 1,
                'message' : 'Some linkedin message - 2'
            }
        ]
    },
    'from_hour': "10:23",
    'to_hour': "21:00",
    'time_zone': {
        'label': "(GMT+00:00) United Kingdom Time",
        'value': "Europe/London",
        'offset': 0
    },

    'sending_days': {
        "0": True,
        "1": True,
        "2": True,
        "3": True,
        "4": True,
        "5": False,
        "6": False
    }
}


CAMPAIGNS_EDIT = {
    'title': "EDIT Create test campaign XX-{0}",
    'templates': {
        'email': [
            {
                'title' : 'Intro email',
                'template_key' : 'intro_email',
                'order' : 0,
                'subject' : 'Some subject on Edit',
                'body' : 'Some body on Edit'
            },
            {
                'title' : 'Follow up email - 1',
                'template_key' : 'email_followup_1',
                'order' : 1,
                'subject': 'Hello {first_name} this is me',
                'body' : '''
<!DOCTYPE html>
<html>
<head>
</head>
<body>
Hi {first_name}<br /><br />If you are interested in participating in our PR project, you’re in luck! We still have time.<br /><br /><br /><span style="color: #e74c3c; font-size: 16px;"><strong>Here are the upcoming events:</strong></span><br />1. <strong>Hackernoon.com Roundup</strong> - “<span style="color: #e74c3c;">Which top 3 industries will dominate blockchain tech utilization by the end of 2020, why?</span>“<br />      * Deadline for sending a <span style="text-decoration: underline;"><span style="color: #e74c3c; text-decoration: underline;">quote - March 16</span></span>.<br />      * Managing <span style="color: #e74c3c;">fee: $220 </span><br /><br />2. <strong>Hackernoon.com Weekly Matter</strong> - Weekly news published on the front page of Hackernoon where our team will explain your project’s news and tell the audience why it matters to your industry. <br />       * Deadline for sending your news — <span style="color: #e74c3c;">each week by Thursday</span> (the nearest: March 5, then March 12)<br />       * Managing <span style="color: #e74c3c;">fee: $250</span><br /><br />3. <strong>AmbCrypto.com Roundup article</strong> - “<span style="color: #e74c3c;">How can blockchain improve online businesses in 2020? (Tell us about your niche)</span>”<br />       * Deadline for sending your <span style="color: #e74c3c;">quote - March 23</span><br />       * Managing <span style="color: #e74c3c;">fee: $190</span><br /><br />If you participate in 2 or more formats there will be a 20% discount.<br /><br />If you’d like to participate just let me know and I’ll be in touch.<br /><br />P.S.<br />For faster communication we could chat on <span style="color: #e74c3c;">telegram: ksshilov</span><br /><br /><br />Thanks,<br />Kirill Shilov,<br />Hackernoon.com contributor (https://hackernoon.com/@ks.shilov)<br />Telegram: @ksshilov<br />Linkedin: https://www.linkedin.com/in/kirill-shilov-25aa8630/
</body>
</html>
'''
            },
            {
                'title' : 'Follow up email - 2',
                'template_key' : 'email_followup_2',
                'order' : 2,
                'subject' : 'Some subject on Edit - 2',
                'body' : 'Some body on Edit - 2'
            },
        ],
        'linkedin': [
            {
                'title' : 'Intro linkedin message',
                'template_key' : 'intro_linkedin',
                'order' : 0,
                'message' : 'Linkedin message on Edit'
            },
            {
                'title' : 'Follow up linkedin - 1',
                'template_key' : 'linkedin_followup_1',
                'order' : 1,
                'message' : 'Linkedin message on Edit - 2'
            }
        ]
    },
    'from_hour': "00:00",
    'to_hour': "18:01",
    'time_zone': {
        'label': "(GMT+07:00) Western Indonesia Time - Pontianak",
        'value': "Asia/Pontianak",
        'offset': 420
    },
    'sending_days': {
        "0": False,
        "1": False,
        "2": True,
        "3": False,
        "4": True,
        "5": True,
        "6": False
    }
}