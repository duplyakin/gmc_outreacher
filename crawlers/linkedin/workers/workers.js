const modules = require('../modules.js');


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
  let email = task.email;
  let password = task.password;
  let searchUrl = task.url;
  let pageNum = task.pageNum;
  let cookies = task.cookies;

  // check cookies
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

  // start work
  let searchAction = new modules.searchAction.SearchAction(email, password, cookies.data, searchUrl, pageNum);
  await searchAction.startBrowser();
  let data = await searchAction.search();
  await searchAction.closeBrowser();

  // TODO: write in taskQueue resultData
  return data;
}

async function connectWorker(task) {
  let connecthUrl = task.url;
  let text = task.text;
  let cookies = task.cookies;

  let connectAction = new modules.ConnectAction(connecthUrl, text, cookies);
  await connectAction.startBrowser();
  await connectAction.connect();
  await connectAction.closeBrowser();

}

async function messageWorker(task) {
  let profileUrl = task.url;
  let text = task.text;
  let cookies = task.cookies;

  let messageAction = new modules.MessageAction(profileUrl, text, cookies);
  await messageAction.startBrowser();
  await messageAction.message();
  await messageAction.closeBrowser();

}

async function scribeWorkWorker(task) {
  let url = task.url;
  let cookies = task.cookies;

  let scribeWorkAction = new modules.ScribeWorkAction(url, cookies);
  await scribeWorkAction.startBrowser();
  await scribeWorkAction.scribe();
  await scribeWorkAction.closeBrowser();

}

module.exports = {
    loginWorker: loginWorker,
    searchWorker: searchWorker,
}
