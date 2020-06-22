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
    await super.gotoLogin()
    await super.gotoChecker(this.url)

    let result = {}
    let country = null
    let company_website = null
    let education = null

    let selector = selectors.COUNTRY_SELECTOR

    result = await this.scribe_contact_info()

    await super.autoScroll(this.page)

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
      return result
    }

    let scribe_result = await this.page.evaluate((mySelectors) => {
      let res = {}

      res.link = document.querySelector(mySelectors.selector1).href
      res.job_title = document.querySelector(mySelectors.selector1).querySelector(mySelectors.selector2).innerText

      return res
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


  async scribe_contact_info() {
    let result = {}
    let mySelector = ''
    log.debug("ScribeAction: scribe_contact_info started")

    let selector_res = ''
    /*
    let selector_res = await super.check_success_selector(selectors.CONTACT_INFO_SELECTOR)
    if(!selector_res) {
      // can't find contact info selector
      return result
    }
    */

    await super.gotoChecker(this.page.url() + 'detail/contact-info/')
    await this.page.waitFor(5000)

    if(!this.page.url().includes('contact-info')) {
      super.gotoChecker(this.url)
      await this.page.waitFor(5000)
      
      return result
    }

    await this.page.click(selectors.CONTACT_INFO_SELECTOR)
    await this.page.waitFor(5000) // XZ etot linked

    // phone
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_PHONE_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_PHONE_SELECTOR

      result.phone = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: phone added")
    }

    // address
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_ADDRESS_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_ADDRESS_SELECTOR

      result.address = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: address added")
    }

    // email
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_EMAIL_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_EMAIL_SELECTOR

      result.email = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: email added")
    }

    // twitter
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_TWITTER_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_TWITTER_SELECTOR

      result.twitter = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: twitter added")
    }

    // IM
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_IM_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_IM_SELECTOR

      result.im = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: im added")
    }

    // birthday
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_BIRTHDAY_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_BIRTHDAY_SELECTOR

      result.birthday = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: birthday added")
    }

    // connected date
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_CONNECTED_DATE_SELECTOR)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_CONNECTED_DATE_SELECTOR

      result.connected_date = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: connected date added")
    }

    // close contact info popup
    selector_res = await super.check_success_selector(selectors.CONTACT_INFO_CLOSE_SELECTOR)
    if(selector_res) {
      this.page.click(selectors.CONTACT_INFO_CLOSE_SELECTOR)
    } else {
      super.gotoChecker(this.url)
    }

    this.page.waitFor(2000)

    log.debug("ScribeAction: contact info scribed:", result)
    return result
  }
}

module.exports = {
  ScribeAction: ScribeAction
}
