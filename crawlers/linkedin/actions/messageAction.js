const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

class MessageAction {
  constructor(profileUrl, text, cookies) {
    this.profileUrl = profileUrl;
    this.text = text;

    this.cookies = JSON.parse(cookies);
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

  async message() {
    const page = await this.context.newPage();  // feature

    await page.goto(this.profileUrl);
    //await page.waitForNavigation();

    await page.click(selectors.WRITE_MSG_BTN_SELECTOR);

    await page.waitForSelector(selectors.MSG_BOX_SELECTOR);
    await page.click(selectors.MSG_BOX_SELECTOR);

    await page.keyboard.type(this.text);
    await page.waitForSelector(selectors.SEND_MSG_BTN_SELECTOR);
    await page.waitFor(1000); // wait untill SEND button become active
    await page.click(selectors.SEND_MSG_BTN_SELECTOR);
    //await page.waitFor(100000); // to see result
  }
}
