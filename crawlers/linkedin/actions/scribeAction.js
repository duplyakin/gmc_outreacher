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
    await super.gotoChecker(this.url)

    let result = {}
    let selector = ''
    let selector_res = false

    result = await this.scribe_contact_info()

    // check current url here
    let current_url = this.page.url()
    if(!current_url.includes(super.get_pathname(this.url)) || current_url.includes('contact-info')) {
      log.debug("ScribeAction: current_url was:", current_url)
      await super.gotoChecker(this.url)
      await this.page.waitFor(5000)
      log.debug("ScribeAction: current_url now:", this.page.url())
    }

    await super.autoScroll(this.page)

    // country
    selector_res = await super.check_success_selector(selectors.COUNTRY_SELECTOR)
    if(selector_res) {
      selector = selectors.COUNTRY_SELECTOR
      result.country = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // education
    selector_res = await super.check_success_selector(selectors.EDUCATION_SELECTOR)
    if(selector_res) {
      selector = selectors.EDUCATION_SELECTOR
      result.education = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // company informatiom
    let mySelectors = {
       selector1: selectors.JOB_LINK_SELECTOR,
       selector2: selectors.JOB_SELECTOR,
    }

    // company linkedin page
    selector_res = await super.check_success_selector(selectors.JOB_LINK_SELECTOR)
    if(selector_res) {
      result.company_linkedin_page = await this.page.evaluate((mySelectors) => {
        return document.querySelector(mySelectors.selector1).href
      }, mySelectors)

      // job title
      selector_res = await super.check_success_selector(selectors.JOB_SELECTOR)
      if(selector_res) {
        result.job_title = await this.page.evaluate((mySelectors) => {
          return document.querySelector(mySelectors.selector1).querySelector(mySelectors.selector2).innerText
        }, mySelectors)
      }

      await super.gotoChecker(result.company_linkedin_page + 'about/')

      // company website on About page
      selector_res = await super.check_success_selector(selectors.JOB_SITE_SELECTOR)
      if(selector_res) {
        selector = selectors.JOB_SITE_SELECTOR
        result.company_url = await this.page.evaluate((selector) => {
          return document.querySelector(selector).innerText
        }, selector)
      }
    }

    return result
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
    
    await this.page.click(selectors.CONTACT_INFO_SELECTOR) // don't work
    await this.page.waitFor(5000) // XZ etot linked
    */

    await super.gotoChecker(this.page.url() + 'detail/contact-info/')
    await this.page.waitFor(5000)

    if(!this.page.url().includes('contact-info')) {
      super.gotoChecker(this.url)
      await this.page.waitFor(5000)
      
      return result
    }

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
      await this.page.click(selectors.CONTACT_INFO_CLOSE_SELECTOR)
    } else {
      super.gotoChecker(this.url)
    }

    this.page.waitFor(5000)

    log.debug("ScribeAction: contact info scribed:", result)
    return result
  }
}

module.exports = {
  ScribeAction: ScribeAction
}
