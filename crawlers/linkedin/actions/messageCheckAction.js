const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

export class MessageCheckAction {
  constructor(url, cookies) {
    this.url = url;

    this.cookies = JSON.parse(cookies);
  }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function messageCheck() {
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
