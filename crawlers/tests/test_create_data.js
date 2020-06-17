const action = require('../linkedin/actions/loginAction.js');
const models_shared = require("../models/shared.js");
const models = require("../models/models.js");

const SEARCH_URL = "https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";

// test task

(async () => {
    console.log("..... test_create_data started: .....", __filename);
    try{

    let account_id = "111113a80a2de70af2b11111"; // test id
    let task_id = "000003a80a2de70af2b00000"; // test id

    let task_data = {
        action_key: '',
        input_data: {
            campaign_data: {
              search_url: SEARCH_URL,
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
          credentials_id: account_id,
          ack: 0,
    }

    let account_data = {
        login: "grinnbob@rambler.ru",
        password: "",
        cookies: [{
            name : "li_at",
            value : "AQEDARcxwXEBb18zAAABcflw5z8AAAFyHX1rP00AVzV1p6dd9IpqrPbIfjq5ajRuaeHm8ZvSGYaQccRo1fX80kr0WHCDWLOvuPfz-uiAn-dw631pZyHV2ZdU66bPPX4J--EXfE0IxqwMYTi8bIiWfL8U",
            domain : '.linkedin.com',
            path : "/",
            expires : Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
            size : 127,
            httpOnly : true,
            secure : true,
            session : false,
            sameSite : "None"
        }],
        expires: Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
        status: 0,
    }

    let account = await models.Accounts.findOneAndUpdate({ _id: account_id }, account_data, { new: true, upsert: true });
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, task_data, { new: true, upsert: true });

    console.log( '..........account.............', account )
    console.log( '..........task.............', task )

} catch(err) {
    console.log( '..........err.............', err.stack )
}

})();