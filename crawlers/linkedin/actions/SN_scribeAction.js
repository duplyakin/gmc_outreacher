const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class SN_ScribeAction extends action.Action {
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
    if(!current_url.includes(super.get_pathname(this.url)) || current_url.includes('contact-info')) {
      log.debug("ScribeAction: current_url was:", current_url)
      await super.gotoChecker(this.url)
      await this.page.waitFor(5000)
      log.debug("ScribeAction: current_url now:", this.page.url())
    }

    await super.autoScroll(this.page)

    // country
    selector_res = await super.check_success_selector(selectors.SN_LOCATION_SELECTOR)
    if(selector_res) {
      selector = selectors.SN_LOCATION_SELECTOR
      result.location = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // education
    selector_res = await super.check_success_selector(selectors.SN_EDUCATION_SELECTOR)
    if(selector_res) {
      selector = selectors.SN_EDUCATION_SELECTOR
      result.education = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // company informatiom
    // company name
    selector_res = await super.check_success_selector(selectors.SN_COMPANY_NAME_SELECTOR)
    if(selector_res) {
      selector = selectors.SN_COMPANY_NAME_SELECTOR
      result.company_name = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // job title
    selector_res = await super.check_success_selector(selectors.SN_JOB_SELECTOR)
    if(selector_res) {
      selector = selectors.SN_JOB_SELECTOR
      result.job_title = await this.page.evaluate((selector) => {
        return document.querySelector(selector).innerText
      }, selector)
    }

    // company linkedin page
    selector_res = await super.check_success_selector(selectors.SN_JOB_LINK_SELECTOR)
    if(selector_res && result.company_url == null) {
      selector = selectors.SN_JOB_LINK_SELECTOR
      result.company_linkedin_page = await this.page.evaluate((selector) => {
        return document.querySelector(selector).href
      }, selector)

      await super.gotoChecker(result.company_linkedin_page)

      // company website on About page
      selector_res = await super.check_success_selector(selectors.SN_JOB_SITE_SELECTOR)
      if(selector_res) {
        selector = selectors.SN_JOB_SITE_SELECTOR
        result.company_url = await this.page.evaluate((selector) => {
          return document.querySelector(selector).href
        }, selector)
      }
    }

    return result
  }


  async scribe_contact_info() {
    let result = {}
    let mySelector = ''
    log.debug("SN_ScribeAction: scribe_contact_info started")

    let selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_SELECTOR)
    if(!selector_res) {
      // can't find contact info selector
      log.debug("SN_ScribeAction: can't find contact info selector")
      return result
    }

    await this.page.$eval(selectors.SN_CONTACT_INFO_SELECTOR, elem => elem.click()) // page.click not working

    await this.page.waitFor(2000)

    // phone
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_PHONE_SELECTOR)
    if(selector_res) {
      mySelector = selectors.SN_CONTACT_INFO_PHONE_SELECTOR

      result.phone = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("SN_ScribeAction: phone added")
    }

    // address
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_ADDRESS_SELECTOR)
    if(selector_res) {
      mySelector = selectors.SN_CONTACT_INFO_ADDRESS_SELECTOR

      result.address = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("SN_ScribeAction: address added")
    }

    // email
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_EMAIL_SELECTOR)
    if(selector_res) {
      mySelector = selectors.SN_CONTACT_INFO_EMAIL_SELECTOR

      result.email = await this.page.evaluate((mySelector) => {
        return document.querySelector(mySelector).innerText
      }, mySelector)

      log.debug("SN_ScribeAction: email added")
    }

    // twitter
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_SOCIAL_SELECTOR)
    if(selector_res) {
      mySelector = selectors.SN_CONTACT_INFO_SOCIAL_SELECTOR

      let social = await this.page.evaluate((mySelector) => {
        let result = {}
        let elements = document.querySelectorAll(mySelector)

        if(elements != null && elements.length > 0) {

          for(let elem of elements) {
            if(elem.querySelector('span') != null && elem.querySelector('a') != null) {
              if(elem.querySelector('span').innerText.toLowerCase().includes('twitter')) {
                result.twitter = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('skype')) {
                result.skype = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('wechat')) {
                result.wechat = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('icq')) {
                result.icq = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('aim')) {
                result.aim = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('yahoo')) {
                result.yahoo = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('qq')) {
                result.qq = elem.querySelector('a').href
              }
              if(elem.querySelector('span').innerText.toLowerCase().includes('hangouts')) {
                result.hangouts = elem.querySelector('a').href
              }
            }
          }
        }

        return result
      }, mySelector)

      if(social != null) {
        if(social.twitter != null) {
          result.twitter = social.twitter
          log.debug("SN_ScribeAction: twitter added")
        }
        if(social.skype != null) {
          result.skype = social.skype
          log.debug("SN_ScribeAction: skype added")
        }
        if(social.wechat != null) {
          result.wechat = social.wechat
          log.debug("SN_ScribeAction: wechat added")
        }
        if(social.icq != null) {
          result.icq = social.icq
          log.debug("SN_ScribeAction: icq added")
        }
        if(social.aim != null) {
          result.aim = social.aim
          log.debug("SN_ScribeAction: aim added")
        }
        if(social.yahoo != null) {
          result.yahoo = social.yahoo
          log.debug("SN_ScribeAction: yahoo added")
        }
        if(social.qq != null) {
          result.qq = social.qq
          log.debug("SN_ScribeAction: qq added")
        }
        if(social.hangouts != null) {
          result.hangouts = social.hangouts
          log.debug("SN_ScribeAction: hangouts added")
        }
      }
    }

    // website
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_WEBSITE_SELECTOR)
    if(selector_res) {
      mySelector = selectors.SN_CONTACT_INFO_WEBSITE_SELECTOR

      let websites = await this.page.evaluate((mySelector) => {
        let result = {
          websites: []
        }
        let elements = document.querySelectorAll(mySelector)

        if(elements != null && elements.length > 0) {

          for(let elem of elements) {
            if(elem.querySelector('span') != null && elem.querySelector('a') != null) {
              if(elem.querySelector('span').innerText.toLowerCase().includes('company')) {
                result.company_url = elem.querySelector('a').href
              }else if (elem.querySelector('span').innerText.toLowerCase().includes('blog')) {
                result.websites.push({ blog: elem.querySelector('a').href })
              } else if (elem.querySelector('span').innerText.toLowerCase().includes('personal')) {
                result.websites.push({ personal: elem.querySelector('a').href })
              } else if (elem.querySelector('span').innerText.toLowerCase().includes('rssfeed')) {
                result.websites.push({ rssfeed: elem.querySelector('a').href })
              } else if (elem.querySelector('span').innerText.toLowerCase().includes('portfolio')) {
                result.websites.push({ portfolio: elem.querySelector('a').href })
              } else {
                result.websites.push({ other: elem.querySelector('a').href })
              }
            }
          }
        }

        return result
      }, mySelector)

      if(websites != null) {
        if(websites.company_url != null) {
          result.company_url = websites.company_url
          log.debug("SN_ScribeAction: company_url added")
        }
        if(websites.websites != null) {
          result.websites = websites.websites
          log.debug("SN_ScribeAction: websites added")
        }
      }

      log.debug("SN_ScribeAction: website added")
    }


    // close contact info popup
    selector_res = await super.check_success_selector(selectors.SN_CONTACT_INFO_CLOSE_SELECTOR)
    if(selector_res) {
      await this.page.click(selectors.SN_CONTACT_INFO_CLOSE_SELECTOR)
    } else {
      await super.gotoChecker(this.url)
    }

    await this.page.waitFor(5000)

    log.debug("SN_ScribeAction: contact info scribed:", result)
    return result
  }
}

module.exports = {
  SN_ScribeAction: SN_ScribeAction
}
