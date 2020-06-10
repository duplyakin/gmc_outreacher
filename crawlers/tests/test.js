const workers = require('./../linkedin/workers/workers.js');


const SEARCH_URL = "https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97";
const CONNECT_URL = "https://www.linkedin.com/in/bersheva/";
const MY_URL = "https://www.linkedin.com/in/grigoriy-polyanitsin/";

// test running

(async () => {
  console.log("..... test_db started: .....", __filename);

  let task_old = {
    input_data: {
      credentials_data: {
        email: "grinnbob@rambler.ru",
        password: "",
        li_at: "AQEDARcxwXEBb18zAAABcflw5z8AAAFyHX1rP00AVzV1p6dd9IpqrPbIfjq5ajRuaeHm8ZvSGYaQccRo1fX80kr0WHCDWLOvuPfz-uiAn-dw631pZyHV2ZdU66bPPX4J--EXfE0IxqwMYTi8bIiWfL8U"
      },
      campaign_data: {
        next_url: SEARCH_URL,
        page_count: 2,
      },
      template_data: {
        subject: '',
        body: 'Hi {first_name}, nice to meet you.',
      },
      prospect_data: {
        first_name: 'Olga',
        last_name: '',
        company_title: 'howtotoken.com',
        linkedin: CONNECT_URL,
      }
    },
    credentials_id: '507f1f77bcf86cd799439011',
  };

  //task = JSON.stringify(task);
  let task = "5ed54711ad1aa4da0718c61b";

  //await workers.loginWorker(task);
  //await workers.searchWorker(task);
  //await workers.connectWorker(task);
  await workers.messageWorker(task);
  //await workers.scribeWorker(task);
  //await workers.messageCheckWorker(task);
  //await workers.connectCheckWorker(task);
  //await workers.visitProfileWorker(task);

})();
