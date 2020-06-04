const selectors = require("../selectors");
const links = require("../links");
const models = require("../../models/models.js");
const puppeteer = require("puppeteer");

const MyExceptions = require('../../exceptions/exceptions.js');

class LoginAction {
    constructor(email, password, li_at, credentials_id) {
        this.email = email;
        this.password = password;
        this.li_at = li_at;
        this.credentials_id = credentials_id;
    }

    async startBrowser() {
        this.browser = await puppeteer.launch({ headless: false }); // test mode
        //this.browser = await puppeteer.launch();
        this.context = await this.browser.createIncognitoBrowserContext();
        this.page = await this.context.newPage();

        //this.set_cookie(this.cookies);
    }

    async closeBrowser() {
        await this.browser.close();
        this.browser.disconnect();
      }

    async setContext(context) {
        this.context = context;
        this.page = await this.context.newPage();
    }

    async set_cookie(cookies) {
        if (cookies != undefined && cookies != null) {
            //console.log('cooooookiieeeess: ', cookies)
            await this.page.setCookie(...cookies);
            return true;
        }
        return false;
    }

    async _get_domain() {
        await this.page.goto(links.SIGNIN_LINK);
        await this.page.waitFor(1000);

        let current_url = await this.page.url();

        // Exctract domain here in format: “www.linkedin.com”

        return (new URL(current_url)).hostname;
    }

    async _get_current_cookie() {
        // Get Session Cookies
        await this.page.goto(links.SIGNIN_LINK);
        await this.page.waitFor(1000);

        let newCookies = await this.page.cookies();
        if (!newCookies) {
            throw new Error("Can't get cookie.");
        }

        return newCookies;
    }

    async _update_cookie() {
        let new_cookie = await this._get_current_cookie();

        let new_expires = 0;
        new_cookie.forEach((item) => {
            if (item.name === 'li_at') {
                new_expires = item.expires;
            }
        });

        await models.Cookies.updateOne({ credentials_id: this.credentials_id }, { expires: new_expires, data: new_cookie }, { upsert: true }, function (err, res) {
            if (err) throw MyExceptions.MongoDBError('MongoDB find COOKIE err: ' + err); 
        });

    }

    async login_with_email() {
        await this.page.goto(links.SIGNIN_LINK);

        await this.page.waitFor(1000);

        try {
            await this.page.waitForSelector(selectors.USERNAME_SELECTOR, { timeout: 5000 });
          } catch (err) {
            throw MyExceptions.LoginPageError('Login page is not available.');
          }

          await this.page.click(selectors.USERNAME_SELECTOR);
          await this.page.keyboard.type(this.email);
          await this.page.click(selectors.PASSWORD_SELECTOR);
          await this.page.keyboard.type(this.password);
          await this.page.click(selectors.CTA_SELECTOR);
          await this.page.waitFor(1000);
      
          let is_phone = this.check_phone_page(this.page);
          if (is_phone) {
            await this.skip_phone(this.page);
          }
    }


    async login_with_li_at() {
        let domain_var = await this._get_domain();
        if(domain_var == null || domain_var == '') {
            console.log('Never happend: domain_var is broken.')
            return;
        }
        let cookies_data = [{
            name : "li_at",
            value : this.li_at,
            domain : '.' + domain_var,
            path : "/",
            expires : Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
            size : (new TextEncoder().encode(this.li_at)).length,
            httpOnly : true,
            secure : true,
            session : false,
            sameSite : "None"
            }];

        await this.set_cookie(cookies_data);
    }

    async is_logged() {
        //await this.page.waitFor(1000);
        await this.page.goto(links.SIGNIN_LINK, {
            waitUntil: 'load',
            timeout: 60000 // it may load too long! critical here
        });

        let current_url = await this.page.url();
        if (current_url === links.START_PAGE_LINK) { // add domain here
            // login success
            return true;
        } else if (this.check_block()) {
            // BAN here
            let context_obj = await this.get_context();
            if(context_obj !== null && context_obj !== undefined) {
                throw MyExceptions.ContextError('Can\'t goto url: ' + err, context_obj);
            } else {
                console.log( 'Never happend - empty context: ', err );
                throw MyExceptions.ContextError('Can\'t goto url and empty context: ' + err, context_obj);
            }
        }

        // login failed
        return false;
    }

    async login() {

        // check - if we logged
        let logged = await this.is_logged();
        if (logged) {
            await this._update_cookie();
            await this.page.close();
            return logged;
        }

        // if not - try to login with li_at
        if (this.li_at) {
            await this.login_with_li_at();
            logged = await this.is_logged();

            if (logged) {
                await this._update_cookie();
                await this.page.close();
                return logged;
            }
        }

        // if not - try to login with email/password
        if (!this.email || !this.password) {
            throw new Error('BROKEN CREDENTIALS: Email or password is empty.');
        }

        await this.login_with_email()
        logged = await this.is_logged();

        if (!logged) {
            throw new Error('Can\'t login.');
        }

        await this._update_cookie();
        await this.page.close();
        return logged;
    }


    async skip_phone(page) {
        await page.waitForSelector(selectors.SKIP_PHONE_BTN_SELECTOR, { timeout: 5000 });
        await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
    }

    check_phone_page(page) {
        let url = page.url();

        if (url.includes('phone')) {
            return true;
        }

        return false;
    }

    check_block() {
        let current_url = this.page.url();
        if(current_url.includes(links.BAN_LINK) || current_url.includes(links.CHALLENGE_LINK)) {
          return true;
        } else {
          return false;
        }
    }

    async get_context() {
        if(this.browser == null) {
          throw new Error('Can\t get context. Browser is not defined.')
        }
    
        if(this.context == null) {
          throw new Error('Can\t get context. Context is not defined.')
        }
    
        if(this.page == null) {
          throw new Error('Can\t get context. Page is not defined.')
        }
    
        await page.waitFor(10000); // wait 10 sec for lading and screenshot page
        let screenshot_str = await this.page.screenshot();
    
        let context_obj = {
          endpoint: this.browser.wsEndpoint(),
          context_id: this.context._id,
          page_url: this.page.url(),
          screenshot: screenshot_str,
        }
        
        return context_obj;
      }

}

module.exports = {
    LoginAction: LoginAction
}
