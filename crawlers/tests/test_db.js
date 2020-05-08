const workers = require(__dirname + '/../linkedin/workers/workers.js');


const SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";
const MY_URL = "https://www.linkedin.com/in/grigoriy-polyanitsin/";

// test running

(async () => {
  console.log("..... test_db started: .....", __filename);

  let task = {
    email: "grinnbob@rambler.ru",
    password: "linked123",
    url: CONNECT_URL,
    pageNum: 9,
    data: {
      first_name: 'Kirill',
      last_name: 'Shilov',
      company_name: 'howtotoken.com'
    },
    template: `test 123v {first_name} olololv 132 d ${first_name} oloodv`,
    connectName: 'Kirill Shilov',
  };
  //var first_name = task.data.first_name;
  //var my_template = (first_name) => task.template;
  //console.log('---------------------', my_template(first_name));

  //await workers.loginWorker(task);
  //await workers.searchWorker(task);
  //await workers.connectWorker(task);
  //await workers.messageWorker(task);
  //await workers.scribeWorkWorker(task);
  //await workers.messageCheckWorker(task);
  //await workers.connectCheckWorker(task);

})();
