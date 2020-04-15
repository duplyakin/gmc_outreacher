const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");
const links = require(__dirname + "/./links");

class ConnectCheckAction {
  constructor(connectName, cookies) {
    this.connectName = connectName;

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

  async connectCheck() {
    await this.page.goto(links.CONNECTS_LINK);
    await this.page.waitForSelector(selectors.SEARCH_CONNECTS_SELECTOR);

    await this.page.click(selectors.SEARCH_CONNECTS_SELECTOR);
    await this.page.keyboard.type(this.connectName);

    await this.page.waitForSelector(selectors.CONNECTOR_SELECTOR);
    await this.page.waitFor(1000);  // wait linkedIn loading process
    let connect = await this.page.evaluate((selectors.CONNECTOR_SELECTOR) => {
      let a = document.querySelector(selectors.CONNECTOR_SELECTOR);
      if(a !== null) {
        a = a.innerText;
      };
      return a;
    }, selectors.CONNECTOR_SELECTOR);

   if(connect === this.connectName) {
     console.log("..... connect found - success: .....", connect)
     return true;
   }

    console.log("..... connect NOT found: .....", connect)
    return false;
  }
}
