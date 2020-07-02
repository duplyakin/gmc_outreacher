export default
    {
            code: 1, 
            columns: [
                        {"label": "Prospects contacted", "field": "prospects_total"}, 
                        {"label": "Emails sent", "field": "email-send-message"}, 
                        {"label": "Emails replied", "field": "email-check-reply"}, 
                        {"label": "Emails opened", "field": "email_opens"}, 
                        {"label": "Emails enriched", "field": "emails-enriched-success"}, 
                        {"label": "Linkedin invites sent", "field": "linkedin-connect"}, 
                        {"label": "Linkedin profiles viewed", "field": "linkedin-visit-profile"}, 
                        {"label": "Linkedin messages sent", "field": "linkedin-send-message"}, 
                        {"label": "Linkedin replied", "field": "linkedin-check-reply"}, 
        
                        {"label": "Enrich credits left", "field": "credits-left"}
            ], 
            msg: 'Success', 
            statistics: [
                    {"_id": {"action_key": "linkedin-send-message", "month_day": "06-24"}, "total": 35}, 
                    {"_id": {"action_key": "linkedin-send-message", "month_day": "06-23"}, "total": 40}, 
                    {"_id": {"action_key": "linkedin-visit-profile", "month_day": "06-23"}, "total": 15}, 
                    {"_id": {"action_key": "linkedin-connect", "month_day": "06-23"}, "total": 3}, 
                    {"_id": {"action_key": "email-send-message", "month_day": "06-23"}, "total": 4}, 
                    {"_id": {"month_day": "06-24", "action_key": "prospects_total"}, "total": 79}, 
                    {"_id": "credits-left", "total": 999}
            ]
    }
