const modules = require('../modules.js');
const cookieModel = require(__dirname + "/../.././models/models.js");
const taskModel = require(__dirname + "/../.././models/shared.js");

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');
const error_db_save_text = "........ERROR MONGODB: update TASK failed: ";
const success_db_save_text = "........SUCCSESS MONGODB: result_data added........";


async function checkCookies(task_id, cookies) {
  if (cookies != undefined || cookies != null) {
    if (Date.now() / 1000 > cookies.expires) {
      loginWorker(task_id);
    }
  } else {
    loginWorker(task_id);
  }
}

async function loginWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data);
    await loginAction.startBrowser();
    let res = await loginAction.login();
    await loginAction.closeBrowser();

    let result = {
      code: 0,
      if_true: res,
    };

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.LoginWorkerError().code,
        if_true: false,
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
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let searchUrl = task.url;
    let pageNum = task.pageNum;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let searchAction = new modules.searchAction.SearchAction(email, password, cookies.data, searchUrl, pageNum);
    await searchAction.startBrowser();
    let res = await searchAction.search();
    await searchAction.closeBrowser();

    let result = {
      code: 0,
      raw: res,
    };

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.SearchWorkerError().code,
        if_true: false,
        raw: MyExceptions.SearchWorkerError("searchWorker error: " + err).error
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

async function connectWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let connecthUrl = task.url;
    let template = task.template;
    let data = task.data;

    let connectName = task.connectName;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    // check connect
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, connectName);
    await connectCheckAction.startBrowser();
    let resCheck = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let res = false;
    if (!resCheck) {
      // connect if not connected
      let connectAction = new modules.connectAction.ConnectAction(email, password, cookies.data, connecthUrl, template, data);
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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.ConnectWorkerError().code,
        if_true: false,
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
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let url = task.url;
    let data = task.data;
    let template = task.template;

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
    if (resCheckMsg === '') {
      // if no reply - send msg
      let messageAction = new modules.messageAction.MessageAction(email, password, cookies.data, url, data, template);
      await messageAction.startBrowser();
      res = await messageAction.message();
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
        raw: resCheckMsg
      };
    }

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.MessageWorkerError().code,
        if_true: false,
        raw: MyExceptions.MessageWorkerError("messageWorker error: " + err).error
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

async function scribeWorkWorker(task_id) {
  try {
    /*let task = await taskModel.TaskQueue.findOne({ id: task_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });*/
    let task = task_id;
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let url = task.url;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let scribeWorkAction = new modules.scribeWorkAction.ScribeWorkAction(email, password, cookies.data, url);
    await scribeWorkAction.startBrowser();
    let res = await scribeWorkAction.scribe();
    await scribeWorkAction.closeBrowser();

    let result = {
      code: 0,
      //if_true: true,
      raw: JSON.stringify(res),
    };

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.ScribeWorkerError().code,
        if_true: false,
        raw: MyExceptions.ScribeWorkerError("scribeWorkWorker error: " + err).error
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
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    // CONNECT URL
    let url = task.url;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(email, password, cookies.data, url);
    await messageCheckAction.startBrowser();
    let res = await messageCheckAction.messageCheck();
    await messageCheckAction.closeBrowser();

    let result = {
      code: 0,
      if_true: (res === '' ? false : true),
      raw: res
    };

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.MessageCheckWorkerError().code,
        if_true: false,
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
    let email = task.email;
    let password = task.password;
    let cookies = await cookieModel.Cookies.findOne({ username: email });

    let connectName = task.connectName;

    // check cookies
    await checkCookies(task_id, cookies);

    // start work
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, connectName);
    await connectCheckAction.startBrowser();
    let res = await connectCheckAction.connectCheck();
    await connectCheckAction.closeBrowser();

    let result = {
      code: 0,
      if_true: res,
    };

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
        if_true: false,
        raw: err.error
      };
    } else {
      err_result = {
        code: MyExceptions.ConnectCheckWorkerError().code,
        if_true: false,
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
  scribeWorkWorker: scribeWorkWorker,
  messageCheckWorker: messageCheckWorker,
  connectCheckWorker: connectCheckWorker,
}
