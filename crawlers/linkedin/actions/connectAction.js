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

    // close messages box !!! critical here?
    await this.page.waitFor(1000);  // wait linkedIn loading process
    await this.page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
    await this.page.waitFor(1000);  // wait linkedIn loading process

    //await this.page.waitForSelector(selectors.CONNECT_SELECTOR);
    if (await this.page.$(selectors.CONNECT_SELECTOR) === null) {
      console.log('You can\'t contact ' + this.url);

      // TODO: add logic for FOLLOW-UP (for famous contacts) and MESSAGE (for premium acc's)
      return false;
    }
    await this.page.click(selectors.CONNECT_SELECTOR);

    // check - if CONNECT btm exist, but muted, then you have already sent request
    //await this.page.waitForSelector(selectors.ADD_MSG_BTN_SELECTOR);
    if (await this.page.$(selectors.ADD_MSG_BTN_SELECTOR) === null) {
      console.log('You have already sent request to ' + this.url);
      return true;
    }
    await this.page.click(selectors.ADD_MSG_BTN_SELECTOR);

    await this.page.waitForSelector(selectors.MSG_SELECTOR, { timeout: 5000 });
    await this.page.click(selectors.MSG_SELECTOR);

    let text = super.formatMessage(this.template, this.data);

    await this.page.keyboard.type(text);
    await this.page.click(selectors.SEND_INVITE_TEXT_BTN_SELECTOR);
    //await this.page.waitFor(100000); // to see result

    return true;
  }
}

module.exports = {
  ConnectAction: ConnectAction
}
