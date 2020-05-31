const action = require('../linkedin/actions/loginAction.js');
const models_shared = require("../models/shared.js");

// test task

(async () => {
    console.log("..... test_task started: .....", __filename);
    try{

    let task_id = "5ece63a80a2de70af2b327d7";

    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0 }, { new: true });
    //let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { input_data.credentials_data.email: 0 }, { new: true });

    if (task == null) {
      console.log("..... task not found .....");
      return;
    }

    let input_data = task.input_data;

    if (input_data == null) {
        console.log("..... task.input_data not found .....");
        return;
    }

    input_data.credentials_data.email = 'clients@boostlabs.co.uk';
    input_data.credentials_data.password = '!@£$%^';
    input_data.credentials_data.li_at = '3454ccx';

    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { input_data: input_data });

    console.log( '..........task.............', task )

} catch(err) {
    console.log( '..........err.............', err.stack )
}

})();