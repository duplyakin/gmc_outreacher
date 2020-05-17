const selectors = require(__dirname + "/.././selectors");
const action = require(__dirname + '/action.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class ScribeAction extends action.Action {
  constructor(email, password, cookies, url) {
    super(email, password, cookies);

    this.url = url;
  }

  async scribe() {
    await super.gotoChecker(this.url);

    await super.autoScroll(this.page);
    let result = {};

    try {
      await this.page.waitForSelector(selectors.JOB_LINK_SELECTOR, { timeout: 5000 });
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
      await this.page.waitForSelector(selectors.JOB_SITE_SELECTOR, { timeout: 5000 });
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
    if (job_link === undefined || job_link === null) {
      console.log("..... job_link not found: .....", job_link)
      console.log("..... result: .....", result);
      return result;
    }
    result.company_url = job_link;
    console.log("..... result: .....", result);
    return result;
  }
}

module.exports = {
  ScribeAction: ScribeAction
}
