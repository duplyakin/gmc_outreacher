const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class Action {
  constructor(email, password, cookies) {
    this.email = email;
    this.password = password;
    this.cookies = cookies;
  }

  async startBrowser() {
    this.browser = await puppeteer.launch({ headless: false }); // test mode
    //this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async closeBrowser() {
    this.browser.disconnect();
    this.browser.close();
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

  // do 3 tries to connect URL or goto login
  async gotoCheckerThree(url) {
    for (let i = 0; i < 3; i++) {
      await this.page.goto(url);
      let current_url = await this.page.url();
      if (current_url.includes('login') || current_url.includes('signup')) {
        let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
        await loginAction.startBrowser();
        await loginAction.login();
      } else {
        return true;
      }
    }
    return false;
  }

  // do 1 trie to connect URL or goto login
  async gotoChecker(url) {

    await this.page.goto(url);
    let current_url = await this.page.url();

    if (current_url !== url) {
      if (current_url.includes('login') || current_url.includes('signup')) {

        let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
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
