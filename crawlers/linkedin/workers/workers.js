const modules = require('../modules.js');
const models_shared = require("../../models/shared.js");
const models = require("../../models/models.js");

const MyExceptions = require('../../exceptions/exceptions.js');

const status_codes = require('../status_codes')


async function get_cookies(credentials_id) {

  let account = await models.Accounts.findOne({ _id: credentials_id }, function (err, res) {
    if (err) throw MyExceptions.MongoDBError('MongoDB find account err: ' + err);
  });

  let is_expired = check_expired(account); // true if we have to update cookies

  if (account == null || is_expired) {
    let loginAction = new modules.loginAction.LoginAction(credentials_id);
    await loginAction.startBrowser();
    await loginAction.login();
    await loginAction.closeBrowser();

    account = await models.Accounts.findOne({ _id: credentials_id }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find account err: ' + err);
    });

    return account.cookies;
  }

  return account.cookies;
}


function check_expired(account) {
  if (account == null) {
    return true;
  }
  return (Date.now() / 1000 > account.expires);
}


function serialize_data(input_data) {
  if (!input_data) {
    throw new Error('SERIALIZATION error: input_data can’t be empty');
  }

  let task_data = {};

  task_data['campaign_data'] = input_data.campaign_data;
  task_data['template_data'] = input_data.template_data;
  task_data['prospect_data'] = input_data.prospect_data;

  return task_data;
}


async function searchWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);
    //console.log("..... task_data: .....", task_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    searchAction = new modules.searchAction.SearchAction(cookies, credentials_id, task_data.campaign_data.search_url, task_data.campaign_data.interval_pages);
    browser = await searchAction.startBrowser();
    result_data = await searchAction.search();
    browser = await searchAction.closeBrowser();

    status = result_data.code >= 0 ? 5 : -1;  // if we got some exception (BAN?), we have to save results before catch Error and send task status -1

  } catch (err) {

    console.log(err.stack)

    status = status_codes.FAILED;

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.SearchWorkerError().code,
        raw: MyExceptions.SearchWorkerError("searchWorker error: " + err).error
      };
    }

  } finally {
    //console.log("SearchWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function connectWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    let message = '';
    if (task_data.template_data != null) {
      if (task_data.template_data.message != null)
        message = task_data.template_data.message;
    }

    let connectAction = new modules.connectAction.ConnectAction(cookies, credentials_id, task_data.prospect_data.linkedin, message, task_data.prospect_data);
    browser = await connectAction.startBrowser();
    res = await connectAction.connect();
    browser = await connectAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: res,
    };
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.ConnectWorkerError().code,
        raw: MyExceptions.ConnectWorkerError("connectWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
    //console.log("ConnectWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function messageWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    // check reply
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(cookies, credentials_id, task_data.prospect_data.linkedin);
    browser = await messageCheckAction.startBrowser();
    let resCheckMsg = await messageCheckAction.messageCheck();
    browser = await messageCheckAction.closeBrowser();

    if (resCheckMsg.message === '') {
      // if no reply - send msg
      let messageAction = new modules.messageAction.MessageAction(cookies, credentials_id, task_data.prospect_data.linkedin, task_data.prospect_data, task_data.template_data.message);
      browser = await messageAction.startBrowser();
      let res = await messageAction.message();
      browser = await messageAction.closeBrowser();

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
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.MessageWorkerError().code,
        raw: MyExceptions.MessageWorkerError("messageWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
    //console.log("MessageWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function scribeWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    let scribeAction = new modules.scribeAction.ScribeAction(cookies, credentials_id, task_data.prospect_data.linkedin);
    browser = await scribeAction.startBrowser();
    let res = await scribeAction.scribe();
    browser = await scribeAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: true,
      data: JSON.stringify(res),
    };
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.ScribeWorkerError().code,
        raw: MyExceptions.ScribeWorkerError("scribeWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
   // console.log("ScribeWorker RES: ", result_data);
    
    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function messageCheckWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(cookies, credentials_id, task_data.prospect_data.linkedin);
    browser = await messageCheckAction.startBrowser();
    let res = await messageCheckAction.messageCheck();
    browser = await messageCheckAction.closeBrowser();

    result_data = {
      code: (res.message == '' ? 0 : 2000),
      if_true: (res.message == '' ? false : true),
      data: JSON.stringify(res)
    };
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.MessageCheckWorkerError().code,
        raw: MyExceptions.MessageCheckWorkerError("messageCheckWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
   // console.log("MessageCheckWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function connectCheckWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(cookies, credentials_id, task_data.prospect_data.linkedin);
    browser = await connectCheckAction.startBrowser();
    let res = await connectCheckAction.connectCheck();
    browser = await connectCheckAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: res,
    };
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.ConnectCheckWorkerError().code,
        raw: MyExceptions.ConnectCheckWorkerError("connectCheckWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
   // console.log("ConnectCheckWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
    }
  }
}


async function visitProfileWorker(task_id) {
  let status = status_codes.FAILED;
  let result_data = {};
  let task = null;
  let credentials_id = null;

  let browser = null;
  try {
    task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, ack: 0 }, { ack: 1 }, { new: true, upsert: false });
    if (task == null) {
      console.log("..... task not found or locked: .....");
      return;
    }

    credentials_id = task.credentials_id;
    if (!credentials_id) {
      throw new Error('there is no task.credentials_id');
    }
    let input_data = task.input_data;
    if (!input_data) {
      throw new Error('there is no task.input_data');
    }
    let task_data = serialize_data(input_data);

    let cookies = await get_cookies(credentials_id);

    // start work
    let visitProfileAction = new modules.visitProfileAction.VisitProfileAction(cookies, credentials_id, task_data.prospect_data.linkedin);
    browser = await visitProfileAction.startBrowser();
    let res = await visitProfileAction.visit();
    browser = await visitProfileAction.closeBrowser();

    result_data = {
      code: 0,
      if_true: res,
    };
    status = status_codes.CARRYOUT;

  } catch (err) {

    console.log(err.stack)

    if (err.code != null && err.code != -1) {
      result_data = {
        code: err.code,
        raw: err.error
      };
    } else if (err.code == -1) {
      status = status_codes.BLOCK_HAPPENED;
      // Context error
      result_data = {
        code: err.code,
        raw: err.error
      };
      await models.Accounts.findOneAndUpdate({ _id: credentials_id }, { task_id: task_id }, { upsert: false });
      
    } else {
      result_data = {
        code: MyExceptions.VisitProfileWorkerError().code,
        raw: MyExceptions.VisitProfileWorkerError("visitProfileWorker error: " + err).error
      };
    }
    status = status_codes.FAILED;

  } finally {
   // console.log("VisitProfileWorker RES: ", result_data);

    if (task !== null) {
      await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { ack: 0, status: status, result_data: result_data, is_queued: 0 }, { upsert: false });
    }

    if(browser != null) {
      await browser.close();
      browser.disconnect();
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
  visitProfileWorker: visitProfileWorker,
}
