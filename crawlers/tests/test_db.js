const workers = require(__dirname + '/../linkedin/workers/workers.js');


const SEARCH_URL = "https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";
const MY_URL = "https://www.linkedin.com/in/grigoriy-polyanitsin/";

// test running

(async () => {
  console.log("..... test_db started: .....", __filename);

  let task = {
    input_data: {
      credentials_data: {
        email: "grinnbob@rambler.ru",
        password: "linked123",
      },
      campaign_data: {
        next_url: SEARCH_URL,
        page_count: 2,
      },
      template_data: {
        template: 'Hi {first_name}, nice to meet you. {first_name} 111 {first{first_name}_name} hi {ololo }',
      },
      prospect_data: {
        first_name: 'Justin',
        last_name: 'Shilov',
        company_title: 'howtotoken.com',
        linkedin: CONNECT_URL,
      }
    }
  };

  //await workers.loginWorker(task);
  await workers.searchWorker(task);
  //await workers.connectWorker(task);
  //await workers.messageWorker(task);
  //await workers.scribeWorkWorker(task);
  //await workers.messageCheckWorker(task);
  //await workers.connectCheckWorker(task);

})();
