const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class ConnectAction extends action.Action {
  constructor(email, password, li_at, cookies, credentials_id, url, template, data) {
    super(email, password, li_at, cookies, credentials_id);

    this.url = url;
    this.template = template;
    this.data = data;
  }

  async connect() {
    await super.gotoChecker(this.url);

    await super.close_msg_box(this.page);

    //await this.page.waitForSelector(selectors.CONNECT_SELECTOR);
    if (await this.page.$(selectors.CONNECT_SELECTOR) === null) {
      console.log('You can\'t contact ' + this.url);

      // TODO: add logic for FOLLOW-UP (for famous contacts) and MESSAGE (for premium acc's)
      return false;
    }
    await this.page.click(selectors.CONNECT_SELECTOR);

    // check - if CONNECT btm exists, but muted, then you have already sent request
    //await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    if (await this.page.$(selectors.ADD_MSG_BTN_SELECTOR) === null) {
      console.log('You have already sent request to ' + this.url);
      return true;
    }
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    // wait selector here
    await super.check_success_selector(selectors.MSG_SELECTOR);
    await this.page.click(selectors.MSG_SELECTOR);

    let text = super.formatMessage(this.template, this.data);

    await this.page.keyboard.type(text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
    //await this.page.waitFor(100000); // to see result

    // wait page here
    await this.page.waitFor(2000);
    await super.check_success_page(this.url);

    return true;
  }
}

module.exports = {
  ConnectAction: ConnectAction
}
