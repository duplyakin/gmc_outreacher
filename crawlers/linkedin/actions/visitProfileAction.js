const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class VisitProfileAction extends action.Action {
  constructor(cookies, credentials_id, url) {
    super(cookies, credentials_id);

    this.url = url;
  }

  async visit() {
    await super.gotoChecker(this.url);
    await this.page.waitFor(2000); // XZ how linkedin calculate visits?

    return true;
  }
}

module.exports = {
  VisitProfileAction: VisitProfileAction
}
