const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class ScribeAction extends action.Action {
  constructor(cookies, credentials_id, url) {
    super(cookies, credentials_id);

    this.url = url;
  }

  async scribe() {
    await super.gotoLogin();
    await super.gotoChecker(this.url);

    await super.autoScroll(this.page);

    let result = {};
    let country = null;
    let company_website = null;
    let education = null;

    let selector = selectors.COUNTRY_SELECTOR;

    try {
      await this.page.waitForSelector(selectors.COUNTRY_SELECTOR, { timeout: 5000 });

      country = await this.page.evaluate((selector) => {
        let res = document.querySelector(selector).innerText;
        return res;
      }, selector);

    } catch(err) {
      log.debug("ScribeAction: empty country for this profile: ", this.url)
    }

    if(country){
      result.country = country;
    }

    let mySelectors = {
       selector1: selectors.JOB_LINK_SELECTOR,
       selector2: selectors.JOB_SELECTOR,
       selector3: selectors.EDUCATION_SELECTOR,
    };

    try {
      await this.page.waitForSelector(selectors.JOB_LINK_SELECTOR, { timeout: 5000 });
      await this.page.waitForSelector(selectors.JOB_SELECTOR, { timeout: 5000 });
      
    } catch (err) {
      // if we cant find company informatiom
      return result;
    }

    let scribe_result = await this.page.evaluate((mySelectors) => {
      let res = {};

      res.link = document.querySelector(mySelectors.selector1).href;
      res.job_title = document.querySelector(mySelectors.selector1).querySelector(mySelectors.selector2).innerText;

      //log.debug("ScribeAction: job:", res);
      return res;
    }, mySelectors);

    if(scribe_result.job_title) {
      result.job_title = scribe_result.job_title;
    }

    try {
      await this.page.waitForSelector(selectors.EDUCATION_SELECTOR, { timeout: 5000 });
      
      selector = selectors.EDUCATION_SELECTOR;

      education = await this.page.evaluate((selector) => {
        let education = document.querySelector(selector).innerText;
  
        return education;
      }, selector);

    } catch (err) {
      // education not found
    }

    if(education) {
      result.education = education;
    }

    if (!scribe_result.link) {
      // company don't have linkedin page -> we can't continue scribe
      //log.debug("ScribeAction: company_linkedin_page is null: ", link)
      return result;
    }
    result.company_linkedin_page = scribe_result.link;

    await super.gotoChecker(scribe_result.link + 'about/');

    try {
      await this.page.waitForSelector(selectors.JOB_SITE_SELECTOR, { timeout: 5000 });
    } catch (err) {
      // if we cant find company website on About page
      return result;
    }

    selector = selectors.JOB_SITE_SELECTOR;
    company_website = await this.page.evaluate((selector) => {
      res = document.querySelector(selector).innerText;
      return res;
    }, selector);

    //log.debug("ScribeAction: company_website: ", company_website)
    if (!company_website) {
      //log.debug("ScribeAction: company_website not found: ", company_website)
      //log.debug("ScribeAction: result: ", result);
      return result;
    }

    result.company_url = company_website;
    //log.debug("ScribeAction: result: ", result);
    return result;
  }
}

module.exports = {
  ScribeAction: ScribeAction
}
