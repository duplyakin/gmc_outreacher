const modules = require('../modules.js');
const cookieModel = require(__dirname + "/../.././models/models.js");
const taskModel = require(__dirname + "/../.././models/shared.js");

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');
const error_db_save_text = "........ERROR MONGODB: update TASK failed: ";
const success_db_save_text = "........SUCCSESS MONGODB: result_data added........";

// update cookies if: 1. old cookies, 2. there is no cookies
async function checkCookies(task_id, cookies) {
  if (cookies != undefined && cookies != null) {
    if (Date.now() / 1000 > cookies.expires) {
      await loginWorker(task_id);
    }
  } else {
    await loginWorker(task_id);
  }
}

async function loginWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let cookies_data = null;
    if(cookies != undefined && cookies != null) {
      cookies_data = cookies.data;
    }

    let loginAction = new modules.loginAction.LoginAction(email, password, cookies_data);
    await loginAction.startBrowser();
    let res = await loginAction.login();
    await loginAction.closeBrowser();

    let result = {
      code: 0,
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
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let searchUrl = task.input_data.campaign_data.next_url;
    let page_count = task.input_data.campaign_data.page_count;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let searchAction = new modules.searchAction.SearchAction(email, password, cookies.data, searchUrl, page_count);
    await searchAction.startBrowser();
    let res = await searchAction.search();
    await searchAction.closeBrowser();

    console.log('result_data: ', res);
    // if we got some exception (BAN?), we have to save results before catch Error and send task status -1
    await task.updateOne({ status: res.code >= 0 ? 5 : -1, result_data: res }, function (err, res) {
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
        code: MyExceptions.SearchWorkerError().code,
        raw: MyExceptions.SearchWorkerError("searchWorker error: " + err).error
      };
    }
    console.log("RES: ", err_result);

    await task.updateOne({ status: -1, result_data: err_result }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError(error_db_save_text + err);
       //updated!
      console.log(success_db_save_text);
    });

  }
}

async function connectWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let url = task.input_data.prospect_data.linkedin;
    let template = task.input_data.template_data.template;
    let data = task.input_data.prospect_data.template_data;

    let prospect_full_name = task.input_data.prospect_data.first_name + ' ' + task.input_data.prospect_data.last_name;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    // check connect
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, prospect_full_name);
    await connectCheckAction.startBrowser();
    let resCheck = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let res = false;
    if (!resCheck) {
      // connect if not connected
      let connectAction = new modules.connectAction.ConnectAction(email, password, cookies.data, url, template, data);
      await connectAction.startBrowser();
      res = await connectAction.connect();
      await connectAction.closeBrowser();
    } else {
      res = true;
      //throw MyExceptions.ConnectActionError('Connect is already connected: ' + err);
    }

    let result = {
      code: 0,
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
        code: MyExceptions.ConnectWorkerError().code,
        raw: MyExceptions.ConnectWorkerError("connectWorker error: " + err).error
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

async function messageWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let url = task.input_data.prospect_data.linkedin;
    let data = task.input_data.prospect_data;
    let template = task.input_data.template_data.template;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    // check reply
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(email, password, cookies.data, url);
    await messageCheckAction.startBrowser();
    let resCheckMsg = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    let task_status = 1;
    let result = {};
    if (resCheckMsg.message === '') {
      // if no reply - send msg
      let messageAction = new modules.messageAction.MessageAction(email, password, cookies.data, url, data, template);
      await messageAction.startBrowser();
      let res = await messageAction.message();
      await messageAction.closeBrowser();

      task_status = 5;
      result = {
        code: 0,
        if_true: res,
      };
    } else {
      // else - task finished
      task_status = 3;
      result = {
        code: 0,
        if_true: true,
        data: JSON.stringify(resCheckMsg)
      };
    }

    console.log('result_data: ', result);
    await task.updateOne({ status: task_status, result_data: result }, function (err, res) {
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
        code: MyExceptions.MessageWorkerError().code,
        raw: MyExceptions.MessageWorkerError("messageWorker error: " + err).error
      };
    }
    console.log("RES: ", err_result);

    console.log('result_data: ', result);
    await task.updateOne({ status: -1, result_data: err_result }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError(error_db_save_text + err);
      // updated!
      console.log(success_db_save_text);
    });

  }
}

async function scribeWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let url = task.input_data.prospect_data.linkedin;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let scribeAction = new modules.scribeAction.ScribeAction(email, password, cookies.data, url);
    await scribeAction.startBrowser();
    let res = await scribeAction.scribe();
    await scribeAction.closeBrowser();

    let result = {
      code: 0,
      if_true: true,
      data: JSON.stringify(res),
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
        code: MyExceptions.ScribeWorkerError().code,
        raw: MyExceptions.ScribeWorkerError("scribeWorker error: " + err).error
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

async function messageCheckWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    // CONNECT URL
    let url = task.input_data.prospect_data.linkedin;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(email, password, cookies.data, url);
    await messageCheckAction.startBrowser();
    let res = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    let result = {
      code: 0,
      if_true: (res.message === '' ? false : true),
      data: JSON.stringify(res)
    };
    console.log('result_data: ', result);

    await task.updateOne({ status: 3, result_data: result }, function (err, res) {
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
        code: MyExceptions.MessageCheckWorkerError().code,
        raw: MyExceptions.MessageCheckWorkerError("messageCheckWorker error: " + err).error
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

async function connectCheckWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.input_data.credentials_data.email;
    let password = task.input_data.credentials_data.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let prospect_full_name = task.input_data.prospect_data.first_name + ' ' + task.input_data.prospect_data.last_name;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, prospect_full_name);
    await connectCheckAction.startBrowser();
    let res = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let result = {
      code: 0,
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
        code: MyExceptions.ConnectCheckWorkerError().code,
        raw: MyExceptions.ConnectCheckWorkerError("connectCheckWorker error: " + err).error
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

module.exports = {
  loginWorker: loginWorker,
  searchWorker: searchWorker,
  connectWorker: connectWorker,
  messageWorker: messageWorker,
  scribeWorker: scribeWorker,
  messageCheckWorker: messageCheckWorker,
  connectCheckWorker: connectCheckWorker,
}
