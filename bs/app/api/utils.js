const puppeteer = require('puppeteer')

const links = require('../../../crawlers/linkedin/links')
const selectors = require('../../../crawlers/linkedin/selectors')
const status_codes = require('../../../crawlers/linkedin/status_codes')

const models = require('../../../crawlers/models/models')
const models_shared = require('../../../crawlers/models/shared')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');


// -2 = system err, -1 = block, 0 = resolved
const found_form_and_input = async (page, input) => {
    if(page == null) {
        console.log('Empty page in found_form_and_input.');
        return -2;
    }

    let url = page.url();
    let res = -2;

    if(!url) {
        return -2;
    }

    if(url.includes(links.CHALLENGE_LINK)) {
        res = await resolve_challenge(page, input);

    } else if (url.includes(links.BAN_LINK)) {
        res = await resolve_ban(page, input);

    } else {
        console.log('UNCKNOWN page found: ', url);
        return -2;
    }

    return res;
}


// -2 = system err, -1 = block, 0 = resolved
const resolve_challenge = async(page, input) => {
    try {
        if(page == null) {
            console.log("..... Empty page in resolve_challenge. ..... ");
            return -2;
        }

        if(!input || input == '') {
            console.log("..... Input can't be empty in resolve_challenge. ..... ");
            //throw MyExceptions.EmptyInputError("Input can't be empty in resolve_challenge.");
            return -2;
        }

        try {
            await page.waitForSelector(selectors.VERIFICATION_PIN_SELECTOR, { timeout: 5000 });
            await page.waitForSelector(selectors.VERIFICATION_PIN_BTN_SELECTOR, { timeout: 5000 });
        } catch (err) {
            console.log("..... Challenge page selectors not found. ..... ");
            //throw new Error('Challenge page selectors not found: ' + err);
            return -2;
        }

        await page.click(selectors.VERIFICATION_PIN_SELECTOR);
        await page.keyboard.type(input);
        await page.click(selectors.VERIFICATION_PIN_BTN_SELECTOR);
        await page.waitFor(1000);

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

        return 0;

    } catch(err) {
        console.log("..... Error in resolve_challenge: ..... ", err.stack);
        return -2;
    }
}


const resolve_ban = async(page, input) => {
    return false;
}


const check_block_url = (url) => {
    if(!url) {
        throw new Error('Empty url.');
    }

    if(url.includes(links.BAN_LINK) || url.includes(links.CHALLENGE_LINK)) {
        console.log('check_block_url block happend: ', url);
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


// -2 = system err, -1 = block, 0 = resolved
const login = async(page, account) => {
    try {
        if(!account.login || !account.password) {
            console.log("Empty login or password in login().")
            return -2; 
        }

        if(page == null) {
            console.log("Empty page in login().")
            return -2;
        }

        await page.goto(links.SIGNIN_LINK);

        //await page.waitFor(1000);
        //console.log("..... account.login: ..... ", account.login);

        try {
            await page.waitForSelector(selectors.USERNAME_SELECTOR, { timeout: 5000 });
        } catch (err) {
            console.log("Login page is not available in login().")
            return -2;
        }

        await page.click(selectors.USERNAME_SELECTOR);
        await page.keyboard.type(account.login);
        await page.click(selectors.PASSWORD_SELECTOR);
        await page.keyboard.type(account.password);
        await page.click(selectors.CTA_SELECTOR);
        await page.waitFor(5000);

        try {
            //await page.waitForSelector(selectors.BLOCK_TOAST_SELECTOR, { timeout: 1000 }); // do smth // todo
        } catch (err) {
            console.log("Login FAILED - toast error.")
            return -2;
        }
    
        let current_url = page.url();

        if (check_phone_page(current_url)) {
            await skip_phone(page);
            current_url = page.url();
        }

        if (check_block_url(current_url)) {
            return -1; // block happend
        }

        if (current_url.includes(links.SIGNIN_SHORTLINK)) {
            return 1; // wrong credentials
        }

        return 0; // resolved
    } catch(err) {
        console.log("Error in login(): ", err.stack);
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

    await page.waitFor(10000); // wait 10 sec for lading and screenshot page
    let screenshot_str = await page.screenshot();

    let context_obj = {
      endpoint: browser.wsEndpoint(),
      context_id: context._id,
      page_url: page.url(),
      screenshot: screenshot_str,
    }
    
    console.log('get_context context_obj created: ', context_obj);
    return context_obj;
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
    if (contexts == null){
        throw new Error("Can't receive browser.browserContexts");
    }

    let found_context = null;
    for (cx in contexts){
        if (cx._id == context_id){
            found_context = cx;
            break;
        }
    }

    if (found_context == null){
        throw new Error("Can't find context by id: " + context_id);
    }

    return found_context;
}


const page_connect = async (context, page_url) => {
    if (context == null){
        throw new Error("Can't find context: " + context);
    }

    if(!page_url){
        throw new Error("Can't find page_url: " + page_url);
    }

    let pages = await context.pages();
    if (pages == null){
        throw new Error("Context doesn't have pages.");
    }

    let found_page = null;
    for (page in pages){ 
        if (page.url() == page_url){ // here can be several pages with same url
            found_page = page;
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
        console.log("..... Empty input in input_data. ..... ");
    }

    if(account == null) {
        console.log("..... Empty account in input_data. ..... ");
        throw new Error('Empty account in input_data.');
    }

    if (account.blocking_data == null) {
        console.log("..... There is no account.blocking_data. ..... ");
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

        if(res == 0) {
            // block resolved
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.ACTIVE }, { upsert: false });
            if(account.task_id != null) {
                await models_shared.TaskQueue.findOneAndUpdate({ _id: account.task_id }, { status: status_codes.NEED_USER_ACTION_RESOLVED }, { upsert: false });
            }
            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.AVAILABLE, task_id: null }, { upsert: false });

            await browser.close();
            browser.disconnect();

        } else if (res == -1) {
            // block didn't resolved
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_data: context_obj is null.");
            }

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res == -2) {
            // system error
            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });
            
            await browser.close();
            browser.disconnect();
        }

    } catch(err) {
        console.log("..... Error in input_data : ..... ", err.stack);

        await models.Accounts.findOneAndUpdate({ _id: account._id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.FAILED }, { upsert: false });

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
        browser = await puppeteer.launch({ headless: false }); // test mode
        //browser = await puppeteer.launch();
        context = await browser.createIncognitoBrowserContext();
        page = await context.newPage();

        let res = await login(page, account);

        if(res === 0) {
            // login success
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.ACTIVE }, { upsert: false });
            if(account.task_id != null) {
                await models_shared.TaskQueue.findOneAndUpdate({ _id: account.task_id }, { status: status_codes.NEED_USER_ACTION_RESOLVED }, { upsert: false });
            }

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
            await models.Accounts.findOneAndUpdate({ _id: account._id }, account_new, { upsert: false }); // upsert = false; because we have already created account object in DB

            await browser.close();
            browser.disconnect();

        } else if (res === -1) {
            // login failed - block happend
            console.log('input_login res = -1');
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_login: context_obj is null.");
            }

            await models.Accounts.findOneAndUpdate({ _id: account._id }, { status: status_codes.BLOCKED, blocking_data: context_obj }, { upsert: false });
            await models_shared.Credentials.findOneAndUpdate({ _id: account._id }, { status: status_codes.FAILED }, { upsert: false });

            browser.disconnect();

        } else if (res === 1) {
            // wrong credentials - need one more try
            let context_obj = await get_context(browser, context, page);
            if(context_obj == null) {
                throw new Error("Error in input_login: context_obj is null.");
            }

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
        console.log("..... Error in input_login : ..... ", err.stack);

        await models.Accounts.findOneAndUpdate({ _id: account._id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.FAILED }, { upsert: false });

        if(browser != null) {
            await browser.close();
            browser.disconnect();
        }
    }
}


const _get_current_cookie = async (page) => {
    // Get Session Cookies
    await page.goto(links.SIGNIN_LINK);
    await page.waitFor(1000);

    let newCookies = await page.cookies();
    if (!newCookies) {
        throw new Error("Can't get cookie.");
    }

    return newCookies;
}


module.exports = {
    input_data: input_data,
    input_login: input_login
  }
