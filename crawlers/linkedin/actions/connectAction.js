const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

class ConnectAction {
  constructor(email, password, cookies, connectUrl, text) {
    this.email = email;
    this.password = password;

    this.connectUrl = connectUrl;
    this.text = text;

    //this.cookies = JSON.parse(cookies);
    this.cookies = cookies;
  }

  // do 1 trie to connect URL or goto login
  async gotoChecker(url) {
    await this.page.goto(url);
    let current_url = await this.page.url();
    if(current_url.includes('login') || current_url.includes('signup')) {
      let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
      await loginAction.setContext(this.context);
      let result = await loginAction.login();
      if(!result) {
        // TODO: throw exception
        return false;
      } else {
        await this.page.goto(url);
        return true;
      }
    } else {
      return true;
    }
  }

  async startBrowser() {
    this.browser = await puppeteer.launch({ headless: false });
    //this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async closeBrowser(browser) {
    this.browser.close();
  }

  async connect() {
    await this.gotoChecker(this.connectUrl);

    await this.page.click(selectors.CONNECT_SELECTOR);
    // TODO: add logic for connected links

    await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    await this.page.waitForSelector(selectors.MSG_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);

    await this.page.keyboard.type(this.text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
  }
}

module.exports = {
    ConnectAction: ConnectAction
}
