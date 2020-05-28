const puppeteer = require("puppeteer");
const LoginAction = require('./loginAction.js');

const MyExceptions = require('./../../exceptions/exceptions.js');

class Action {
  constructor(email, password, li_at, cookies, credentials_id) {
    this.email = email;
    this.password = password;
    this.li_at = li_at;

    this.cookies = cookies;
    
    this.credentials_id = credentials_id;
  }

  async startBrowser() {
    this.browser = await puppeteer.launch({ headless: false }); // test mode
    //this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();

    //console.log('cooooookiieeeess: ', this.cookies)
    await this.page.setCookie(...this.cookies);

    return this.browser;
  }

  async closeBrowser() {
    this.browser.disconnect();
    this.browser.close();
    return null;
  }

  formatMessage(template, data) {
    // format template
    let str = template;
    for (var obj in data) {
      str = str.replace(new RegExp('{' + obj + '}', 'g'), data[obj]);
    }
    str = str.replace(new RegExp('\{(.*?)\}', 'g'), '');
    return str;
  }

  // do 1 trie to connect URL or goto login
  async gotoChecker(url) {
    try {
      //console.log('........url......: ', url);
      if(!url) {
        throw new Error ('Empty url.');
      }
      await this.page.goto(url);
      let current_url = await this.page.url();

      if (current_url !== url) {
        if (current_url.includes('login') || current_url.includes('signup')) {

          let loginAction = new LoginAction.LoginAction(this.email, this.password, this.li_at, this.credentials_id);
          await loginAction.setContext(this.context);

          let result = await loginAction.login();
          if (result) {
            await this.page.goto(url);
          }
        } else {
          console.log('current_url: ', current_url);
          console.log('url: ', url);
          throw MyExceptions.BanError('We cann\'t go to page, we got: ' + current_url);
        }
      }
    } catch (err) {
      // TODO: check, if it BanError
      console.log( err.stack )
      throw MyExceptions.NetworkError('Something wromg with network: ' + err);
    }
  }

  async autoScroll(page) {
    await page.evaluate(async () => {
      await new Promise((resolve, reject) => {
        var totalHeight = 0;
        var distance = 100;
        var timer = setInterval(() => {
          var scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;

          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, 100);
      });
    });
  }

}

module.exports = {
  Action: Action
}
