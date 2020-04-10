const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

export class ConnectAction {
  constructor(connecthUrl, text, cookies) {
    this.connecthUrl = connecthUrl;
    this.text = text;

    this._cookies = cookies;
  }

  cookies() {
      return this._cookies
    }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function connect() {
    const page = await this.context.newPage();

    await page.goto(url);
    await page.click(selectors.CONNECT_SELECTOR);
    //await page.waitForNavigation();
    await page.click(selectors.ADD_MSG_BTN_SELECTOR);
    await page.click(selectors.MSG_SELECTOR);
    await page.keyboard.type(this.text);
    await page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
  }
}
