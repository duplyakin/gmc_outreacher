const selectors = require("../selectors");
const links = require("../links");
const models = require("../../models/models.js");
const puppeteer = require("puppeteer");

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class LoginAction {
    constructor(credentials_id) {
        this.credentials_id = credentials_id
    }

    async startBrowser() {
        //this.browser = await puppeteer.launch({ headless: false }) // test mode
        this.browser = await puppeteer.launch()
        this.context = await this.browser.createIncognitoBrowserContext()
        this.page = await this.context.newPage()

        //this.set_cookie(...this.cookies)
    }

    async closeBrowser() {
        await this.browser.close()
        this.browser.disconnect()
      }

    async setContext(context) {
        this.context = context
        this.page = await this.context.newPage()
    }

    async set_cookie(cookies) {
        if (cookies != null) {
            //log.debug('cooooookiieeeess: ', cookies)
            await this.page.setCookie(...cookies)
            return true
        }
        return false
    }

    async _get_domain() {
        let current_url = this.page.url()

        // Exctract domain here in format: “www.linkedin.com”

        return (new URL(current_url)).hostname
    }

    async _get_current_cookie() {
        // Get Session Cookies
        let newCookies = await this.page.cookies();
        if (!newCookies) {
            throw new Error("Can't get cookie.");
        }

        return newCookies;
    }

    async _update_cookie() {
        let new_cookies = await this._get_current_cookie();

        let new_expires = 0;
        for(let item of new_cookies) {
            if (item.name === 'li_at') {
                new_expires = item.expires;
            }
        }

        let account = await models.Accounts.findOneAndUpdate({ _id: this.credentials_id }, { expires: new_expires, cookies: new_cookies }, { upsert: false }, function (err, res) {
            if (err) throw MyExceptions.MongoDBError('MongoDB find Account err: ' + err); 
        });

        if(account == null) {
            throw MyExceptions.LoginActionError("Account with credentials_id: " + this.credentials_id + " not exists.");
        }
    }

    async get_account() {
        let account = await models.Accounts.findOne({ _id: this.credentials_id });
        if(account == null) {
            throw MyExceptions.LoginActionError("Account with credentials_id: " + this.credentials_id + " not exists.");
        }
        return account;
    }

    async login_with_email() {
        await this.page.goto(links.SIGNIN_LINK, {
            waitUntil: 'load',
            timeout: 60000 // it may load too long! critical here
        })
        
        try {
            await this.page.waitForSelector(selectors.USERNAME_SELECTOR, { timeout: 5000 });
        } catch (err) {
            throw MyExceptions.LoginPageError('Login page is not available.');
        }

        let account = await this.get_account();
        if(account == null) {
            throw MyExceptions.LoginActionError("Account with credentials_id: " + this.credentials_id + " not exists.");
        }

        if(!account.login || !account.password) {
            throw MyExceptions.LoginActionError("Empty login or password in account.");
        }

        await this.page.click(selectors.USERNAME_SELECTOR);
        await this.page.keyboard.type(account.login);
        await this.page.click(selectors.PASSWORD_SELECTOR);
        await this.page.keyboard.type(account.password);
        await this.page.click(selectors.CTA_SELECTOR);
        await this.page.waitFor(1000);
    
        let is_phone = this.check_phone_page(this.page.url());
        if (is_phone) {
            await this.skip_phone(this.page);
        }
    }

/*
    async login_with_li_at() {
        let domain_var = await this._get_domain();
        if(domain_var == null || domain_var == '') {
            log.debug('Never happend: domain_var is broken.')
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
*/

    async is_logged() {
        /*
        await this.page.waitFor(2000)
        await this.page.goto(links.SIGNIN_LINK, {
            waitUntil: 'load',
            timeout: 60000 // it may load too long! critical here
        })

        await this.page.waitFor(7000) // puppeteer wait loading..
        */

        let current_url = this.page.url()
        if (current_url.includes(links.START_PAGE_SHORTLINK)) {
            // login success
            log.debug("LoginAction: Login success.")
            return true
        } else if (this.check_block(current_url)) {
            // BAN here
            log.debug("LoginAction: Not logged - BAN here. current url: ", current_url)
            throw MyExceptions.ContextError("Can't goto url: " + current_url)
        }

        log.debug("LoginAction: Not logged. current url: ", current_url)
        // login failed
        return false;
    }

    async login() {

        // check - if we logged
        let logged = await this.is_logged()
        if (logged) {
            await this._update_cookie()
            await this.page.close()
            return logged
        }

        /*
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
        */

        // if not - try to login with login/password
        await this.login_with_email()
        logged = await this.is_logged()

        if (!logged) {
            throw MyExceptions.LoginActionError("Can't login")
        }

        await this._update_cookie()
        await this.page.close()

        return logged
    }


    async skip_phone(page) {
        await page.waitForSelector(selectors.SKIP_PHONE_BTN_SELECTOR, { timeout: 5000 });
        await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
    }

    check_phone_page(url) {
        if (url.includes('phone')) {
            return true;
        }

        return false;
    }

    check_block(url) {
        if(!url) {
          throw new Error('LoginAction: Empty url in check_block.')
        }
    
        if(url.includes(links.BAN_LINK) || url.includes(links.CHALLENGE_LINK)) {
          // not target page here
          return true;
        } else {
          // all ok
          return false;
        }
      }
}

module.exports = {
    LoginAction: LoginAction
}
