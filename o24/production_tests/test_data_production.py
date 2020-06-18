from o24.globals import *

USERS = [
    {'email' : '1@email.com',
     'password' : 'password1',
     'role' : 'admin',
     'invited_by' : 'test_invite',
     'invite_code' : 'test_invite',
     'enrich_credits' : 1000,
     'active' : True,
     'credentials' : [
         {
         'data' : { 'sender' : 'special-medium'},
         'medium' : 'special-medium'
         }
     ]
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
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_VISIT_PROFILE_ACTION
    },
    {
        'action_type' : 0,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_CONNECT_ACTION
    },
    {
        'action_type' : 0,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_SEND_MESSAGE_ACTION
    },
    {
        'action_type' : 2,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_CHECK_ACCEPT_ACTION
    },
    {
        'action_type' : 2,
        'data' : {},
        'medium' : 'linkedin',
        'key' : LINKEDIN_CHECK_REPLY_ACTION
    },    
    {
        'action_type' : 0,
        'data' : {},
        'medium' : 'email',
        'key' : EMAIL_SEND_MESSAGE_ACTION
    },
    {
        'action_type' : 2,
        'data' : {},
        'medium' : 'email',
        'key' : EMAIL_CHECK_REPLY_ACTION
    },
    {
        'action_type' : 2,
        'data' : {},
        'medium' : 'special-medium',
        'key' : EMAIL_ENRICH
    },
    {
        'action_type' : 2,
        'data' : {},
        'medium' : 'special-medium',
        'key' : EMAIL_CHECK_ENRICHED
    },
    {
        'action_type' : 1,
        'data' : {},
        'medium' : 'special-medium',
        'key' : DELAY_ACTION
    },
    {
        'action_type' : 4,
        'data' : {},
        'medium' : 'special-medium',
        'key' : FINISHED_ACTION
    },
    {
        'action_type' : 5,
        'data' : {},
        'medium' : 'special-medium',
        'key' : SUCCESS_ACTION
    }
]

FUNNELS = [
    #NEVER SHOWED ON FRONTEND
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
    #NEVER SHOWED ON FRONTEND
    {
        'root' : {
            'key' : LINKEDIN_PARSE_PROFILE_ACTION,
            'funnel_type' : LINKEDIN_ENRICHMENT_FUNNEL_TYPE,
            'templates_required' : {'dummy' : 1},
            'title' : 'Linkedin parse profile funnel',
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
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'title' : 'Linkedin only sequence',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'root' : True,
            'if_true' : 'visit-delay-1',
            'if_false' : 'visit-delay-1',
            'templates_required' : {
                'linkedin' : {
                    'intro_linkedin' : {
                        'title' : 'Connection request message (up to 299 symbols)',
                        'template_key' : 'intro_linkedin',
                        'order' : 0
                    },
                    'linkedin_followup_1' : {
                        'title' : 'The 1st Linkedin followup message',
                        'template_key' : 'linkedin_followup_1',
                        'order' : 1
                    },
                    'linkedin_followup_2' : {
                        'title' : 'The 2nd Linkedin followup message',
                        'template_key' : 'linkedin_followup_2',
                        'order' : 2
                    },
                    'linkedin_followup_3' : {
                        'title' : 'The 3rd Linkedin followup message',
                        'template_key' : 'linkedin_followup_3',
                        'order' : 3
                    }
                }
            },
        },
                'visit-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-connect-1',
                    'if_false' : 'linkedin-connect-1'
                },

        'linkedin-connect-1' : {
            'key' : LINKEDIN_CONNECT_ACTION,
            'template_key' : 'intro_linkedin',
            'if_true' : 'connect-delay-1',
            'if_false' : 'connect-delay-1'
        },

                'connect-delay-1' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'after_connect_sent',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-check-accept-1',
                    'if_false' : 'linkedin-check-accept-1'
                },
        'linkedin-check-accept-1' : {
            'key' : LINKEDIN_CHECK_ACCEPT_ACTION,
            'if_true' : 'linkedin-accepted',
            'if_false' : 'linkedin-accept-denied'
        },

        'linkedin-accept-denied' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'if_true' : 'delay-3',
            'if_false' : 'delay-3',
        },
                'delay-3' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-check-accept-2',
                    'if_false' : 'linkedin-check-accept-2'
                },

        'linkedin-check-accept-2' : {
            'key' : LINKEDIN_CHECK_ACCEPT_ACTION,
            'if_true' : 'linkedin-accepted',
            'if_false' : FINISHED_ACTION
        },

        'linkedin-accepted' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'template_key' : 'linkedin_followup_1',
            'if_true' : 'delay-4',
            'if_false' : 'delay-4',
        },
                'delay-4' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-visit-before-followup-2',
                    'if_false' : 'ln-visit-before-followup-2'
                },
        'ln-visit-before-followup-2' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION,
            'if_true' : 'delay-5',
            'if_false' : 'delay-5',
        },
                'delay-5' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'linkedin_followup_2',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-check-before-followup-2',
                    'if_false' : 'ln-check-before-followup-2'
                },
        'ln-check-before-followup-2' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'ln-followup-2'       
        },
        'ln-followup-2' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'template_key' : 'linkedin_followup_2',
            'if_true' : 'delay-6',
            'if_false' : 'delay-6',
        },
                'delay-6' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'linkedin_followup_3',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-visit-before-followup-3',
                    'if_false' : 'ln-visit-before-followup-3'
                },
        'ln-visit-before-followup-3' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION,
            'if_true' : 'ln-check-before-followup-3',
            'if_false' : 'ln-check-before-followup-3',
        },
        'ln-check-before-followup-3' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'ln-followup-3'       
        },
        'ln-followup-3' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'template_key' : 'linkedin_followup_3',
            'if_true' : 'delay-7',
            'if_false' : 'delay-7',
        },
                'delay-7' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-last-check',
                    'if_false' : 'ln-last-check'
                },
        'ln-last-check' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : FINISHED_ACTION       
        },

        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        },
        SUCCESS_ACTION : {
            'key' : SUCCESS_ACTION
        }
    },


  {
        'root' : {
            'key' : EMAIL_ENRICH,
            'title' : 'Email only sequence',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'root' : True,
            'if_true' : 'email-send-intro',
            'if_false' : 'visit-delay-1',
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                    'email_followup_1' : {
                        'title' : 'The 1st followup email',
                        'template_key' : 'email_followup_1',
                        'order' : 1
                    },
                    'email_followup_2': {
                        'title' : 'The 2nd followup email',
                        'template_key' : 'email_followup_2',
                        'order' : 2
                    },
                    'email_followup_3': {
                        'title' : 'The 3rd followup email',
                        'template_key' : 'email_followup_3',
                        'order' : 2
                    }
                }
            },
        },
                'visit-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 20000 },
                    'if_true' : 'has-email',
                    'if_false' : 'has-email'
                },
        'has-email' : {
            'key' : EMAIL_CHECK_ENRICHED,
            'if_true' : 'email-send-intro',
            'if_false' : FINISHED_ACTION 

        },
        'email-send-intro' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'intro_email',
            'if_true' : 'delay-before',
            'if_false' : 'delay-before' 
        },
        'delay-before' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_1',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'email-check-before-followup-1',
                    'if_false' : 'email-check-before-followup-1'
        },
        'email-check-before-followup-1' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-1' 
        },
        'email-followup-1' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_1',
            'if_true' : 'email-delay-1',
            'if_false' : 'email-delay-1' 
        },
                'email-delay-1' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_2',
                    'data' : {'delay' : 80000},
                    'if_true' : 'email-check-before-followup-2',
                    'if_false' : 'email-check-before-followup-2'    
                },
        'email-check-before-followup-2' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-2' 
        },

        'email-followup-2' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_2',
            'if_true' : 'email-delay-3',
            'if_false' : 'email-delay-3' 
        },
                'email-delay-3' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_3',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'email-check-before-followup-3',
                    'if_false' : 'email-check-before-followup-3'    
                },

        'email-check-before-followup-3' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-3' 
        },

        'email-followup-3' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_3',
            'if_true' : 'email-check-last-reply',
            'if_false' : 'email-check-last-reply' 
        },
        
        'email-check-last-reply' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : FINISHED_ACTION
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        },
        SUCCESS_ACTION : {
            'key' : SUCCESS_ACTION
        }
    },



  {
        'root' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'title' : 'Linedin + Email simple sequence',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'root' : True,
            'if_true' : 'visit-delay-1',
            'if_false' : 'visit-delay-1',
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                    'email_followup_1' : {
                        'title' : 'The 1st followup email',
                        'template_key' : 'email_followup_1',
                        'order' : 1
                    },
                    'email_followup_2': {
                        'title' : 'The 2nd followup email',
                        'template_key' : 'email_followup_2',
                        'order' : 2
                    }
                },
                'linkedin' : {
                    'intro_linkedin' : {
                        'title' : 'Connection request message (up to 299 symbols)',
                        'template_key' : 'intro_linkedin',
                        'order' : 0
                    }
                }
            },
        },
                'visit-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-connect-1',
                    'if_false' : 'linkedin-connect-1'
                },

        'linkedin-connect-1' : {
            'key' : LINKEDIN_CONNECT_ACTION,
            'template_key' : 'intro_linkedin',
            'if_true' : 'connect-delay-1',
            'if_false' : 'connect-delay-1'
        },

                'connect-delay-1' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'after_connect_sent',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-check-accept-1',
                    'if_false' : 'linkedin-check-accept-1'
                },
        'linkedin-check-accept-1' : {
            'key' : LINKEDIN_CHECK_ACCEPT_ACTION,
            'if_true' : 'is-email',
            'if_false' : 'is-email'
        },
        'is-email' : {
            'key' : EMAIL_ENRICH,
            'if_true' : 'email-1',
            'if_false' : 'delay-before'
        },
        'delay-before' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 20000 },
                    'if_true' : 'has-email',
                    'if_false' : 'has-email'
        },
        'has-email' : {
            'key' : EMAIL_CHECK_ENRICHED,
            'if_true' : 'email-1',
            'if_false' : FINISHED_ACTION
        },
        'email-1' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'intro_email',
            'if_true' : 'email-delay-1',
            'if_false' : 'email-delay-1'
        },
                'email-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'profile-view-2',
                    'if_false' : 'profile-view-2'   
                },
        'profile-view-2' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'if_true' : 'email-delay-2',
            'if_false' : 'email-delay-2',
        },
                'email-delay-2' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_1',
                    'data' : { 'delay' : 8000 },
                    'if_true' : 'email-check-before-followup-1',
                    'if_false' : 'email-check-before-followup-1'   
                },
        'email-check-before-followup-1' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-1' 
        },
        'email-followup-1' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_1',
            'if_true' : 'email-delay-3',
            'if_false' : 'email-delay-3' 
        },
                'email-delay-3' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_2',
                    'data' : {'delay' : 80000},
                    'if_true' : 'email-check-before-followup-2',
                    'if_false' : 'email-check-before-followup-2'    
                },
        'email-check-before-followup-2' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-2' 
        },

        'email-followup-2' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_2',
            'if_true' : 'email-delay-4',
            'if_false' : 'email-delay-4' 
        },
                'email-delay-4' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'email-check-last-reply',
                    'if_false' : 'email-check-last-reply'    
                },
        
        'email-check-last-reply' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : FINISHED_ACTION
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        },
        SUCCESS_ACTION : {
            'key' : SUCCESS_ACTION
        }
    },


    {
        'root' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'title' : 'Linedin + Email sequence',
            'funnel_type' : GENERAL_FUNNEL_TYPE,
            'root' : True,
            'if_true' : 'visit-delay-1',
            'if_false' : 'visit-delay-1',
            'templates_required' : {
                'email' : {
                    'intro_email' : {
                        'title' : 'Intro email',
                        'template_key' : 'intro_email',
                        'order' : 0
                    },
                    'email_followup_1' : {
                        'title' : 'The 1st followup email',
                        'template_key' : 'email_followup_1',
                        'order' : 1
                    },
                    'email_followup_2': {
                        'title' : 'The 2nd followup email',
                        'template_key' : 'email_followup_2',
                        'order' : 2
                    }
                },
                'linkedin' : {
                    'intro_linkedin' : {
                        'title' : 'Connection request message (up to 299 symbols)',
                        'template_key' : 'intro_linkedin',
                        'order' : 0
                    },
                    'linkedin_followup_1' : {
                        'title' : 'The 1st Linkedin followup message',
                        'template_key' : 'linkedin_followup_1',
                        'order' : 1
                    },
                    'linkedin_followup_2' : {
                        'title' : 'The 2nd Linkedin followup message',
                        'template_key' : 'linkedin_followup_2',
                        'order' : 2
                    }
                }
            },
        },
                'visit-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-connect-1',
                    'if_false' : 'linkedin-connect-1'
                },

        'linkedin-connect-1' : {
            'key' : LINKEDIN_CONNECT_ACTION,
            'template_key' : 'intro_linkedin',
            'if_true' : 'connect-delay-1',
            'if_false' : 'connect-delay-1'
        },

                'connect-delay-1' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'after_connect_sent',
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'linkedin-check-accept-1',
                    'if_false' : 'linkedin-check-accept-1'
                },
        'linkedin-check-accept-1' : {
            'key' : LINKEDIN_CHECK_ACCEPT_ACTION,
            'if_true' : 'connect-approve-1',
            'if_false' : 'connect-deny-1'
        },

        # EMAIL sending branch
        'connect-deny-1' : {
            'key' : EMAIL_ENRICH,
            'if_true' : 'send-intro',
            'if_false' : 'delay-before'
        },
        'delay-before' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 20000 },
                    'if_true' : 'has-email',
                    'if_false' : 'has-email'
        },
        'has-email' : {
            'key' : EMAIL_CHECK_ENRICHED,
            'if_true' : 'send-intro',
            'if_false' : FINISHED_ACTION
        },
        'send-intro' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'intro_email',
            'if_true' : 'email-delay-1',
            'if_false' : 'email-delay-1'
        },
                'email-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'profile-view-2',
                    'if_false' : 'profile-view-2'   
                },
        'profile-view-2' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'if_true' : 'email-delay-2',
            'if_false' : 'email-delay-2',
        },
                'email-delay-2' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_1',
                    'data' : { 'delay' : 8000 },
                    'if_true' : 'email-check-before-followup-1',
                    'if_false' : 'email-check-before-followup-1'   
                },
        'email-check-before-followup-1' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-1' 
        },
        'email-followup-1' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_1',
            'if_true' : 'email-delay-3',
            'if_false' : 'email-delay-3' 
        },
                'email-delay-3' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'email_followup_2',
                    'data' : {'delay' : 80000},
                    'if_true' : 'email-check-before-followup-2',
                    'if_false' : 'email-check-before-followup-2'    
                },
        'email-check-before-followup-2' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'email-followup-2' 
        },

        'email-followup-2' : {
            'key' : EMAIL_SEND_MESSAGE_ACTION,
            'template_key' : 'email_followup_2',
            'if_true' : 'email-delay-4',
            'if_false' : 'email-delay-4' 
        },
                'email-delay-4' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 3600 },
                    'if_true' : 'email-check-last-reply',
                    'if_false' : 'email-check-last-reply'    
                },
        
        # Linkedin sending branch
        'connect-approve-1' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'ln-followup-1'       
        },
        
        'ln-followup-1' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'template_key' : 'linkedin_followup_1',
            'if_true' : 'ln-delay-1',
            'if_false' : 'ln-delay-1'
        },
                'ln-delay-1' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-profile-view',
                    'if_false' : 'ln-profile-view'    
                },
        'ln-profile-view' : {
            'key' : LINKEDIN_VISIT_PROFILE_ACTION ,
            'if_true' : 'ln-delay-2',
            'if_false' : 'ln-delay-2',
        },
                'ln-delay-2' : {
                    'key' : DELAY_ACTION,
                    'template_key' : 'linkedin_followup_2',
                    'data' : { 'delay' : 8000 },
                    'if_true' : 'check-before-followup-2',
                    'if_false' : 'check-before-followup-2'    
                },

        'check-before-followup-2' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'ln-followup-2'       
        },

        'ln-followup-2' : {
            'key' : LINKEDIN_SEND_MESSAGE_ACTION,
            'template_key' : 'linkedin_followup_2',
            'if_true' : 'ln-delay-3',
            'if_false' : 'ln-delay-3'
        },
                'ln-delay-3' : {
                    'key' : DELAY_ACTION,
                    'data' : { 'delay' : 80000 },
                    'if_true' : 'ln-check-reply-1',
                    'if_false' : 'ln-check-reply-1'    
                },
        'ln-check-reply-1' : {
            'key' : LINKEDIN_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : 'connect-deny-1'       
        },

        'email-check-last-reply' : {
            'key' : EMAIL_CHECK_REPLY_ACTION,
            'if_true' : SUCCESS_ACTION,
            'if_false' : FINISHED_ACTION
        },
        FINISHED_ACTION : {
            'key' : FINISHED_ACTION
        },
        SUCCESS_ACTION : {
            'key' : SUCCESS_ACTION
        }
    }
]

CAMPAIGNS = []

LISTS = []

PROSPECTS = []

TEAMS = []

TEST_CREDENTIALS = {}


GOOGLE_APP_SETTINGS = [{
    'title': 'Outreacher24 - web app credentials - development local',
    'credentials': {"web":{"client_id":"606646624276-qcedt5p3vdad7h6aie2l5s75mg59at7t.apps.googleusercontent.com","project_id":"outreacher24","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"Gn-M_96r8PTML9SQaLxAqqWD","redirect_uris":["http://127.0.0.1:5000/oauth/callback"],"javascript_origins":["http://127.0.0.1:5000"]}},
    'redirect_uri': 'http://127.0.0.1:5000/oauth/callback',

    'gmail_scopes': ['https://mail.google.com/'],
    'gmail_access_type': 'offline',
    'gmail_include_granted_scopes': 'false',

    'gmail_api_name': 'gmail',
    'gmail_api_version': 'v1',

    'active' : True
}]


GOOGLE_APP_SETTINGS_PRODUCTION = [{
    'title': 'Outreacher24 - web app credentials - PRODUCTION',
    'credentials': {"web":{"client_id":"606646624276-k7p37f77u8rp2np03hd8up7p6amshpl2.apps.googleusercontent.com","project_id":"outreacher24","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"9YrijbGJA8J0YZCA9HDzckMx","redirect_uris":["https://outreacher24.com/oauth/callback"],"javascript_origins":["https://outreacher24.com"]}},
    'redirect_uri': 'https://outreacher24.com/oauth/callback',

    'gmail_scopes': ['https://mail.google.com/'],
    'gmail_access_type': 'offline',
    'gmail_include_granted_scopes': 'false',

    'gmail_api_name': 'gmail',
    'gmail_api_version': 'v1',

    'active' : True
}]



