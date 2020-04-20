const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

class MessageCheckAction {
  constructor(email, password, cookies, url) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;

    this.url = url;
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

  async messageCheck() {
    await this.gotoChecker(this.url);
    await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR);

    await this.page.click(selectors.WRITE_MSG_BTN_SELECTOR);
    let selector = selectors.LAST_MSG_SELECTOR;
    let lastSender = await this.page.evaluate((selector) => {
        let a = Array.from(document.querySelectorAll(selector)).map(el => (el.href));
        return a.pop();
    }, selector);

   if(lastSender === this.url) {
     console.log("..... new message: .....", lastSender)
     return true;
   }

    console.log("..... NO new messages: .....", lastSender)
    return false;
  }
}

module.exports = {
    MessageCheckAction: MessageCheckAction
}
