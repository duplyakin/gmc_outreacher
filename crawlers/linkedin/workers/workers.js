//import LoginAction from __dirname  + "/./actions/loginAction.js"
//import SearchAction from __dirname  + "/./actions/searchAction.js"
//import ConnectAction from __dirname  + "/./actions/connectAction.js"
//import MessageAction from __dirname  + "/./actions/messageAction.js"
//import ScribeWorkAction from __dirname  + "/./actions/scribeWorkAction.js"
//import * from __dirname  + "/./actions/"
//const actions = require(__dirname + "/actions/LoginAction.js");
const modules = require('../modules.js');
module.exports.loginWorker = loginWorker;

async function loginWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let loginAction = new modules.loginAction.LoginAction(email, password, cookies);
  await loginAction.startBrowser();
  await loginAction.login();
  //await loginAction.closeBrowser();

}

async function searchWorker(task) {
  let searchUrl = task.url;
  let pageNum = task.pageNum;
  let cookies = task.cookies;

  let searchAction = new SearchAction(searchUrl, pageNum, cookies);
  await searchAction.startBrowser();
  let data = await searchAction.search();
  await searchAction.closeBrowser();

  return data;
}

async function connectWorker(task) {
  let connecthUrl = task.url;
  let text = task.text;
  let cookies = task.cookies;

  let connectAction = new ConnectAction(connecthUrl, text, cookies);
  await connectAction.startBrowser();
  await connectAction.connect();
  await connectAction.closeBrowser();

}

async function messageWorker(task) {
  let profileUrl = task.url;
  let text = task.text;
  let cookies = task.cookies;

  let messageAction = new MessageAction(profileUrl, text, cookies);
  await messageAction.startBrowser();
  await messageAction.message();
  await messageAction.closeBrowser();

}

async function scribeWorkWorker(task) {
  let url = task.url;
  let cookies = task.cookies;

  let scribeWorkAction = new ScribeWorkAction(url, cookies);
  await scribeWorkAction.startBrowser();
  await scribeWorkAction.scribe();
  await scribeWorkAction.closeBrowser();

}
