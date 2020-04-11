const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");
const links = require(__dirname + "/./links");

export class LoginAction {
  constructor(email, password, cookies) {
    this.email = email;
    this.password = password;

    this.login_url = links.SIGNIN_LINK;
    this.cookies = JSON.parse(cookies);
  }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await page.setCookie(...this.cookies);
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function login() {

    await this.page.goto(this.login_url);
    await this.page.waitForNavigation();

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
    //newCookies = await page.cookies();
    //await fs.writeFile(cookiesFilePath, JSON.stringify(newCookies, null, 2));

    // todo: if success - return: true;
  }

  async function skip_phone(page) {
      await this.page.waitForSelector(selectors.SKIP_PHONE_FORM_SELECTOR);
      await this.page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
  }

  async function check_phone_page(page) {
      let url = await page.url();

      if (url.includes(selectors.SKIP_PHONE_PAGE_SELECTOR)) {
          return true;
      }

      return false;
    }
}
