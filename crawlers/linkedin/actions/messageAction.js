const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class MessageAction extends action.Action {
  constructor(email, password, cookies, credentials_id, url, data, template) {
    super(email, password, cookies, credentials_id);

    this.url = url;
    this.data = data;
    this.template = template;
  }

  async message() {
    await super.gotoChecker(this.url);

    const page = await this.context.newPage();  // feature (critical)
    await page.goto(this.url);

    //TODO: add logic for 'closed' for message accounts

    try {
      // close messages box !!! (not critical here, but XZ ETOT LINKED)
      await page.waitFor(1000);  // wait linkedIn loading process
      await page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
      await page.waitFor(1000);  // wait linkedIn loading process
    } catch (err) {
      console.log("..... CLOSE_MSG_BOX_SELECTOR not found .....")
    }

    if (await this.page.$(selectors.WRITE_MSG_BTN_SELECTOR) === null) {
      console.log('You can\'t write messages to ' + this.url);
      return false; 
    }

    await page.waitForSelector(selectors.MSG_BOX_SELECTOR, { timeout: 5000 });
    await page.click(selectors.MSG_BOX_SELECTOR);

    let text = super.formatMessage(this.template, this.data);

    await page.keyboard.type(text);
    await page.waitForSelector(selectors.SEND_MSG_BTN_SELECTOR, { timeout: 5000 });
    await page.waitFor(1000); // wait untill SEND button become active
    await page.click(selectors.SEND_MSG_BTN_SELECTOR);
    //await page.waitFor(100000); // to see result

    return true;
  }
}

module.exports = {
  MessageAction: MessageAction
}
