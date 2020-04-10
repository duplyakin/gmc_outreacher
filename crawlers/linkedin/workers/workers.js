import LoginAction from __dirname  + "/./actions/loginAction.js"
import SearchAction from __dirname  + "/./actions/searchAction.js"
import ConnectAction from __dirname  + "/./actions/connectAction.js"


async function loginWorker(task) {
  let email = task.email;
  let password = task.password;
  let cookies = task.cookies;

  let loginAction = LoginAction(email, password, cookies);
  await loginAction.startBrowser();
  await loginAction.login();
  await loginAction.closeBrowser();

}

async function searchWorker(task) {
  let searchUrl = task.searchUrl;
  let pageNum = task.pageNum;
  let cookies = task.cookies;

  let searchAction = SearchAction(searchUrl, pageNum, cookies);
  await searchAction.startBrowser();
  let data = await searchAction.search();
  await searchAction.closeBrowser();

  return data;
}

async function connectWorker(task) {
  let connecthUrl = task.connecthUrl;
  let text = task.text;
  let cookies = task.cookies;

  let connectAction = ConnectAction(connecthUrl, text, cookies);
  await connectAction.startBrowser();
  await connectAction.connect();
  await connectAction.closeBrowser();

}
