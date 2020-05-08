const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class ScribeWorkAction {
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

  async scribe() {
    await this.gotoChecker(this.url);

    await this.autoScroll(this.page);
    let result = {};

    try {
      await this.page.waitForSelector(selectors.JOB_LINK_SELECTOR);
    } catch (err) {
      // if we cant find company informatiom
      return result;
    }

    let selector = selectors.JOB_LINK_SELECTOR;
    let link = await this.page.evaluate((selector) => {
      let a = document.querySelector(selector).href;
      return a;
    }, selector);

    if (link === null || typeof link === undefined) {
      console.log("..... link-null: .....", link)
      return result;
    }
    result.company_linkedin_page = link;

    await this.page.goto(link + '/about');
    try {
      await this.page.waitForSelector(selectors.JOB_SITE_SELECTOR);
    } catch (err) {
      // if we cant find company website on About page
      return result;
    }

    let job_link = undefined;
    selector = selectors.JOB_SITE_SELECTOR;
    await this.page.evaluate((selector) => {
      job_link = document.querySelector(selector).href;
    }, selector);

    //console.log("..... link: .....", link)
    if (typeof job_link === undefined || job_link === null) {
      console.log("..... job_link not found: .....", job_link)
      return result;
    }
    result.company_url = job_linkl
    console.log("..... result: .....", result)
    return result;
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

          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, 100);
      });
    });
  }

}

module.exports = {
  ScribeWorkAction: ScribeWorkAction
}
