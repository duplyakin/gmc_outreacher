const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class MessageCheckAction extends action.Action {
  constructor(email, password, li_at, cookies, credentials_id, url) {
    super(email, password, li_at, cookies, credentials_id);

    // CONNECT URL
    this.url = url;
  }

  async messageCheck() {
    await super.gotoChecker(this.url);

    try {
      // close messages box !!! (critical here)
      await this.page.waitFor(1000);  // wait linkedIn loading process
      await this.page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
      await this.page.waitFor(1000);  // wait linkedIn loading process
    } catch (err) {
      console.log("..... CLOSE_MSG_BOX_SELECTOR not found .....");
    }

    if (await this.page.$(selectors.WRITE_MSG_BTN_SELECTOR) === null) {
      console.log('You can\'t write messages to ' + this.url);
      return { message: '' }; // TODO: send (code = ...) here in result_data
    }

    await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR, { timeout: 5000 });

    await this.page.click(selectors.WRITE_MSG_BTN_SELECTOR);
    let mySelectors = {
      selector1: selectors.LAST_MSG_LINK_SELECTOR,
      selector2: selectors.LAST_MSG_SELECTOR,
    };
    let lastSender = await this.page.evaluate((mySelectors) => {
      let res = Array.from(document.querySelectorAll(mySelectors.selector1)).map(el => (el.href));
      let text = Array.from(document.querySelectorAll(mySelectors.selector2)).map(el => (el.innerText));
      return { res: res.pop(), text: text.pop() };
    }, mySelectors);

    if (lastSender.res === this.url) {
      //console.log("..... new message: .....", lastSender);
      return { message: lastSender.text };
    }

    //console.log("..... NO new messages: .....", lastSender);
    return { message: '' };
  }

}

module.exports = {
  MessageCheckAction: MessageCheckAction
}
