'use strict';

const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");
const { logger } = require(__dirname + "/../../utils/logger");


class loginAction {
    constructor(email, password) {
        this.email = email;
        this.password = password;

        this.login_url = selectors.linkedin_login_url;
        this._cookies = {}
    }

    cookies(){
        return this._cookies
    }

    async init(){
        this.browser = await puppeteer.launch();
        this.context = await this.browser.createIncognitoBrowserContext();
    }

    async destroy(){
        this.browser.close()
    }

    async login(){
        var page = await this.context.newPage();
        await page.goto(this.login_url);
        await page.waitForSelector(selectors.login_form);

        await page.type(selectors.linkedin_login_id, this.email, {delay: 100})
        await page.type(selectors.linkedin_password_id, this.password, {delay: 100})

        await page.click(selectors.linkedin_login_submit)
        
        let is_phone = await this.check_phone_page(page);
        if (is_phone){
            await this.skip_phone(page);
        }
        await page.waitForSelector(selectors.linkedin_feed_search_div);

        this._cookies = await page.cookies()

        this.browser.close()
    }

    async skip_phone(page){
        await page.waitForSelector(selectors.linkedin_phone_skip_div);
        await page.click(selectors.linkedin_phone_skip_button);
    }

    async check_phone_page(page){
        let url = await page.url();

        if (url.includes(selectors.linkedin_phone_url)){
            return true;
        }

        return false;
    }

    async chek_feed_page(page){
        let url = await page.url();

        if (url.includes(selectors.linkedin_feed_url)){
            return true;
        }

        return false;

    }
}

module.exports = loginAction;