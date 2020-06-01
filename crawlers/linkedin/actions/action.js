const puppeteer = require("puppeteer");
const LoginAction = require('./loginAction.js');
const links = require("../links");
const selectors = require("../selectors");

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
    this.browser.disconnect();

    return null;
  }

  async get_context(browser = this.browser, context = this.context, page = this.page) {
    if(browser == null) {
      throw new Error('Can\t get context. Browser is not defined.')
    }

    if(context == null) {
      throw new Error('Can\t get context. Context is not defined.')
    }

    if(page == null) {
      throw new Error('Can\t get context. Page is not defined.')
    }

    await page.waitFor(10000); // wait 10 sec for lading and screenshot page
    let screenshot_str = await page.screenshot();

    let context_obj = {
      endpoint: browser.wsEndpoint(),
      context_id: context._id,
      page_url: page.url(),
      screenshot: screenshot_str,
    }
    
    return context_obj;
  }

/*
  check_block(url) {
    if(!url) {
      throw new Error('Empty url in check_block.')
    }

    if(url.includes(links.BAN_LINK) || url.includes(links.CHALLENGE_LINK)) {
      // not target page here
      return true;
    } else {
      // all ok
      return false;
    }
  }

  async check_success_selector(selector, page = this.page, data = null) {
    if(!selector) {
      throw new Error ('Empty selector.');
    }

    try {
      await page.waitForSelector(selector, { timeout: 5000 });

    } catch(err) {
      if(this.check_block(page)) {
        // not target page here
        let context_obj = await this.get_context(); // todo: send here browser, page, context

        if(context_obj != null) {
          throw MyExceptions.ContextError('Can\'t goto url: ' + err, context_obj, data);

        } else {
          console.log( 'Never happend - empty context: ', err );
          throw new Error('Can\'t goto url and empty context: ' + err);
        }
      }
 
      // uncknown page here
      throw MyExceptions.NetworkError('Something wromg with connection or uncknown page: ' + err);
    }
  }
*/

async check_block(url, data = null) {
  if(!url) {
    throw new Error('Empty url in check_block.')
  }

  if(url.includes(links.BAN_LINK) || url.includes(links.CHALLENGE_LINK)) {
    // not target page here
    let context_obj = await this.get_context(); // todo: send here browser, page, context

    if(context_obj != null) {
      if(data != null) {
        // add info to excisting result_data
        data.code = MyExceptions.ContextError().code;
        data.raw = MyExceptions.ContextError('Can\'t goto url: ' + url).error;
        data.blocking_data = context_obj;
      } 
      throw MyExceptions.ContextError('Can\'t goto url: ' + url, context_obj, data);
    } else {
      console.log( 'Never happend - empty context in check_block.');
      throw new Error('Can\'t goto url and empty context in check_block');
    }

  } else {
    // all ok
    return false;
  }
}

async check_success_selector(selector, page = this.page, data = null) {
  if(!selector) {
    throw new Error ('Empty selector.');
  }

  try {
    await page.waitForSelector(selector, { timeout: 5000 });

  } catch(err) {
    await this.check_block(page.url(), data);

    // uncknown page here
    throw MyExceptions.NetworkError('Something wromg with connection or uncknown page: ' + err);
  }
}

  async check_success_page(required_url, page = this.page, data = null) {
    if(!required_url) {
      throw new Error ('Empty required_url.');
    }

    let current_url = page.url();

    if(current_url.includes(required_url)) {
      return true;
    }

    await this.check_block(page.url(), data);

    // uncknown page here
    throw new Error('Uncknowm page here: ', current_url);
  }

  async close_msg_box(page = this.page) {
    if(page == null) {
      throw new Error ('Page not found.');
    }
    try {
      // close messages box !!! (XZ ETOT LINKED)
      await page.waitFor(2000);  // wait linkedIn loading process
      await page.waitForSelector(selectors.CLOSE_MSG_BOX_SELECTOR, { timeout: 5000 });
      await page.click(selectors.CLOSE_MSG_BOX_SELECTOR);
      await page.waitFor(1000);  // wait linkedIn loading process
    } catch (err) {
      console.log("..... CLOSE_MSG_BOX_SELECTOR not found .....");
    }
  }

  // format message
  formatMessage(message, data) {
    if(!message || message == '') {
      //throw new Error('Empty message.');
      return '';
    }

    if(data == null) {
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
  async gotoChecker(url, page = this.page) {
    //console.log('........url......: ', url);
    if(!url) {
      throw new Error ('Empty url.');
    }
    try {
      await page.goto(url);
      let current_url = page.url();

      if (current_url !== url) {
        if (current_url.includes('login') || current_url.includes('signup')) {

          let loginAction = new LoginAction.LoginAction(this.email, this.password, this.li_at, this.credentials_id);
          await loginAction.setContext(this.context);

          let result = await loginAction.login();
          if (result) {
            await page.goto(url);
          }
        } else {
          console.log('current_url: ', current_url);
          console.log('url: ', url);
          throw new Error('We cann\'t go to page, we got: ' + current_url);
        }
      }
    } catch (err) {
      await this.check_block(page.url());
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
