const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

export class ConnectAction {
  constructor(connecthUrl, text, cookies) {
    this.connecthUrl = connecthUrl;
    this.text = text;

    this.cookies = JSON.parse(cookies);
  }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await page.setCookie(...this.cookies);
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function connect() {
    await this.page.goto(this.connecthUrl);
    await this.page.click(selectors.CONNECT_SELECTOR);
    //await page.waitForNavigation();
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);
    await this.page.keyboard.type(this.text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
  }
}
