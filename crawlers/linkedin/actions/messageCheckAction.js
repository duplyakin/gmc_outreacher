const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

class MessageCheckAction {
  constructor(url, cookies) {
    this.url = url;

    //this.cookies = JSON.parse(cookies);
    this.cookies = cookies;

    // check cookies
    if(this.cookies !== undefined || this.cookies !== null) {
      this.cookies.forEach((item) => {
        if(item.name === 'li_at') {
          if(Date.now() / 1000 > item.expires) {
            let loginAction = new LoginAction(email, password, cookies);
            loginAction.login();
          }
        }
      });
    } else {
      let loginAction = new LoginAction(email, password, cookies);
      loginAction.login();
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

  async messageCheck() {
    await this.page.goto(this.url);
    await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR);

    await this.page.click(selectors.WRITE_MSG_BTN_SELECTOR);
    let lastSender = await this.page.evaluate((selectors.LAST_MSG_SELECTOR) => {
        let a = Array.from(document.querySelectorAll(selectors.LAST_MSG_SELECTOR)).map(el => (el.href));
        return a.pop();
    }, selectors.LAST_MSG_SELECTOR);

   if(lastSender === url) {
     console.log("..... new message: .....", lastSender)
     return true;
   }

    console.log("..... NO new messages: .....", lastSender)
    return false;
  }
}
