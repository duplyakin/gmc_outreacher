const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

class ScribeWorkAction {
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

  async scribe() {
    await this.page.goto(this.url);
    //await page.waitForNavigation();

    await autoScroll(this.page);
    await this.page.waitForSelector(selectors.JOB_LINK_SELECTOR);

    let link = await this.page.evaluate((selectors.JOB_LINK_SELECTOR) => {
      let a = document.querySelector(selectors.JOB_LINK_SELECTOR).href;
      return a;
    }, selectors.JOB_LINK_SELECTOR);

    if(link === null || link === undefined) {
      console.log("..... link-null: .....", link)
      return false;
    }

    await this.page.goto(link + '/about');
    //await page.waitForNavigation();
    await this.page.waitForSelector(selectors.JOB_SITE_SELECTOR);

    await this.page.evaluate((selectors.JOB_SITE_SELECTOR) => {
      link = document.querySelector(selectors.JOB_SITE_SELECTOR).href;
    }, selectors.JOB_SITE_SELECTOR);

    //console.log("..... link: .....", link)
    return true;
  }

  async autoScroll(page) {
      await page.evaluate(async () => {
          await new Promise((resolve, reject) => {
              var totalHeight = 0;
              var distance = 100;
              var timer = setInterval(() => {
                  var scrollHeight = document.body.scrollHeight;
                  window.scrollBy(0, distance);
                  totalHeight += distance;

                  if(totalHeight >= scrollHeight) {
                      clearInterval(timer);
                      resolve();
                  }
              }, 100);
          });
      });
  }

}
