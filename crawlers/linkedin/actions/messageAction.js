const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class MessageAction {
  constructor(email, password, cookies, url, data, template) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;

    this.url = url;
    this.data = data;
    this.template = template;
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
    this.browser.close();
  }

  async message() {
    await this.gotoChecker(this.url);

    const page = await this.context.newPage();  // feature (critical)
    await page.goto(this.url);
    //TODO: add logic for 'closed' for message accounts

    // close messages box !!! (not critical here, but XZ ETOT LINKED)
    await page.waitFor(1000);  // wait linkedIn loading process
    await page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
    await page.waitFor(1000);  // wait linkedIn loading process

    await page.click(selectors.WRITE_MSG_BTN_SELECTOR);

    await page.waitForSelector(selectors.MSG_BOX_SELECTOR);
    await page.click(selectors.MSG_BOX_SELECTOR);

    let text = this.formatMessage();

    await page.keyboard.type(text);
    await page.waitForSelector(selectors.SEND_MSG_BTN_SELECTOR);
    await page.waitFor(1000); // wait untill SEND button become active
    await page.click(selectors.SEND_MSG_BTN_SELECTOR);
    //await page.waitFor(100000); // to see result

    return true;
  }

  formatMessage() {
    // format template
    return this.template;
  }
}

module.exports = {
  MessageAction: MessageAction
}
