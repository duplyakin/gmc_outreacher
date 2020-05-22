$env:APP_ENV="Test"
SET APP_ENV=Test

#CREATE TEST DATABASE
python -m unittest discover -s .\o24\production_tests\ -p "*1_models.py"

#RUN ALL PRODUCTION TESTS
python -m unittest discover -s .\o24\production_tests\ -p "*2_scenaries.py"



#ONLY IF YOU NEED SEPARATE TESTS

#TEST Linkedin campaigns
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_0_check_linkedin_campaigns_handlers

#TEST Campaign handlers 
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_1_check_campaigns_handlers


#TEST admin handlers
python -m unittest o24.production_tests.test_prod_2_scenaries.ProdTestScenaries.test_2_check_admin_handlers