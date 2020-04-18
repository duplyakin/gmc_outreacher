const puppeteer = require(__dirname + "/../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const links = require(__dirname + "/.././links");
//const cookieModel = require(__dirname + "/../.././models/models.js");

class LoginAction {
  constructor(email, password, cookies) {
    this.email = email;
    this.password = password;

    this.login_url = links.SIGNIN_LINK;
    //this.cookies = JSON.parse(cookies);
    this.cookies = cookies;

  }

  async startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    if(this.cookies != undefined || this.cookies != null) {
      await this.page.setCookie(...this.cookies);
    }
  }

  async closeBrowser(browser) {
    this.browser.close();
  }

  async login() {

    await this.page.goto(this.login_url);
    await this.page.waitForSelector(selectors.USERNAME_SELECTOR);

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
      if(item.name === 'li_at') {
        newExpires = item.expires;
      }
    });

    //let newCookiesDocument = await new Cookie({username: email, expires: newExpires, data: newCookies});
    //await newCookiesDocument.save(function (err) {
    //if (err) return handleError(err);
    // saved!
  //  });

    // todo: if success - return: true;
    return true;
  }

  async skip_phone(page) {
      await page.waitForSelector(selectors.SKIP_PHONE_FORM_SELECTOR);
      await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
  }

  async check_phone_page(page) {
      let url = await page.url();

      if (url.includes(selectors.SKIP_PHONE_PAGE_SELECTOR)) {
          return true;
      }

      return false;
    }
}

module.exports = {
    LoginAction: LoginAction
}
