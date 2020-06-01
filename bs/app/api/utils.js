const puppeteer = require('puppeteer')
const links = require('../../../crawlers/linkedin/links')
const selectors = require('../../../crawlers/linkedin/selectors')

const models_shared = require('../../../crawlers/models/shared')
const status_codes = require('../../../crawlers/linkedin/status_codes')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');


const found_form_and_input = async (page, input) => {

    let url = page.url();
    let res = false;

    if(url.includes(links.CHALLENGE_LINK)) {
        res = await resolve_challenge(page, input);

    } else if(url.includes(links.BAN_LINK)) {
        res = await resolve_ban(page, input);

    } else {
        console.log('UNCKNOWN page found: ', url);
        throw MyExceptions.UnknownPageError("Unknown error page: " + url);
    }

    return res;
}


const resolve_challenge = async(page, input) => {
    try {
        await page.waitForSelector(selectors.VERIFICATION_PIN_SELECTOR, { timeout: 5000 });
        await page.waitForSelector(selectors.VERIFICATION_PIN_BTN_SELECTOR, { timeout: 5000 });
    } catch (err) {
        throw new Error('Challenge page selectors not found: ' + err);
    }

    if(!input || input == '') {
        console.log("..... Input can't be empty in resolve_challenge. ..... ");
        throw MyExceptions.EmptyInputError("Input can't be empty in resolve_challenge.");
    }

    await page.click(selectors.VERIFICATION_PIN_SELECTOR);
    await page.keyboard.type(input);
    await page.click(selectors.VERIFICATION_PIN_BTN_SELECTOR);
    await page.waitFor(1000);

    //await page.goto(links.START_PAGE_LINK); // test - need it or not
    let current_url = page.url();
    if(current_url == links.START_PAGE_LINK) {
        return true; // resolved
    } else {
        return false; // something went wrong...
    }
}


const resolve_ban = async(page, input) => {
    return false;
}


const get_context = async(browser, context, page) => {
    if(browser == null) {
      throw new Error('Can\t get context. Browser is not defined.')
    }

    if(context == null) {
      throw new Error('Can\t get context. Context is not defined.')
    }

    if(page == null) {
      throw new Error('Can\t get context. Page is not defined.')
    }

    await page.waitFor(10000); // wait 10 sec for lading and screenshot page
    let screenshot_str = await page.screenshot();

    let context_obj = {
      endpoint: browser.wsEndpoint(),
      context_id: context._id,
      page_url: page.url(),
      screenshot: screenshot_str,
    }
    
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

    let screenshot = data.screenshot;
    if (!screenshot){
        throw new Error('DATA BROKEN: no screenshot');
    }

}


const context_connect = async (browser, validated_data) => {
    let contexts = await browser.browserContexts();
    if (contexts == null){
        throw new Error("Can't receive browser.browserContexts");
    }

    let context_id = validated_data.context_id;
    let found_context = null;
    for (cx in contexts){
        if (cx._id == context_id){
            found_context = cx;
            break;
        }
    }

    if (found_context == null){
        throw new Error("Can't find context by id", context_id);
    }

    return found_context;
}


const page_connect = async (context, validated_data) => {
    if (context == null){
        throw new Error("Can't find context by id", context_id);
    }

    let pages = await context.pages();
    if (pages == null){
        throw new Error("Context doesn't have pages");
    }

    let page_url = validated_data.page_url;
    let found_page = null;
    for (page in pages){ 
        if (page.url() == page_url){ // here can be several pages with same url
            found_page = page;
            break;
        }
    }

    if (found_page == null){
        throw new Error("Can't find page by url", context_id);
    }

    return found_page;
}


const input_captcha = async (task, input) => {
    if (!input){
        console.log("..... Empty input. ..... ");
    }

    if (task.result_data == null) {
        console.log("..... There is no task.result_data. ..... ", task_id);
        throw new Error('There is no task.result_data.');
    }

    if (task.result_data.blocking_data == null) {
        console.log("..... There is no task.result_data.blocking_data. ..... ", task_id);
        throw new Error('There is no task.result_data.blocking_data.');
    }

    await validate_data(task.result_data.blocking_data)

    var browser = await puppeteer.connect({
        browserWSEndpoint: data.endpoint
    });

    let context = await context_connect(browser, data);
    if (context == null){
        throw new Error("Can't connect to context");
    }
    let page = await page_connect(context, data);
    if (page == null){
        throw new Error("Can't connect to page");
    }

    let res = await found_form_and_input(page, input);

    if(res) {
        await models_shared.TaskQueue.findOneAndUpdate({ _id: task._id }, { status: status_codes.NEED_USER_ACTION_RESOLVED });
    } else {
        let context_obj = await get_context(browser, context, page);
        if(context_obj == null) {
            throw new Error("Error in input_captcha: context_obj is null.");
        }
        let result_data = {
            code: -1,
            raw: 'Block error is NOT resolved.',
            blocking_data: context_obj,
          }
        await models_shared.TaskQueue.findOneAndUpdate({ _id: task._id }, { status: status_codes.NEED_USER_ACTION, result_data: result_data });
    }
}

const check_captcha_status = async (data, input) => {

}


module.exports.input_captcha = input_captcha
//module.exports.get_task = get_task
module.exports.check_captcha_status = check_captcha_status
