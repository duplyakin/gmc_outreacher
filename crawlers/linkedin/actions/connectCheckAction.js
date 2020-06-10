const selectors = require("../selectors");
const links = require("../links");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class ConnectCheckAction extends action.Action {
  constructor(cookies, credentials_id, prospect_full_name) {
    super(cookies, credentials_id);

    this.prospect_full_name = prospect_full_name;
  }

  async connectCheck() {
    await super.gotoChecker(links.CONNECTS_LINK);

    await this.page.waitForSelector(selectors.SEARCH_CONNECTS_SELECTOR, { timeout: 5000 });

    await this.page.click(selectors.SEARCH_CONNECTS_SELECTOR);
    await this.page.keyboard.type(this.prospect_full_name);

    // wait selector here
    await super.check_success_selector(selectors.CONNECTOR_SELECTOR);

    await this.page.waitFor(1000);  // wait linkedIn loading process

    let selector = selectors.CONNECTOR_SELECTOR;
    let connect = await this.page.evaluate((selector) => {
      let a = document.querySelector(selector);
      if (a !== null) {
        a = a.innerText;
      };
      return a;
    }, selector);

    if (connect === this.prospect_full_name) {
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
