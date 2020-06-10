const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class MessageCheckAction extends action.Action {
  constructor(cookies, credentials_id, url) {
    super(cookies, credentials_id);

    // CONNECT URL
    this.url = url;
  }

  async messageCheck() {
    await super.gotoLogin();
    await super.gotoChecker(this.url);

    await super.close_msg_box(this.page);

    if (await this.page.$(selectors.WRITE_MSG_BTN_SELECTOR) === null) {
      console.log('You can\'t write messages to ' + this.url);
      return { message: '' }; // TODO: send (code = ...) here in result_data
    }

    await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR, { timeout: 5000 });

    await this.page.click(selectors.WRITE_MSG_BTN_SELECTOR);

    // wait selector here
    await super.check_success_selector(selectors.LAST_MSG_LINK_SELECTOR);

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
