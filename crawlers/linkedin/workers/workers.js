const modules = require('../modules.js');
const models_shared = require("../../models/shared.js");
const models = require("../../models/models.js");

const MyExceptions = require('../../exceptions/exceptions.js');


async function get_cookies(email, password, li_at, credentials_id) {

  let cookies = await models.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
  });
  
  let is_expired = check_expired(cookies); // true if we have to update cookies
  
  if (cookies == null || is_expired) {
    let loginAction = new modules.loginAction.LoginAction(email, password, li_at, credentials_id);
    await loginAction.startBrowser();
    await loginAction.login();
    await loginAction.closeBrowser();

    cookies = await models.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
    });
  
    return cookies.data; 
  }
  
  return cookies.data;
}
  

function check_expired(cookies) {
	if (cookies == null){
		return true;
  }
	return (Date.now() / 1000 > cookies.expires);
}


function get_val_0(target, name, default_val = null) {
  return target.hasOwnProperty(name) ? target[name] : default_val;
}  

function get_val(target, name) {
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


async function searchWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);
    //console.log("..... task_data: .....", task_data);
    
    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let searchAction = new modules.searchAction.SearchAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.campaign_data.next_url, task_data.campaign_data.page_count);
    await searchAction.startBrowser();
    result_data = await searchAction.search();
    await searchAction.closeBrowser();

    status = result_data.code >= 0 ? 5 : -1;  // if we got some exception (BAN?), we have to save results before catch Error and send task status -1
   
  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.SearchWorkerError().code,
        raw: MyExceptions.SearchWorkerError("searchWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


async function connectWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    let prospect_full_name = task_data.prospect_data.first_name + ' ' + task_data.prospect_data.last_name;

    // start work
    // check connect
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, prospect_full_name);
    await connectCheckAction.startBrowser();
    let resCheck = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let res = false;
    if (!resCheck) {
      // connect if not connected
      let connectAction = new modules.connectAction.ConnectAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.prospect_data.linkedin, task_data.template_data.message, task_data.prospect_data);
      await connectAction.startBrowser();
      res = await connectAction.connect();
      await connectAction.closeBrowser();
    } else {
      res = true;
      //throw MyExceptions.ConnectActionError('Connect is already connected: ' + err);
    }

    result_data = {
      code: 0,
      if_true: res,
    };
    status = 5

  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.ConnectWorkerError().code,
        raw: MyExceptions.ConnectWorkerError("connectWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


async function messageWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    // check reply
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.prospect_data.linkedin);
    await messageCheckAction.startBrowser();
    let resCheckMsg = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    if (resCheckMsg.message === '') {
      // if no reply - send msg
      let messageAction = new modules.messageAction.MessageAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.prospect_data.linkedin, task_data.prospect_data, task_data.template_data.message);
      await messageAction.startBrowser();
      let res = await messageAction.message();
      await messageAction.closeBrowser();

      result_data = {
        code: 0,
        if_true: res,
      };
    } else {
      // else - task finished
      result_data = {
        code: 2000,
        if_true: true,
        data: JSON.stringify(resCheckMsg)
      };
    }
    status = 5;
    
  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.MessageWorkerError().code,
        raw: MyExceptions.MessageWorkerError("messageWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


async function scribeWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let scribeAction = new modules.scribeAction.ScribeAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.prospect_data.linkedin);
    await scribeAction.startBrowser();
    let res = await scribeAction.scribe();
    await scribeAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: true,
      data: JSON.stringify(res),
    };
    status = 5;

  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.ScribeWorkerError().code,
        raw: MyExceptions.ScribeWorkerError("scribeWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


async function messageCheckWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, task_data.prospect_data.linkedin);
    await messageCheckAction.startBrowser();
    let res = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    result_data = {
      code: (res.message === '' ? 0 : 2000),
      if_true: (res.message === '' ? false : true),
      data: JSON.stringify(res)
    };
    status = 5;

  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.MessageCheckWorkerError().code,
        raw: MyExceptions.MessageCheckWorkerError("messageCheckWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


async function connectCheckWorker(task_id) {
  let status = -1; 
  let result_data = {};
  let task = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = get_val(task, 'credentials_id');
    if (!credentials_id) {
      throw new Error ('there is no task.credentials_id');
    }
    let input_data = get_val(task, 'input_data');
    if (!input_data) {
      throw new Error ('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let prospect_full_name = task_data.prospect_data.first_name + ' ' + task_data.prospect_data.last_name;

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, cookies, credentials_id, prospect_full_name);
    await connectCheckAction.startBrowser();
    let res = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: res,
    };
    status = 5;

  } catch (err) {

    console.log( err.stack )

    if (err.code !== undefined && err.code !== null) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else {
      result_data = {
        code: MyExceptions.ConnectCheckWorkerError().code,
        raw: MyExceptions.ConnectCheckWorkerError("connectCheckWorker error: " + err).error
      };
    }
    status = -1;

  } finally {
    console.log("RES: ", result_data);
    if(task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
    }
  }
}


module.exports = {
  searchWorker: searchWorker,
  connectWorker: connectWorker,
  messageWorker: messageWorker,
  scribeWorker: scribeWorker,
  messageCheckWorker: messageCheckWorker,
  connectCheckWorker: connectCheckWorker,
}
