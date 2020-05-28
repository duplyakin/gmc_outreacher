const action = require('../linkedin/actions/loginAction.js');
const models_shared = require("../models/shared.js");

// test login

(async () => {
    console.log("..... test_login started: .....", __filename);
    try{

    let task_id = "5ece63a80a2de70af2b327d7";

    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0 }, { new: true });
    //let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { input_data.credentials_data.email: 0 }, { new: true });

    if (task == null) {
      console.log("..... task not found .....");
      return;
    }

    let input_data = get_val(task, 'input_data');
    input_data.credentials_data.email = 'clients@boostlabs.co.uk';
    input_data.credentials_data.password = '!@£$%^';
    input_data.credentials_data.li_at = 'AQEDARcxwXEBb18zAAABcflw5z8AAAFyHX1rP00AVzV1p6dd9IpqrPbIfjq5ajRuaeHm8ZvSGYaQccRo1fX80kr0WHCDWLOvuPfz-uiAn-dw631pZyHV2ZdU66bPPX4J--EXfE0IxqwMYTi8bIiWfL8U';

    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { input_data: input_data });


    /*
    task.input_data.credentials_data.li_at = '',
    task.input_data.credentials_data.email = 'grinnbob@rambler.ru',
    task.input_data.credentials_data.password = 'linkedin123',
    await task.save();
    */

    console.log( '..........task.............', task )

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
