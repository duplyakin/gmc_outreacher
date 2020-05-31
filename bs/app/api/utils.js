const puppeteer = require('puppeteer')
const links = require('../../../crawlers/linkedin/links')
const selectors = require('../../../crawlers/linkedin/selectors')

const found_form_and_input = async (page, input) => {

    let url = page.url();
    let res = false;

    if(url.includes(links.CHALLENGE_LINK)) {
        res = await resolve_challenge(page, input);

    } else if(url.includes(links.BAN_LINK)) {
        res = await resolve_ban(page, input);

    } else {
        console.log('UNCKNOWN page found: ', url);
        throw new Error('UNCKNOWN page found: ' + url);
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

      await page.click(selectors.VERIFICATION_PIN_SELECTOR);
      await page.keyboard.type(input);
      await page.click(selectors.VERIFICATION_PIN_BTN_SELECTOR);
      await page.waitFor(1000);

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

const page_connect = async (browser, validated_data) => {
    let contexts = await browser.browserContexts();
    if (!contexts){
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

    let pages = await found_context.pages();
    if (pages ==  null){
        throw new Error("Context doesn't have pages");
    }

    let page_url = validated_data.page_url;
    let found_page = null;
    for (page in pages){
        if (page.url() == page_url){
            found_page = page;
            break;
        }
    }


    if (!found_page){
        throw new Error("Can't find page by url", context_id);
    }

    return found_page;
}

const input_captcha = async (data, input) => {
    if (!input){
        throw new Error("Input can't be empty");
    }

    await validate_data(data)

    var browser = await puppeteer.connect({
        browserWSEndpoint: data.endpoint
    });

    let captcha_page = await page_connect(browser, data);
    if (!captcha_page){
        throw new Error("Can't connect to page");
    }

    let res = await found_form_and_input(captcha_page, input);

    return res;
}

const check_captcha_status = async (data, input) => {

}


module.exports.input_captcha = input_captcha
//module.exports.get_task = get_task
module.exports.check_captcha_status = check_captcha_status
