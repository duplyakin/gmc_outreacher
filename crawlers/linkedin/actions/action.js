const puppeteer = require("puppeteer");
const LoginAction = require('./loginAction.js');
const links = require("../links");

const MyExceptions = require('../../exceptions/exceptions.js');

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
    await this.browser.close();
    await this.browser.disconnect();
    return null;
  }

  async get_context() {
    if(this.browser == null || this.browser == undefined) {
      throw new Error('Can\t get context. Browser is not defined.')
    }

    if(this.context == null || this.context == undefined) {
      throw new Error('Can\t get context. Context is not defined.')
    }

    if(this.page == null || this.page == undefined) {
      throw new Error('Can\t get context. Page is not defined.')
    }

    await page.waitFor(10000); // wait 10 sec for lading and screenshot page
    let screenshot_str = await page.screenshot();

    let context = {
      endpoint: this.browser.wsEndpoint(),
      context_id: this.context._id,
      url: this.page.url(),
      screenshot: screenshot_str,
    }
    
    return context;
  }

  check_block() {
    let current_url = this.page.url();
    if(current_url == links.BAN_LINK || current_url == links.CHALLENGE_LINK) {
      return true;
    } else {
      return false;
    }
  }

  async error_handler(err) {
    if(err == null || err == undefined) {
      throw new Error('Empty error in error_handler.');
    }

    console.log( err.stack );

    if(this.check_block()) {
      let context_obj = await this.get_context();
      if(context_obj !== null && context_obj !== undefined) {
        throw MyExceptions.ContextError('Can\'t goto url: ' + err, context_obj);
      } else {
        console.log( 'Never happend - empty context: ', err );
        throw MyExceptions.ContextError('Can\'t goto url and empty context: ' + err, context_obj);
      }
    }

    throw MyExceptions.NetworkError('Something wromg with connection: ' + err);
  }

  async close_msg_box(page) {
    if(page == null || page == undefined) {
      throw new Error ('Page not found.');
    }
    try {
      // close messages box !!! (XZ ETOT LINKED)
      await page.waitFor(2000);  // wait linkedIn loading process
      await page.waitForSelector(selectors.CLOSE_MSG_BOX_SELECTOR, { timeout: 5000 });
      await page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
      await page.waitFor(1000);  // wait linkedIn loading process
    } catch (err) {
      console.log("..... CLOSE_MSG_BOX_SELECTOR not found .....")
    }
  }

  // format message
  formatMessage(message, data) {
    if(!message || message == '') {
      throw new Error('Empty message.');
    }

    if(!data) {
      return message;
    }

    let str = message;
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
      let current_url = this.page.url();

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
      this.error_handler(err);
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
