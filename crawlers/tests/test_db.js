const workers = require(__dirname + '/../linkedin/workers/workers.js');


const SEARCH_URL = "https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";
const MY_URL = "https://www.linkedin.com/in/grigoriy-polyanitsin/";

// test running

(async () => {
  console.log("..... test_db started: .....", __filename);

  let task_0 = {
    email: "grinnbob@rambler.ru",
    password: "linked123",
    url: SEARCH_URL,
    pageNum: 6,
    data: {
      first_name: 'Justin',
      last_name: 'Shilov',
      company_name: 'howtotoken.com'
    },
    template: 'Hi {first_name}, nice to meet you. {first_name} 111 {first{first_name}_name} hi {ololo }',
    connectName: 'Kirill Shilov',
  };

  let task = {
    input_data: {
      credentials: {
        email: "grinnbob@rambler.ru",
        password: "linked123",
      },
      data: {
        url: SEARCH_URL,
        pageNum: 6,
        template_data: {
          first_name: 'Justin',
          last_name: 'Shilov',
          company_name: 'howtotoken.com'
        },
        template: 'Hi {first_name}, nice to meet you. {first_name} 111 {first{first_name}_name} hi {ololo }',
        connectName: 'Kirill Shilov',
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
