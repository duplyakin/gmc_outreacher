const puppeteer = require("./node_modules/puppeteer");
const links = require(__dirname + "/./links");

import LoginAction from __dirname  + "/./actions/loginAction.js"
import SearchAction from __dirname  + "/./actions/searchAction.js"
import ConnectAction from __dirname  + "/./actions/connectAction.js"

class LoginWorker {
  constructor(task) {
    this.email = task.email;
    this.password = task.password;

    this._cookies = task.cookies;
  }

  async function login() {
    let loginAction = LoginAction(this.email, this.password, this.cookies);
    await loginAction.startBrowser();
    await loginAction.login();
    await loginAction.closeBrowser();
  }
}

class SearchWorker {
  constructor(task) {
    this.searchUrl = task.searchUrl;
    this.pageNum = task.pageNum;

    this._cookies = task.cookies;
  }

  async function search() {
    let searchAction = SearchAction(this.searchUrl, this.pageNum, this.cookies);
    await searchAction.startBrowser();
    let data = await searchAction.search();
    await searchAction.closeBrowser();

    return data;
  }
}

class ConnectWorker {
  constructor(task) {
    this.connecthUrl = task.connecthUrl;
    this.text = task.text;

    this._cookies = task.cookies;
  }

  async function connect() {
    let connectAction = ConnectAction(this.connecthUrl, this.text, this.cookies);
    await connectAction.startBrowser();
    await connectAction.connect();
    await connectAction.closeBrowser();
  }
}
