const selectors = require("../selectors");
const links = require("../links");
const cookieModel = require("../../models/models.js");
const action = require('./action.js');
const puppeteer = require("puppeteer");

const MyExceptions = require('../../exceptions/exceptions.js');

class LoginAction extends action.Action {
  constructor(email, password, cookies, credentials_id) {
    super(email, password, cookies, credentials_id);
  }

  async startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false }); // test mode
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();

    if (this.cookies != undefined && this.cookies != null) {
      //console.log(this.cookies)
      await this.page.setCookie(...this.cookies);
    }
  }

  async setContext(context) {
    this.context = context;
    this.page = await this.context.newPage();
  }

  async login() {
    await this.page.goto(links.SIGNIN_LINK);

    await this.page.waitFor(1000);  // wait linkedIn loading process (not needed here, but XZ ETOT LINKED)
    
    let res = await this.check_login();
    if(res) {
      // cookies fine
      return res;
    }

    try {
      await this.page.waitForSelector(selectors.USERNAME_SELECTOR, { timeout: 5000 });
    } catch (err) {
      throw MyExceptions.LoginPageError('Login page is not available');
    }
    await this.page.click(selectors.USERNAME_SELECTOR);
    await this.page.keyboard.type(this.email);
    await this.page.click(selectors.PASSWORD_SELECTOR);
    await this.page.keyboard.type(this.password);
    await this.page.click(selectors.CTA_SELECTOR);

    let is_phone = await this.check_phone_page(this.page);
    if (is_phone) {
      await this.skip_phone(this.page);
    }

    res = await this.check_login();
    if(res) {
      return res;
    } else {
      throw MyExceptions.LoginError('Login error - check credentials');
    }
  }

  async check_login() {
    // check - if login success
    let current_url = await this.page.url();
    if (current_url === links.START_PAGE_LINK) {

      console.log('........login success.......');

      // add / update cookie_obj in DB
      let cookie_obj = await cookieModel.Cookies.findOne({ credentials_id: this.credentials_id }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err);
      });

      // Get Session Cookies
      let newCookies = await this.page.cookies();
      let newExpires = 0;
      newCookies.forEach((item) => {
        if (item.name === 'li_at') {
          newExpires = item.expires;
        }
      });

      await this.page.close(); // if we call loginAction from any other worker - we have to close page here

      //console.log('........find cookie object: ........', cookie_obj);
      if (cookie_obj === undefined || cookie_obj === null) {
        // create new cookie_obj
        let newCookiesDocument = await new cookieModel.Cookies({ credentials_id: this.credentials_id, expires: newExpires, data: newCookies });
        await newCookiesDocument.save(function (err) {
          if (err) throw MyExceptions.MongoDBError('MongoDB save COOKIE err: ' + err);
          // saved!
          console.log('........saved in mongoDB.......');
        });

      } else {
        // update cookie_obj info
        await cookie_obj.updateOne({ expires: newExpires, data: newCookies }, function (err, res) {
          if (err) throw MyExceptions.MongoDBError('MongoDB update COOKIE err: ' + err);
          // updated!
          console.log('........updated in mongoDB.......');
        });
      }

      return true;
    } else {
      return false;
    }
  }

  async skip_phone(page) {
    await page.waitForSelector(selectors.SKIP_PHONE_BTN_SELECTOR, { timeout: 5000 });
    await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
  }

  async check_phone_page(page) {
    let url = await page.url();

    if (url.includes('phone')) {
      return true;
    }

    return false;
  }
}

module.exports = {
  LoginAction: LoginAction
}
