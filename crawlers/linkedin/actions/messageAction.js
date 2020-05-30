const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class MessageAction extends action.Action {
  constructor(email, password, li_at, cookies, credentials_id, url, data, template) {
    super(email, password, li_at, cookies, credentials_id);

    this.url = url;
    this.data = data;
    this.template = template;
  }

  async message() {
    await super.gotoChecker(this.url);

    const page = await this.context.newPage();  // feature (critical)
    await page.goto(this.url); // add gotoChecker here ?

    //TODO: add logic for 'closed' for message accounts

    await super.close_msg_box(page);

    if (await this.page.$(selectors.WRITE_MSG_BTN_SELECTOR) === null) {
      console.log('You can\'t write messages to ' + this.url);
      return false; 
    }

    await page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR, { timeout: 5000 });
    await page.click(selectors.WRITE_MSG_BTN_SELECTOR);

    let text = super.formatMessage(this.template, this.data);

    try {
      await page.waitForSelector(selectors.SEND_MSG_BTN_SELECTOR, { timeout: 5000 });
    } catch (err) {
      await super.error_handler(err);
    }

    await page.keyboard.type(text);
    await page.waitForSelector(selectors.SEND_MSG_BTN_SELECTOR, { timeout: 5000 });
    await page.waitFor(2000); // wait untill SEND button become active
    await page.click(selectors.SEND_MSG_BTN_SELECTOR);
    //await page.waitFor(100000); // to see result

    await super.error_handler('Check message');

    return true;
  }
}

module.exports = {
  MessageAction: MessageAction
}
