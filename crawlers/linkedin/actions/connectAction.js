const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class ConnectAction {
  constructor(email, password, cookies, url, template, data) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;

    this.url = url;
    this.template = template;
    this.data = data;
  }

  // do 1 trie to connect URL or goto login
  async gotoChecker(url) {
    await this.page.goto(url);
    let current_url = await this.page.url();
    if (current_url.includes('login') || current_url.includes('signup')) {
      let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
      await loginAction.setContext(this.context);
      let result = await loginAction.login();
      if (!result) {
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
    this.browser.disconnect();
    this.browser.close();
  }

  async connect() {
    await this.gotoChecker(this.url);

    // close messages box !!! critical here?
    await this.page.waitFor(1000);  // wait linkedIn loading process
    await this.page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
    await this.page.waitFor(1000);  // wait linkedIn loading process

    //await this.page.waitForSelector(selectors.CONNECT_SELECTOR);
    if (await this.page.$(selectors.CONNECT_SELECTOR) === null) {
      console.log('You can\'t contact ' + this.url);

      // TODO: add logic for FOLLOW-UP (for famous contacts) and MESSAGE (for premium acc's)
      return false;
    }
    await this.page.click(selectors.CONNECT_SELECTOR);

    // check - if CONNECT btm exist, but muted, then you have already sent request
    //await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    if (await this.page.$(selectors.ADD_MSG_BTN_SELECTOR) === null) {
      console.log('You have already sent request to ' + this.url);
      return true;
    }
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    await this.page.waitForSelector(selectors.MSG_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);

    let text = this.formatMessage();

    await this.page.keyboard.type(text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
    //await this.page.waitFor(100000); // to see result

    return true;
  }

  formatMessage() {
    // format template
    let str = this.template;
    for (var obj in this.data) {
      str = str.replace(new RegExp('{' + obj + '}', 'g'), this.data[obj]);
    }
    str = str.replace(new RegExp('\{(.*?)\}', 'g'), '');
    return str;
  }
}

module.exports = {
  ConnectAction: ConnectAction
}
