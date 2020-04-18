const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

class ConnectAction {
  constructor(connectUrl, text, cookies) {
    this.connectUrl = connectUrl;
    this.text = text;

    //this.cookies = JSON.parse(cookies);
    this.cookies = cookies;

    // check cookies
    if(this.cookies !== undefined || this.cookies !== null) {
      this.cookies.forEach((item) => {
        if(item.name === 'li_at') {
          if(Date.now() / 1000 > item.expires) {
            let loginAction = new LoginAction(email, password, cookies);
            await loginAction.startBrowser();
            await loginAction.login();
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

  async connect() {
    await this.page.goto(this.connectUrl);
    await this.page.waitForNavigation();

    await this.page.click(selectors.CONNECT_SELECTOR);

    await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    await this.page.waitForSelector(selectors.MSG_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);

    await this.page.keyboard.type(this.text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
  }
}
