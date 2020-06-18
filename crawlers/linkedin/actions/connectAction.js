const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class ConnectAction extends action.Action {
  constructor(cookies, credentials_id, url, template, data) {
    super(cookies, credentials_id);

    this.url = url;
    this.template = template;
    this.data = data;
  }

  async connect() {
    await super.gotoLogin();
    await super.gotoChecker(this.url);

    let check = await this.connectCheck();
    if(check) {
      log.debug('ConnectAction: You are already connected with ' + this.url);
      return true;
    }

    await super.close_msg_box(this.page);

    //await this.page.waitForSelector(selectors.CONNECT_SELECTOR);
    if (await this.page.$(selectors.CONNECT_SELECTOR) === null) {
      log.debug('ConnectAction: You can\'t connect ' + this.url);

      // TODO: add logic for FOLLOW-UP (for famous contacts) and MESSAGE (for premium acc's)
      return false;
    }
    await this.page.click(selectors.CONNECT_SELECTOR);

    // check - if CONNECT btm exists, but muted, then you have already sent request
    //await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    if (await this.page.$(selectors.ADD_MSG_BTN_SELECTOR) === null) {
      log.debug('ConnectAction: You have already sent request (or you can\'t) ' + this.url);
      return true;
    }
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    // wait selector here
    await super.check_success_selector(selectors.MSG_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);

    let text = super.formatMessage(this.template, this.data);

    await this.page.keyboard.type(text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);

    // wait page here
    await this.page.waitFor(2000);
    await super.check_success_page(this.url);

    return true;
  }

  async connectCheck() {
    // wait selector here
    let check_selector = await super.check_success_selector(selectors.CONNECT_DEGREE_SELECTOR)
    if(!check_selector) {
      log.debug("ConnectAction: connection NOT found (selector not foumd):", this.url)
      return false
    }

    await this.page.waitFor(1000);  // wait linkedIn loading process

    let selector = selectors.CONNECT_DEGREE_SELECTOR;
    let connect = await this.page.evaluate((selector) => {

      let a = document.querySelector(selector)

      if (a != null) {
        return a.innerText
      } else {
        return null
      }
    }, selector)

    if (connect == null || connect == '') {
      log.debug("ConnectAction: connection NOT found (selector result is NULL or empty):", this.url)
      return false

    } else if (connect.includes("1")) {
      log.debug("ConnectAction: connection found - success:", connect)
      return true
    }

    log.debug("ConnectAction: connection NOT found (not 1st degree):", connect + " for " + this.url)
    return false
  }
}

module.exports = {
  ConnectAction: ConnectAction
}
