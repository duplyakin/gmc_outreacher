const modules = require('../modules.js');
const cookieModel = require(__dirname + "/../.././models/models.js");

async function checkCookies(task, cookies) {
  if(cookies != undefined || cookies != null) {
    if(Date.now() / 1000 > cookies.expires) {
      loginWorker(task);
    }
  } else {
    loginWorker(task);
  }
}

async function loginWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data);
  await loginAction.startBrowser();
  let result = await loginAction.login();

  await task.updateOne({result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });

  if(!result) {
    // throw exception;
  }

}

async function searchWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let searchUrl = task.url;
  let pageNum = task.pageNum;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let searchAction = new modules.searchAction.SearchAction(email, password, cookies.data, searchUrl, pageNum);
  await searchAction.startBrowser();
  let result = await searchAction.search();
  await searchAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
}

async function connectWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let connecthUrl = task.url;
  let text = task.text;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let connectAction = new modules.connectAction.ConnectAction(email, password, cookies.data, connecthUrl, text);
  await connectAction.startBrowser();
  let result = await connectAction.connect();
  await connectAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
}

async function messageWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let profileUrl = task.url;
  let text = task.text;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let messageAction = new modules.messageAction.MessageAction(email, password, cookies.data, profileUrl, text);
  await messageAction.startBrowser();
  let result = await messageAction.message();
  await messageAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
}

async function scribeWorkWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let url = task.url;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let scribeWorkAction = new modules.scribeWorkAction.ScribeWorkAction(email, password, cookies.data, url);
  await scribeWorkAction.startBrowser();
  let result = await scribeWorkAction.scribe();
  await scribeWorkAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
}

async function messageCheckWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let url = task.url;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(email, password, cookies.data, url);
  await messageCheckAction.startBrowser();
  let result = await messageCheckAction.messageCheck();
  await messageCheckAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
}

async function connectCheckWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = await cookieModel.Cookies.findOne({username: email});

  let connectName = task.connectName;

  // check cookies
  await checkCookies(task, cookies);

  // start work
  let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, connectName);
  await connectCheckAction.startBrowser();
  let result = await connectCheckAction.connectCheck();
  await connectCheckAction.closeBrowser();

  await task.updateOne({status: 4, result_data: result}, function(err, res) {
    // updated!
    console.log('........result_data added in mongoDB.......');
  });
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
