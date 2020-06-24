$env:APP_ENV="Test"
SET APP_ENV=Test

#CREATE TEST DATABASE
python -m unittest discover test_data -s .\o24\production_tests\ -p "*1_models.py"


#RUN ALL PRODUCTION TESTS
python -m unittest discover -s .\o24\production_tests\ -p "*2_scenaries.py"

#CREATE PRODUCTION TEST DATA
python -m unittest discover -s .\o24\production_tests\ -p "*test_production_database.py"


#ONLY IF YOU NEED SEPARATE TESTS

#TEST Linkedin campaigns
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_0_check_linkedin_campaigns_handlers

#TEST Campaign handlers 
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_1_check_campaigns_handlers


#TEST admin handlers
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_2_check_admin_handlers



#TEST sequences
python -m unittest discover -s .\o24\production_tests\ -p "*3_carefull_real_sequence.py"

#TEST email handler
python -m unittest o24.production_tests.test_prod_3_carefull_real_sequence.RealSequenceTest.test_1_email_handlers


#TEST linkedin handler
python -m unittest o24.production_tests.test_prod_3_carefull_real_sequence.RealSequenceTest.test_1_linkedin_handlers



#TEST Google Oauth
python -m unittest o24.production_tests.test_prod_10_oauth.OauthTest.test_0_ack



#TEST PING PONG emails:
#from gmail to gsuite
python -m unittest o24.production_tests.test_PING_PONG_emails.PingPongEmailsTest.test_gmail_to_gsuite


python -m unittest o24.production_tests.test_PING_PONG_emails.PingPongEmailsTest.test_check_reply


#TEST Enrichment
python -m unittest o24.production_tests.test_prod_4_enrichment.EnricherTest.test_snovio_emit_enricher

python -m unittest o24.production_tests.test_prod_4_enrichment.EnricherTest.test_snovio_restart_prospect


#TEST Statistics:
python -m unittest o24.production_tests.test_stats.StatsTest.test_create_random_stats_data

python -m unittest o24.production_tests.test_stats.StatsTest.test_list_stats

python -m unittest o24.production_tests.test_stats.StatsTest.test_create_stats

python -m unittest o24.production_tests.test_stats.StatsTest.test_show_stats

python -m unittest o24.production_tests.test_stats.StatsTest.test_show_campaign_stats


python -m unittest o24.tests.test_lock.TestLock.test_lock