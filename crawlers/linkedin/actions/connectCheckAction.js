const selectors = require(__dirname + "/.././selectors");
const links = require(__dirname + "/.././links");
const action = require(__dirname + '/action.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class ConnectCheckAction extends action.Action {
  constructor(email, password, cookies, connectName) {
    super(email, password, cookies);

    this.connectName = connectName;
  }

  async connectCheck() {
    await super.gotoChecker(links.CONNECTS_LINK);

    await this.page.waitForSelector(selectors.SEARCH_CONNECTS_SELECTOR, { timeout: 5000 });

    await this.page.click(selectors.SEARCH_CONNECTS_SELECTOR);
    await this.page.keyboard.type(this.connectName);

    await this.page.waitForSelector(selectors.CONNECTOR_SELECTOR, { timeout: 5000 });
    await this.page.waitFor(1000);  // wait linkedIn loading process

    let selector = selectors.CONNECTOR_SELECTOR;
    let connect = await this.page.evaluate((selector) => {
      let a = document.querySelector(selector);
      if (a !== null) {
        a = a.innerText;
      };
      return a;
    }, selector);

    if (connect === this.connectName) {
      console.log("..... connect found - success: .....", connect)
      return true;
    }

    console.log("..... connect NOT found: .....", connect)
    return false;
  }
}

module.exports = {
  ConnectCheckAction: ConnectCheckAction
}
