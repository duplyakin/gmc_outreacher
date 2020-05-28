const action = require('../linkedin/actions/loginAction.js');
const models_shared = require("../models/shared.js");

// test login

(async () => {
    console.log("..... test_login started: .....", __filename);
    try{

    let task_id = "5ece63a80a2de70af2b327d7";

    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    //console.log( '..........typeof task.............', typeof task )
    //console.log( '..........task["credentials_id"].............', task["credentials_id"] )
    //console.log( '..........hasOwnProperty.............', task.hasOwnProperty("credentials_id") )

    let credentials_id = get_val(task, "credentials_id");
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id: ', credentials_id);
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    //console.log( '..........task_data.............', task_data )

    let loginAction = new action.LoginAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    await loginAction.startBrowser();
    await loginAction.login();
    await loginAction.closeBrowser();
} catch(err) {
    console.log( '..........err.............', err.stack )
}

})();


function get_val(target, name, default_val = null) {
    //console.log( '..........target.............', target )
    console.log( '..........name.............', name )
    console.log( '..........hasOwnProperty.............', target.hasOwnProperty(name) )
    //return target.hasOwnProperty(name) ? target[name] : default_val;
    return target[name];
}
  
  
function serialize_data(input_data) {
    if (!input_data){
        throw new Error ('SERIALIZATION error: input_data can’t be empty');
    }
        
    let task_data = {};
        
    task_data['credentials_data'] = get_val(input_data, 'credentials_data', {})
    task_data['campaign_data'] = get_val(input_data, 'campaign_data', {})
    task_data['template_data'] = get_val(input_data, 'template_data', {})
    task_data['prospect_data'] = get_val(input_data, 'prospect_data', {})
        
    return task_data;
}
