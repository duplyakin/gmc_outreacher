const selectors = require(__dirname + "/.././selectors");
const links = require(__dirname + "/.././links");
const cookieModel = require(__dirname + "/../.././models/models.js");
const action = require(__dirname + '/action.js');
const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class LoginAction extends action.Action {
  constructor(email, password, cookies) {
    super(email, password, cookies);
  }

  async startBrowser() {
    this.browser = await puppeteer.launch({ headless: false });
    //this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();

    if (this.cookies != undefined && this.cookies != null) {
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
    let current_url = await this.page.url();

    if (current_url === links.START_PAGE_LINK) {
      return true;
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

    // Save Session Cookies
    let newCookies = await this.page.cookies();
    let newExpires = 0;
    newCookies.forEach((item) => {
      if (item.name === 'li_at') {
        newExpires = item.expires;
      }
    });

    // check - if login success
    current_url = await this.page.url();
    if (current_url === links.START_PAGE_LINK) {
      console.log('........login success.......');
      await this.page.close();

      // add / update user in DB
      let user = await cookieModel.Cookies.findOne({ username: this.email });
      //console.log('........find object: ........', user);
      if (user === undefined || user === null) {
        // create new user
        let newCookiesDocument = await new cookieModel.Cookies({ username: this.email, expires: newExpires, data: newCookies });
        await newCookiesDocument.save(function (err) {
          if (err) return handleError(err);
          // saved!
          console.log('........saved in mongoDB.......');
        });
      } else {
        // update user info
        await user.updateOne({ expires: newExpires, data: newCookies }, function (err, res) {
          // updated!
          console.log('........updated in mongoDB.......');
        });
      }

      return true;
    } else {
      throw MyExceptions.LoginError('Login error - check credentials');
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
