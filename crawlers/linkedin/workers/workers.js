const modules = require('../modules.js');
const models_shared = require("../../models/shared.js");
const models = require("../../models/models.js");

const MyExceptions = require('../../exceptions/exceptions.js');
const error_db_save_text = "........ERROR MONGODB: update TASK failed: ";
const success_db_save_text = "........SUCCSESS MONGODB: result_data added........";


async function get_cookies(email, password, li_at, credentials_id) {
  console.log('.......typeof..credentials_id........ ', typeof credentials_id)
  console.log('.........credentials_id........ ', credentials_id)

  let cookies = await models.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
    if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
  });

  // update cookies if: 1. old cookies, 2. there is no cookies
  if (cookies != undefined && cookies != null) {
    // cookies defined
    if (Date.now() / 1000 > cookies.expires) {
      // check - if cookies old
      // login
      let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data, credentials_id);
      await loginAction.startBrowser();
      await loginAction.login();
      await loginAction.closeBrowser();

      cookies = await models.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
      }); 
    }

    if(cookies !== null) {
      return cookies.data;
    } else {
      return null;
    }

  } else {
    // cookies not defined
    let cookies_data = null;
    if (li_at !== '' && li_at != undefined && li_at != null) {
      cookies_data = [{
        name : "li_at",
        value : li_at,
        domain : ".www.linkedin.com",
        path : "/",
        expires : Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
        size : (new TextEncoder().encode(li_at)).length,
        httpOnly : true,
        secure : true,
        session : false,
        sameSite : "None"
      }];
    };

    // login
    let loginAction = new modules.loginAction.LoginAction(email, password, cookies_data, credentials_id);
    await loginAction.startBrowser();
    await loginAction.login();
    await loginAction.closeBrowser();

    cookies = await models.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
    });

    if(cookies !== null) {
      return cookies.data;
    } else {
      return null;
    }
  }
}


function serialize_data(task_data, task) {
  for (var key in task) {
    if (task_data.hasOwnProperty(key) && task[key]){
        //task_data[key] = JSON.parse(task[key]);
        task_data[key] = task[key];
    }
  }
  return task_data;
}


// todo: delete it...
async function loginWorker(task_id) {
  try {
    /*
    let task = await models_shared.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find TASK err: ' + err);
    });*/
    let task = task_id.input_data;
    let credentials_id = task_id.credentials_id;

    let task_data = {
      credentials_data: {
          email: '',
          password: '',
          li_at: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    /*
    if (task_data.credentials_data.li_at === '' && (task_data.credentials_data.email === '' || task_data.credentials_data.password === '')) {
      throw MyExceptions.LoginWorkerError('Empty credentials - login/password or li_at required.');
    }
    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);
    */

    //
    let cookies_data = null;
    if (task_data.credentials_data.li_at !== '') {
      cookies_data = [{
        name : "li_at",
        value : task_data.credentials_data.li_at,
        domain : ".www.linkedin.com",
        path : "/",
        expires : Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
        size : (new TextEncoder().encode(task_data.credentials_data.li_at)).length,
        httpOnly : true,
        secure : true,
        session : false,
        sameSite : "None"
      }];

    } else if (task_data.credentials_data.email !== '' && task_data.credentials_data.password !== '') {

      cookies = await cookieModel.Cookies.findOne({ credentials_id: credentials_id }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
      });

      if (cookies != undefined && cookies != null) {
        cookies_data = cookies.data;
      } 
    } else {
      throw MyExceptions.LoginWorkerError('Empty credentials - login/password or li_at required.');
    }

    let loginAction = new modules.loginAction.LoginAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies_data, credentials_id);
    await loginAction.startBrowser();
    let res = await loginAction.login();
    await loginAction.closeBrowser();
    //

    let result = {
      code: 0,
      //if_true: cookies ? true : false, // if we here - we loggedin
      if_true: res,
    };

    console.log('result_data: ', result);
    await task.updateOne({ status: 5, result_data: result }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError(error_db_save_text + err);
      // updated!
      console.log(success_db_save_text);
    });

  } catch (err) {

    let err_result = {};
    if (err.code !== undefined && err.code !== null) {
      err_result = {
        code: err.code,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.LoginWorkerError().code,
        raw: MyExceptions.LoginWorkerError("loginWorker error: " + err).error
      };
    }
    console.log("RES: ", err_result);

    await task.updateOne({ status: -1, result_data: err_result }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError(error_db_save_text + err);
      // updated!
      console.log(success_db_save_text);
    });

  }
}


async function searchWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      campaign_data: {
        next_url: '',
        page_count: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let searchAction = new modules.searchAction.SearchAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.campaign_data.next_url, task_data.campaign_data.page_count);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


async function connectWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      prospect_data: {
        first_name: '',
        last_name: '',
        company_title: '',
        linkedin: '',
      },
      template_data: {
        body: ''
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    let prospect_full_name = task_data.prospect_data.first_name + ' ' + task_data.prospect_data.last_name;

    // start work
    // check connect
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, prospect_full_name);
    await connectCheckAction.startBrowser();
    let resCheck = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let res = false;
    if (!resCheck) {
      // connect if not connected
      let connectAction = new modules.connectAction.ConnectAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.prospect_data.linkedin, task_data.template_data.body, task_data.prospect_data);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


async function messageWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      prospect_data: {
        first_name: '',
        last_name: '',
        company_title: '',
        linkedin: '',
      },
      template_data: {
        body: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    // check reply
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.prospect_data.linkedin);
    await messageCheckAction.startBrowser();
    let resCheckMsg = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    if (resCheckMsg.message === '') {
      // if no reply - send msg
      let messageAction = new modules.messageAction.MessageAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.prospect_data.linkedin, task_data.prospect_data, task_data.template_data.body);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


async function scribeWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      prospect_data: {
        linkedin: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let scribeAction = new modules.scribeAction.ScribeAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.prospect_data.linkedin);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


async function messageCheckWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      prospect_data: {
        linkedin: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, task_data.prospect_data.linkedin);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


async function connectCheckWorker(task_id) {
  let status = -1; 
  let result_data = {};
  try {
    let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true });
    if (!task) {
      console.log("..... task not found or locked: .....");
      return;
    }

    let credentials_id = task.credentials_id;

    let task_data = {
      credentials_data: {
        email: '',
        password: '',
        li_at: '',
      },
      prospect_data: {
        first_name: '',
        last_name: '',
        company_title: '',
        linkedin: '',
      }
    }

    task_data = serialize_data(task_data, task.input_data);

    let prospect_full_name = task_data.prospect_data.first_name + ' ' + task_data.prospect_data.last_name;

    let cookies = await get_cookies(task_data.credentials_data.email, task_data.credentials_data.password, task_data.credentials_data.li_at, credentials_id);

    // start work
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(task_data.credentials_data.email, task_data.credentials_data.password, cookies, credentials_id, prospect_full_name);
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
    await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data }, { new: true });
  }
}


module.exports = {
  loginWorker: loginWorker,
  searchWorker: searchWorker,
  connectWorker: connectWorker,
  messageWorker: messageWorker,
  scribeWorker: scribeWorker,
  messageCheckWorker: messageCheckWorker,
  connectCheckWorker: connectCheckWorker,
}
