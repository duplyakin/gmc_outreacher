const selectors = require("../selectors");
const action = require('./action.js');
const utils = require("./utils");

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class ScribeAction extends action.Action {
  constructor(cookies, credentials_id, url) {
    super(cookies, credentials_id)

    this.url = url
  }

  async scribe() {
    await super.gotoChecker(this.url)

    let result = {}
    let selector = ''
    let selector_res = false

    result = await this.scribe_contact_info()

    // check current url here
    let current_url = this.page.url()
    if(!current_url.includes(utils.get_pathname_url(this.url)) || current_url.includes('contact-info')) {
      log.debug("ScribeAction: current_url was:", current_url)
      await super.gotoChecker(this.url)
      await this.page.waitFor(5000)
      log.debug("ScribeAction: current_url now:", this.page.url())
    }

    await utils.autoScroll(this.page)

    // location
    selector_res = await utils.check_success_selector(selectors.COUNTRY_SELECTOR, this.page)
    if(selector_res) {
      selector = selectors.COUNTRY_SELECTOR
      result.location = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // SN link
    selector_res = await utils.check_success_selector(selectors.LINK_TO_SN_SELECTOR, this.page)
    if(selector_res) {
      selector = selectors.LINK_TO_SN_SELECTOR
      let linkedin_sn = await this.page.evaluate((selector) => {
        return document.querySelector(selector).href
      }, selector)

      if(linkedin_sn.includes('sales')) {
        if(utils.get_search_url(linkedin_sn) != '') {
          result.linkedin_sn = linkedin_sn.split(utils.get_search_url(linkedin_sn))[0]
        } else {
          result.linkedin_sn = linkedin_sn
        }
      } else {
        log.debug("ScribeAction: wrong linkedin_sn format:", linkedin_sn)
      }
    }
    /*
    let linkedin_sn = await this.page.evaluate(() => {
      let elems = document.querySelectorAll('code')
      for(let el of elems) {
        try {
          let res = JSON.parse(el.innerText)
          if(res.hasOwnProperty('flagshipProfileUrl')) {
            return res.flagshipProfileUrl
          }
        } catch(err) {}
      }
    })

    if(linkedin_sn != null) {
      if(utils.get_search_url(linkedin_sn) != '') {
        result.linkedin_sn = linkedin_sn.split(utils.get_search_url(linkedin_sn))[0]
      } else {
        result.linkedin_sn = linkedin_sn
      }
    }*/

    // education
    selector_res = await utils.check_success_selector(selectors.EDUCATION_SELECTOR, this.page)
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
       selector3: selectors.COMPANY_NAME_SELECTOR,
    }

    // company linkedin page
    selector_res = await utils.check_success_selector(selectors.JOB_LINK_SELECTOR, this.page)
    if(selector_res) {
      result.company_linkedin_page = await this.page.evaluate((mySelectors) => {
        return document.querySelector(mySelectors.selector1).href
      }, mySelectors)

      // job title
      selector_res = await utils.check_success_selector(selectors.JOB_SELECTOR, this.page)
      if(selector_res) {
        result.job_title = await this.page.evaluate((mySelectors) => {
          return document.querySelector(mySelectors.selector1).querySelector(mySelectors.selector2).innerText
        }, mySelectors)
      }

      // company name
      selector_res = await utils.check_success_selector(selectors.COMPANY_NAME_SELECTOR, this.page)
      if(selector_res) {
        result.company_name = await this.page.evaluate((mySelectors) => {
          return document.querySelector(mySelectors.selector1).querySelector(mySelectors.selector3).innerText
        }, mySelectors)
      }

      await super.gotoChecker(result.company_linkedin_page + 'about/')

      // company website on About page
      selector_res = await utils.check_success_selector(selectors.JOB_SITE_SELECTOR, this.page)
      if(selector_res) {
        selector = selectors.JOB_SITE_SELECTOR
        result.company_url = await this.page.evaluate((selector) => {
          return document.querySelector(selector).innerText
        }, selector)
      }
    }

    log.debug("ScribeAction: result:", result)
    return result
  }


  async scribe_contact_info() {
    let result = {}
    let mySelector = ''
    log.debug("ScribeAction: scribe_contact_info started")

    await super.gotoChecker(this.page.url() + 'detail/contact-info/')
    await this.page.waitFor(5000)

    if(!this.page.url().includes('contact-info')) {  
      return result
    }

    // websites
    let selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_WEBSITE_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_WEBSITE_SELECTOR

      let websites = await this.page.evaluate((mySelector) => {
        let result = []
        let website_elements = document.querySelectorAll(mySelector)
        if(website_elements != null) {
          for(let el of website_elements) {
            if(el != null && el.href != null) {
              result.push( el.href )
            }
          }
        }
        return result
      }, mySelector)

      if(websites != null && websites.length > 0) {
        result.websites = websites

        log.debug("ScribeAction: websites added")
      }
    }

    // phone
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_PHONE_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_PHONE_SELECTOR

      result.phone = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: phone added")
    }

    // address
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_ADDRESS_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_ADDRESS_SELECTOR

      result.address = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: address added")
    }

    // email
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_EMAIL_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_EMAIL_SELECTOR

      result.emails = await this.page.evaluate((mySelector) => {
        let emails = []
        let elements = document.querySelectorAll(mySelector)
        for(let elem of elements) {
          emails.push(elem.innerText)
        }

        return emails

      }, mySelector)

      log.debug("ScribeAction: emails added")
    }

    // twitter
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_TWITTER_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_TWITTER_SELECTOR

      result.twitter = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: twitter added")
    }

    // IM
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_IM_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_IM_SELECTOR

      result.im = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: im added")
    }

    // birthday
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_BIRTHDAY_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_BIRTHDAY_SELECTOR

      result.birthday = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: birthday added")
    }

    // connected date
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_CONNECTED_DATE_SELECTOR, this.page)
    if(selector_res) {
      mySelector = selectors.CONTACT_INFO_CONNECTED_DATE_SELECTOR

      result.connected_date = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("ScribeAction: connected date added")
    }

    // close contact info popup
    selector_res = await utils.check_success_selector(selectors.CONTACT_INFO_CLOSE_SELECTOR, this.page)
    if(selector_res) {
      await this.page.click(selectors.CONTACT_INFO_CLOSE_SELECTOR)
    } else {
      await super.gotoChecker(this.url)
    }

    await this.page.waitFor(5000)

    //log.debug("ScribeAction: contact info scribed:", result)
    return result
  }
}

module.exports = {
  ScribeAction: ScribeAction
}
