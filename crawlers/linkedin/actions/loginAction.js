const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");
const links = require(__dirname + "/./links");

export class LoginAction {
  constructor(email, password, cookies) {
    this.email = email;
    this.password = password;

    this.login_url = links.SIGNIN_LINK;
    this._cookies = cookies;
  }

  cookies() {
      return this._cookies
   }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function login() {
    const page = await this.context.newPage();

    // Load Session Cookies
    //const cookiesString = await fs.readFile(cookiesFilePath);
    //const cookies = JSON.parse(cookiesString);
    //await page.setCookie(...cookies);

    await page.goto(this.login_url);
    //await page.waitForSelector(selectors.login_form); // TODO

    await page.click(selectors.USERNAME_SELECTOR);
    await page.keyboard.type(this.email);
    await page.click(selectors.PASSWORD_SELECTOR);
    await page.keyboard.type(this.password);
    await page.click(selectors.CTA_SELECTOR);
    await page.waitForNavigation();

    let is_phone = await this.check_phone_page(page);
    if (is_phone) {
        await this.skip_phone(page);
    }
    // Save Session Cookies
    //newCookies = await page.cookies();
    //await fs.writeFile(cookiesFilePath, JSON.stringify(newCookies, null, 2));

    // todo: if success - return: true;
  }

  async function skip_phone(page) {
      await page.waitForSelector(selectors.SKIP_PHONE_FORM_SELECTOR);
      await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
  }

  async function check_phone_page(page) {
      let url = await page.url();

      if (url.includes(selectors.SKIP_PHONE_PAGE_SELECTOR)) {
          return true;
      }

      return false;
    }
}
