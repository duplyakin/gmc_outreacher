const selectors = require(__dirname + "/.././selectors");
const action = require(__dirname + '/action.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class MessageCheckAction extends action.Action {
  constructor(email, password, cookies, url) {
    super(email, password, cookies);

    // CONNECT URL
    this.url = url;
  }

  async messageCheck() {
    await super.gotoChecker(this.url);

    await this.page.waitForSelector(selectors.WRITE_MSG_BTN_SELECTOR, { timeout: 5000 });

    // close messages box !!! (critical here)
    await this.page.waitFor(1000);  // wait linkedIn loading process
    await this.page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
    await this.page.waitFor(1000);  // wait linkedIn loading process

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
      console.log("..... new message: .....", lastSender)
      return lastSender.text;
    }

    console.log("..... NO new messages: .....", lastSender)
    return '';
  }

}

module.exports = {
  MessageCheckAction: MessageCheckAction
}
