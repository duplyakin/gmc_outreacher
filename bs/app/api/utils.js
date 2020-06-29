const puppeteer = require('puppeteer')

const links = require('../../../crawlers/linkedin/links')
const selectors = require('../../../crawlers/linkedin/selectors')
const status_codes = require('../../../crawlers/linkedin/status_codes')

const models = require('../../../crawlers/models/models')
const models_shared = require('../../../crawlers/models/shared')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");


// -2 = system err, -1 = block, 0 = resolved, 2 = captcha
const found_form_and_input = async (page, input) => {
    if(page == null) {
        log.error('Empty page in found_form_and_input.');
        return -2;
    }

    let url = page.url();
    let res = -2;

    if(!url) {
        log.error('Empty url in found_form_and_input.');
        return -2;
    }

    if (await page.$(selectors.CAPTCHA_SELECTOR) != null) {
        res = await resolve_captcha(page, input);
    } else if (url.includes(links.CHALLENGE_LINK)) {
        res = await resolve_challenge(page, input);
    }  else {
        //todo: add logic for empty page (try again status or smth like that)
        log.error('UNCKNOWN page found_form_and_input: ', url);
        return -2;
    }

    return res;
}


// -2 = system err, -1 = block, 0 = resolved, 2 = captcha
const resolve_challenge = async(page, input) => {
    try {
        if(page == null) {
            log.erro("..... Empty page in resolve_challenge. ..... ");
            return -2;
        }

        if(!input || input == '') {
            log.error("..... Input can't be empty in resolve_challenge. ..... ");
            return -2;
        }

        try {
            await page.waitForSelector(selectors.VERIFICATION_PIN_SELECTOR, { timeout: 5000 });
            await page.waitForSelector(selectors.VERIFICATION_PIN_BTN_SELECTOR, { timeout: 5000 });
        } catch (err) {
            log.error("..... Challenge page selectors not found in resolve_challenge. ..... ");
            return -2;
        }

        await page.click(selectors.VERIFICATION_PIN_SELECTOR);
        await page.keyboard.type(input);
        await page.click(selectors.VERIFICATION_PIN_BTN_SELECTOR);
        await page.waitFor(10000);

        if (await page.$(selectors.CAPTCHA_SELECTOR) != null) {
            log.debug("Captcha happend in resolve_challenge.")
            return 2; // captcha happend
        }

        let current_url = page.url();

        if(check_block_url(current_url)) {
            return -1; // block not resolved
        }

        /*
        //await page.goto(links.START_PAGE_LINK); // test - need it or not
        if(current_url == links.START_PAGE_LINK || current_url == links.SIGNIN_LINK) {
            return 0; // resolved
        } else {
            return -1; // block not resolved
        }
        */

        return 0; // resolved

    } catch(err) {
        log.error("..... Error in resolve_challenge: ..... ", err.stack);
        return -2;
    }
}


// -2 = system err, -1 = block, 0 = resolved, 2 = captcha
const resolve_captcha = async(page, response) => {
    try {
        if(page == null) {
            log.erro("..... Empty page in resolve_captcha. ..... ")
            return -2
        }

        if(!response || response == '') {
            log.error("..... response can't be empty in resolve_captcha. ..... ")
            return -2
        }

        try {
            await page.waitForSelector(selectors.CAPTCHA_RESPONSE_SELECTOR, { timeout: 5000 })
        } catch (err) {
            log.error("..... Captcha selector not found in resolve_captcha. ..... ");
            return -2;
        }

        await page.evaluate((response) => {
            document.querySelector(selectors.CAPTCHA_RESPONSE_SELECTOR).value = response
          }, response)
        
        try {
            await page.waitForSelector(selectors.SUBMIT_CAPTCHA_BTN_SELECTOR, { timeout: 5000 })
        } catch (err) {
            log.error("..... Captcha submit BTN selector not found in resolve_captcha. ..... ");
            return -2;
        }
        await page.click(selectors.SUBMIT_CAPTCHA_BTN_SELECTOR);
        await page.waitFor(10000);

        if (await page.$(selectors.CAPTCHA_SELECTOR) != null) {
            log.debug("Captcha not resolved in resolve_captcha.")
            return 2; // captcha not resolved
        }

        let current_url = page.url();

        if(check_block_url(current_url)) {
            return -1; // block not resolved
        }

        /*
        //await page.goto(links.START_PAGE_LINK); // test - need it or not
        if(current_url == links.START_PAGE_LINK || current_url == links.SIGNIN_LINK) {
            return 0; // resolved
        } else {
            return -1; // block not resolved
        }
        */

        return 0; // resolved

    } catch(err) {
        log.error("..... Error in resolve_captcha: ..... ", err.stack);
        return -2;
    }
}


const check_block_url = (url) => {
    if(!url) {
        throw new Error('Empty url in check_block_url.');
    }

    if(url.includes(links.BAN_LINK) || url.includes(links.CHALLENGE_LINK)) {
        log.debug('check_block_url block happend: ', url);
        return true;
    }

    return false;
}


const skip_phone = async(page) => {
    await page.waitForSelector(selectors.SKIP_PHONE_BTN_SELECTOR, { timeout: 5000 });
    await page.click(selectors.SKIP_PHONE_BTN_SELECTOR);
}


const check_phone_page = (url) => {
    if (url.includes('phone')) {
        return true;
    }

    return false;
}


// -2 = system err, -1 = block, 0 = resolved, 4 = wrong credentials, 2 = captcha
const login = async(page, account) => {
    try {
        if(!account.login || !account.password) {
            log.error("Empty login or password in login.")
            return -2; 
        }

        if(page == null) {
            log.error("Empty page in login.")
            return -2;
        }

        await page.goto(links.SIGNIN_LINK, {
            waitUntil: 'load',
            timeout: 60000 // it may load too long! critical here
        });

        try {
            await page.waitForSelector(selectors.USERNAME_SELECTOR, { timeout: 5000 });
        } catch (err) {
            log.error("Login page is not available in login, current url = ", page.url())
            return -2;
        }

        await page.click(selectors.USERNAME_SELECTOR);
        await page.keyboard.type(account.login);
        await page.click(selectors.PASSWORD_SELECTOR);
        await page.keyboard.type(account.password);
        await page.click(selectors.CTA_SELECTOR);
        await page.waitFor(10000);

        try {
            // todo: check toast by url (?)
            //await page.waitForSelector(selectors.BLOCK_TOAST_SELECTOR, { timeout: 1000 }); // todo: add status - wait a day and try again
        } catch (err) {
            log.error("Login FAILED - toast error.")
            return -2;
        }
    
        let current_url = page.url();

        if (check_phone_page(current_url)) {
            await skip_phone(page);
            current_url = page.url();
        }

        if (await page.$(selectors.CAPTCHA_SELECTOR) != null) {
            log.debug("Captcha happend in login.")
            return 2; // captcha happend
        }

        if (check_block_url(current_url)) {
            log.debug("Block happend in login.")
            return -1; // block happend
        }

        if (current_url.includes(links.SIGNIN_SHORTLINK)) {
            log.debug("Wrong credentials in login.")
            return 4; // wrong credentials
        }

        log.debug("login success.") // add check here (?)
        return 0; // logged in
    } catch(err) {
        log.error("Error in login(): ", err.stack);
        return -2;
    }
}


const get_context = async(browser, context, page) => {
    if(browser == null) {
      throw new Error("Can't get_context. Browser is not defined.");
    }

    if(context == null) {
      throw new Error("Can't get_context. Context is not defined.");
    }

    if(page == null) {
      throw new Error("Can't get_context. Page is not defined.");
    }

    await page.waitFor(10000); // wait 10 sec for lading and screenshot the page
    let screenshot_str = await page.screenshot();

    let context_obj = {
      endpoint: browser.wsEndpoint(),
      context_id: context._id,
      page_url: page.url(),
      screenshot: screenshot_str,
    }
    
    log.debug('get_context - context_obj created.');
    //log.debug('get_context - context_obj = ', context_obj);
    return context_obj;
  }


  const get_sitekey = async(page) => {
    if(page == null) {
      throw new Error("Can't get_sitekey. Page is not defined.")
    }

    let mySelector = selectors.CAPTCHA_SELECTOR
    try {
        await page.waitForSelector(mySelector, { timeout: 5000 })
    } catch(err) {
        throw new Error("get_sitekey: captcha selector not found")
    }

    let sitekey = await page.evaluate((mySelector) => {
        return document.querySelector(mySelector).dataset.sitekey
      }, mySelector)

    if(sitekey == '' || sitekey == null) {
        throw new Error("get_sitekey - sitekey not found.")
    }
    
    log.debug('get_sitekey - sitekey:', sitekey)
    return sitekey
  }


const validate_data = async(data) => {
    let endpoint = data.endpoint;
    if (!endpoint){
        throw new Error('DATA BROKEN: no endpoint');
    }

    let context_id = data.context_id;
    if (!context_id){
        throw new Error('DATA BROKEN: no context_id');
    }

    let page_url = data.page_url;
    if (!page_url){
        throw new Error('DATA BROKEN: no page_url');
    }

    /*
    let screenshot = data.screenshot;
    if (!screenshot){
        throw new Error('DATA BROKEN: no screenshot');
    }
    */

}


const context_connect = async (browser, context_id) => {
    let contexts = await browser.browserContexts();
    if (contexts == null) {
        throw new Error("Can't receive browser.browserContexts");
    }

    if(context_id == null) {
        throw new Error("Empty context_id in context_connect");
    }

    let found_context = null;
    for (var cx in contexts) { // for of
        if (contexts[cx]._id == context_id){
            found_context = contexts[cx];
            break;
        }
    }

    if (found_context == null) {
        throw new Error("Can't find context by id: " + context_id);
    }

    return found_context;
}


const page_connect = async (context, page_url) => {
    if (context == null) {
        throw new Error("Can't find context: " + context);
    }

    if(!page_url){
        throw new Error("Can't find page_url: " + page_url);
    }

    let pages = await context.pages();
    if (pages == null) {
        throw new Error("Context doesn't have pages.");
    }

    let found_page = null;
    for (var p in pages) {  // for of
        if (pages[p].url() == page_url) { // here can be several pages with the same url
            found_page = pages[p];
            break;
        }
    }

    if (found_page == null){
        throw new Error("Can't find page by url: " + page_url);
    }

    return found_page;
}


const input_data = async (account, input) => {
    if (!input){
        log.debug("..... Empty input in input_data. ..... ");
    }

    if(account == null) {
        throw new Error('Empty account in input_data.');
    }

    if (account.blocking_data == null) {
        throw new Error('There is no account.blocking_data.');
    }

    let browser = null;

    try {
        await validate_data(account.blocking_data);

        browser = await puppeteer.connect({
            browserWSEndpoint: account.blocking_data.endpoint
        });

        if (browser == null){
            throw new Error("Can't connect to browser endpoint.");
        }

        let context = await context_connect(browser, account.blocking_data.context_id);
        if (context == null){
            throw new Error("Can't connect to context.");
        }
        let page = await page_connect(context, account.blocking_data.page_url);
        if (page == null){
            throw new Error("Can't connect to page.");
        }

        let res = await found_form_and_input(page, input);
        log.debug('input_data res = ', res);

        if(res == 0) { // block resolved
            // get new cookies
            let new_cookies = await _get_current_cookie(page);
            let new_expires = 0;
            for(let item of new_cookies) {
                if (item.name === 'li_at') {
                    new_expires = item.expires;
                }
            }

            let account_update = {
                status: status_codes.AVAILABLE,
                task_id: null, 
                blocking_data: null, 
                blocking_type: null,
                cookies: new_cookies,
                expires: new_expires,
            }

            await models.Accounts.findOneAndUpdate({ _id: account._id }, account_update, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.ACTIVE }, { upsert: false });
            if(account.task_id != null) {
                await models_shared.TaskQueue.findOneAndUpdate({ _id: account.task_id }, { status: status_codes.NEED_USER_ACTION_RESOLVED }, { upsert: false });
            }
            
            await browser.close();
            browser.disconnect();
            log.debug("..... BLOCK RESOLVED. ..... ");

        } else if (res == -1) {
            // block didn't resolved
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_data: context_obj is null.");
            }

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_type: "code", blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res == 2) {
            // captcha
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_data: context_obj is null.");
            }
            let sitekey = await get_sitekey(page);
            if(sitekey == null) {
                throw new Error("Error in input_data: sitekey is null.");
            }

            context_obj.sitekey = sitekey

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_type: "captcha", blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res == -2) {
            // system error
            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });
            
            await browser.close();
            browser.disconnect();
        }

    } catch(err) {
        log.error("..... Error in input_data account._id: ..... ", account._id);
        log.error("..... Error in input_data: ..... ", err.stack);  

        await models.Accounts.findOneAndUpdate({ _id: account._id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.AVAILABLE }, { upsert: false });

        if(browser != null) {
            await browser.close();
            browser.disconnect();
        }
    }
}


const input_login = async (account) => {
    if(account == null) {
        throw new Error('Empty account in input_login.');
    }

    let browser = null;

    try {
        //browser = await puppeteer.launch({ headless: false }); // test mode
        browser = await puppeteer.launch();
        context = await browser.createIncognitoBrowserContext();
        page = await context.newPage();

        let res = await login(page, account);
        log.debug('input_login res = ', res);

        if(res === 0) { // login success
            // get new cookies
            let new_cookies = await _get_current_cookie(page);
            let new_expires = 0;
            new_cookies.forEach((item) => {
                if (item.name === 'li_at') {
                    new_expires = item.expires;
                }
            });

            let account_new = { 
                status: status_codes.AVAILABLE, 
                login: account.login,
                password: account.password,
                cookies: new_cookies,
                expires: new_expires,
                task_id: null, // !
            }

            //log.debug('input_login account_new = ', account_new)
            
            await models.Accounts.findOneAndUpdate({ _id: account._id }, account_new, { upsert: false }); // upsert = false; because we have already created account object in DB
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.ACTIVE }, { upsert: false });
            if(account.task_id != null) {
                await models_shared.TaskQueue.findOneAndUpdate({ _id: account.task_id }, { status: status_codes.NEED_USER_ACTION_RESOLVED }, { upsert: false });
            }

            await browser.close();
            browser.disconnect();

        } else if (res === -1) {
            // login failed - block happend
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_login: context_obj is null.");
            }

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_type: "code", blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res === 2) {
            // login failed - captcha happend
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_login: context_obj is null.");
            }
            let sitekey = await get_sitekey(page);
            if(sitekey == null) {
                throw new Error("Error in input_login: sitekey is null.");
            }

            context_obj.sitekey = sitekey

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_type: "captcha", blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res === 4) {
            // wrong credentials - need one more try
            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BROKEN_CREDENTIALS }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            await browser.close();
            browser.disconnect();

        } else if (res === -2) {
            // system error
            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });
            
            await browser.close();
            browser.disconnect();
        }

    } catch(err) {
        log.error("..... Error in input_login account._id: ..... ", account._id);
        log.error("..... Error in input_login: ..... ", err.stack);

        await models.Accounts.findOneAndUpdate({ _id: account._id, status: status_codes.IN_PROGRESS }, { status: status_codes.AVAILABLE }, { upsert: false });

        if(browser != null) {
            await browser.close();
            browser.disconnect();
        }
    }
}


const _get_current_cookie = async (page) => {
    // Get Session Cookies
    let newCookies = await page.cookies()
    if (!newCookies) {
        throw new Error("Can't get cookie.") //todo: don't throw error here (?)
    }

    return newCookies
}


module.exports = {
    input_data: input_data,
    input_login: input_login
  }
