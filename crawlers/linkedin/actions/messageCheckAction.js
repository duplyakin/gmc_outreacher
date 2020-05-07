const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class MessageCheckAction {
  constructor(email, password, cookies, url) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;

    // CONNECT URL
    this.url = url;
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

  async messageCheck() {
    await this.gotoChecker(this.url);

    try {
      await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR);

      // close messages box !!! (critical here)
      await this.page.waitFor(1000);  // wait linkedIn loading process
      await this.page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
      await this.page.waitFor(1000);  // wait linkedIn loading process

      await this.page.click(selectors.WRITE_MSG_BTN_SELECTOR);
      let mySelectors = {
        selector1: selectors.LAST_MSG_LINK_SELECTOR,
        selector2: selectors.LAST_MSG_SELECTOR,
      };
      let lastSender = await this.page.evaluate((mySelectors) => {
        let res = Array.from(document.querySelectorAll(mySelectors.selector1)).map(el => (el.href));
        let text = Array.from(document.querySelectorAll(mySelectors.selector2)).map(el => (el.innerText));
        return { res: res.pop(), text: text.pop() };
      }, mySelectors);

      if (lastSender.res === this.url) {
        console.log("..... new message: .....", lastSender)
        return lastSender.text;
      }

      console.log("..... NO new messages: .....", lastSender)
      return '';
    } catch (err) {
      throw MyExceptions.MessageCheckActionError(err);
    }
  }

}

module.exports = {
  MessageCheckAction: MessageCheckAction
}
