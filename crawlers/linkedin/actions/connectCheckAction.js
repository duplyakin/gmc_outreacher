const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const links = require(__dirname + "/.././links");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class ConnectCheckAction {
  constructor(email, password, cookies, connectName) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;

    this.connectName = connectName;
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
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async closeBrowser(browser) {
    this.browser.close();
  }

  async connectCheck() {
    await this.gotoChecker(links.CONNECTS_LINK);

    await this.page.waitForSelector(selectors.SEARCH_CONNECTS_SELECTOR);

    await this.page.click(selectors.SEARCH_CONNECTS_SELECTOR);
    await this.page.keyboard.type(this.connectName);

    await this.page.waitForSelector(selectors.CONNECTOR_SELECTOR);
    await this.page.waitFor(1000);  // wait linkedIn loading process

    let selector = selectors.CONNECTOR_SELECTOR;
    let connect = await this.page.evaluate((selector) => {
      let a = document.querySelector(selector);
      if (a !== null) {
        a = a.innerText;
      };
      return a;
    }, selector);

    if (connect === this.connectName) {
      console.log("..... connect found - success: .....", connect)
      return true;
    }

    console.log("..... connect NOT found: .....", connect)
    return false;
  }
}

module.exports = {
  ConnectCheckAction: ConnectCheckAction
}
