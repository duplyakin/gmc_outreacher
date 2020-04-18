const modules = require('../modules.js');

async function checkCookies(cookies) {
  if(cookies != undefined || cookies != null) {
    if(Date.now() / 1000 > cookies.expires) {
      let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data);
      await loginAction.startBrowser();
      await loginAction.login();
    }
  } else {
    let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data);
    await loginAction.startBrowser();
    await loginAction.login();
  }
}

async function loginWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let loginAction = new modules.loginAction.LoginAction(email, password, cookies.data);
  await loginAction.startBrowser();
  await loginAction.login();
  //await loginAction.closeBrowser();

}

async function searchWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let searchUrl = task.url;
  let pageNum = task.pageNum;

  // check cookies
  await checkCookies(cookies);

  // start work
  let searchAction = new modules.searchAction.SearchAction(email, password, cookies.data, searchUrl, pageNum);
  await searchAction.startBrowser();
  let data = await searchAction.search();
  await searchAction.closeBrowser();

  // TODO: write in taskQueue resultData
  return data;
}

async function connectWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let connecthUrl = task.url;
  let text = task.text;

  // check cookies
  await checkCookies(cookies);

  // start work
  let connectAction = new modules.connectAction.ConnectAction(email, password, cookies.data, connecthUrl, text);
  await connectAction.startBrowser();
  await connectAction.connect();
  await connectAction.closeBrowser();

}

async function messageWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let profileUrl = task.url;
  let text = task.text;

  // check cookies
  await checkCookies(cookies);

  // start work
  let messageAction = new modules.messageAction.MessageAction(email, password, cookies.data, profileUrl, text);
  await messageAction.startBrowser();
  await messageAction.message();
  await messageAction.closeBrowser();

}

async function scribeWorkWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let url = task.url;

  // check cookies
  await checkCookies(cookies);

  // start work
  let scribeWorkAction = new modules.scribeWorkAction.ScribeWorkAction(email, password, cookies.data, url);
  await scribeWorkAction.startBrowser();
  await scribeWorkAction.scribe();
  await scribeWorkAction.closeBrowser();

}

async function messageCheckWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let url = task.url;

  // check cookies
  await checkCookies(cookies);

  // start work
  let messageCheckAction = new modules.messageCheckAction.MessageCheckAction(email, password, cookies.data, url);
  await messageCheckAction.startBrowser();
  await messageCheckAction.messageCheck();
  await messageCheckAction.closeBrowser();

}

async function connectCheckWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let connectName = task.connectName;

  // check cookies
  await checkCookies(cookies);

  // start work
  let connectCheckAction = new modules.connectCheckAction.ConnectCheckAction(email, password, cookies.data, connectName);
  await connectCheckAction.startBrowser();
  await connectCheckAction.connectCheck();
  await connectCheckAction.closeBrowser();

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
