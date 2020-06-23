const puppeteer = require("puppeteer");
const LoginAction = require('./loginAction.js');
const links = require("../links");
const selectors = require("../selectors");

var log = require('loglevel').getLogger("o24_logger");

const MyExceptions = require('../../exceptions/exceptions.js');

class Action {
  constructor(cookies, credentials_id) {
    this.cookies = cookies;
    this.credentials_id = credentials_id;
  }


  async startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false }); // test mode
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();

    //log.debug('cooooookiieeeess: ', this.cookies)
    await this.page.setCookie(...this.cookies);

    return this.browser;
  }


  async closeBrowser() {
    await this.browser.close();
    this.browser.disconnect();

    return null;
  }


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


async check_success_selector(selector, page = this.page) {
  if(!selector) {
    throw new Error ('Empty selector.')
  }

  try {
    await page.waitForSelector(selector, { timeout: 5000 })
    return true

  } catch(err) {
    
    if (this.check_block(page.url())) {
      throw MyExceptions.ContextError("Block happend: " + page.url())
    }

    return false
  }
}


  async check_success_page(required_url, page = this.page) {
    if(!required_url) {
      throw new Error ('Empty required_url.')
    }

    let current_url = page.url()

    if(current_url.includes(this.get_pathname(required_url))) {
      return true
    }

    if(this.check_block(page.url())) {
      throw MyExceptions.ContextError("Block happend.")
    }

    // uncknown page here
    throw new Error('Uncknowm page here: ', current_url)
    //return false
  }


  async close_msg_box(page = this.page) {
    if(page == null) {
      throw new Error ('Page not found.')
    }
    try {
      // close messages box !!! (XZ ETOT LINKED)
      await page.waitFor(10000) // wait linkedIn loading process
      await page.waitForSelector(selectors.CLOSE_MSG_BOX_SELECTOR, { timeout: 5000 })
      await page.click(selectors.CLOSE_MSG_BOX_SELECTOR)
      await page.waitFor(2000) // wait linkedIn loading process
    } catch (err) {
      log.debug("action.close_msg_box: CLOSE_MSG_BOX_SELECTOR not found.")
    }
  }


  // format message with data templates
  formatMessage(message, data) {
    if(message == null || message == '') {
      log.debug("action.formatMessage: Empty message.")
      return ''
    }

    if(data == null) {
      return message
    }

    let str = message
    for (var obj in data) {
      str = str.replace(new RegExp('{' + obj + '}', 'g'), data[obj])
    }

    str = str.replace(new RegExp('\{(.*?)\}', 'g'), '')
    return str
  }


  // cut user unique pathname in url
  get_pathname_url(url) {
    if(!url || !url.includes('linkedin') || !url.includes('/in/')) {
      log.error("action.get_pathname_url incorrect url format:", url)
      return url
    }

    var pathname = new URL(url).pathname
    pathname = pathname.split( '/' )[2]

    log.debug("action.get_pathname_url:", pathname)
    return pathname
  }


  // cut pathname in url
  get_pathname(url) {
    if(!url || !url.includes('linkedin')) {
      log.error("action.get_pathname incorrect url format:", url)
      return url
    }

    var pathname = new URL(url).pathname

    log.debug("action.get_pathname:", pathname)
    return pathname
  }


  // do 1 trie to connect URL or goto login
  async gotoChecker(url, page = this.page) {
    //log.debug('gotoChecker - url: ', url);
    if(!url) {
      throw new Error('Empty url.');
    }
    try {
      await page.goto(url, {
        //waitUntil: 'load',
        waitUntil: 'domcontentloaded',
        timeout: 60000 // it may load too long! critical here
      });

      await page.waitFor(15000) // puppeteer wait loading..

      let current_url = page.url()

      let short_url = this.get_pathname(url)

      if (!current_url.includes(short_url)) {
        if (current_url.includes('login') || current_url.includes('signup')) {

          let loginAction = new LoginAction.LoginAction(this.credentials_id);
          await loginAction.setContext(this.context);

          let result = await loginAction.login();
          if (result) {
            await page.goto(url);
          }
        } else {
          log.error('gotoChecker - current url: ', current_url);
          log.error('gotoChecker - required url: ', url);
          throw new Error("gotoChecker - We cann't go to page, we got: " + current_url);
        }
      }
    } catch (err) {
      if(this.check_block(page.url())) {
        throw MyExceptions.ContextError("Block happend.");
      }

      throw new Error('Uncknowm page here: ', page.url());
    }
  }


  async gotoLogin(page = this.page) {
    try {
      await page.goto(links.SIGNIN_LINK, {
        //waitUntil: 'load',
        waitUntil: 'domcontentloaded',
        timeout: 60000 // it may load too long! critical here
      });

      await page.waitFor(15000) // puppeteer wait loading..

      let current_url = page.url();

      if (current_url.includes('login') || current_url.includes('signup')) {

        let loginAction = new LoginAction.LoginAction(this.credentials_id);
        await loginAction.setContext(this.context);

        await loginAction.login(); // if unsuccess - throw eeror
        
      } else if (current_url.includes(links.START_PAGE_SHORTLINK)) {
        return; // success
      } else {
        log.debug('gotoLogin - current url: ', current_url);
        throw new Error("gotoLogin - We cann't go to page, we got: " + current_url);
      }

    } catch (err) { 
      if(this.check_block(page.url())) {
        throw MyExceptions.ContextError("gotoLogin - Block happend.");
      }

      throw new Error('gotoLogin - Uncknowm page here: ', page.url());
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
