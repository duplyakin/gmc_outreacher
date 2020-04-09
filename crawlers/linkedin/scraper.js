const puppeteer = require('puppeteer');
const C = require('./constants');
const fs = require('fs').promises; // for cookies
const USERNAME_SELECTOR = '#username';
const PASSWORD_SELECTOR = '#password';
const CTA_SELECTOR = '#app__container > main > div > form > div.login__form_action_container > button';
const PAGE_NUM = 3;
const SIGNIN_LINK = "https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in";
const SEARCH_LINK = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER";
//const SEARCH_LINK = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER&page=3";
const cookiesFilePath = './cookies.json';
const CONNECT_SELECTOR = '.pv-s-profile-actions.pv-s-profile-actions--connect';
const CONNECT_LINK = "https://www.linkedin.com/in/sergey-smirnov-72193989/";
const ADD_MSG_BTN_SELECTOR = '.mr1.artdeco-button.artdeco-button--muted';
const INVITE_TEXT = "Hi!";
const MSG_SELECTOR = '#custom-message';
const SEND_INVITE_TEXT_BTN_SELECTOR = '.ml1.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view';
const MORE_BTN_SELECTOR = '.ml2.pv-s-profile-actions__overflow-toggle';
const FOLLOW_SELECTOR = '.pv-s-profile-actions.pv-s-profile-actions--follow';

// test running
(async () => {
  const {browser, page} = await startBrowser();
  page.setViewport({width: 1366, height: 768});

  await loginLinked(browser, page, SIGNIN_LINK);
  //await searchLinked(browser, page, SEARCH_LINK);
  //await connectProfile(browser, page, CONNECT_LINK, INVITE_TEXT);
  await followProfile(browser, page, CONNECT_LINK);

  await closeBrowser(browser);

  process.exit(1);
})();

async function startBrowser() {
  const browser = await puppeteer.launch({ headless: false });
  //const browser = await puppeteer.launch();
  const page = await browser.newPage();
  return {browser, page};
}

async function closeBrowser(browser) {
  return browser.close();
}

async function loginLinked(browserGlobal, pageGlobal, url) {
  const browser = browserGlobal;
  const page = pageGlobal;

  // Load Session Cookies
  //const cookiesString = await fs.readFile(cookiesFilePath);
  //const cookies = JSON.parse(cookiesString);
  //await page.setCookie(...cookies);

  await page.goto(url);
  await page.click(USERNAME_SELECTOR);
  await page.keyboard.type(C.username);
  await page.click(PASSWORD_SELECTOR);
  await page.keyboard.type(C.password);
  await page.click(CTA_SELECTOR);
  await page.waitForNavigation();

  let is_phone = await check_phone_page(page);
  if (is_phone){
      await this.skip_phone(page);
  }
  // Save Session Cookies
  //newCookies = await page.cookies();
  //await fs.writeFile(cookiesFilePath, JSON.stringify(newCookies, null, 2));
}

async function skip_phone(page){
    await page.waitForSelector('.linkedin_phone_skip_div');
    await page.click('.linkedin_phone_skip_button');
}

async function check_phone_page(page){
    let url = await page.url();

    if (url.includes('.linkedin_phone_url')){
        return true;
    }

    return false;
}

async function searchLinked(browserGlobal, pageGlobal, url) {
  const browser = browserGlobal;
  const page = pageGlobal;

  await page.goto(url);
  let currentPage = 1;
  let currentPageLink = url;
  if(!url.includes('&page='))
    currentPageLink = url + '&page=1';
  else {
    let i = url.indexOf('&page='); // todo: if there pages like 11, 123, 1234 - it will not work, juat for first 9 pages
    currentPage = url.charAt(i+6);
  }
  let urls = [];
  while (currentPage <= PAGE_NUM) {
      let newUrls = await page.evaluate(() => {
        let results = [];
        let items = document.querySelectorAll('.search-result__wrapper .search-result__info a');
        items.forEach((item) => {
            if(item.querySelector('span > .actor-name') !== null)
              results.push({
                  user_href:  item.href,
                  full_name:  item.querySelector('span > .actor-name').innerText,
              });
        });
        return results;
      });
      urls = urls.concat(newUrls);

      currentPage++;
      currentPageLink = currentPageLink.slice(0, -1) + currentPage.toString(); // add page number to the link

      await page.goto(currentPageLink);
  }

  console.log("..... User Data: .....", urls)
}

async function connectProfile(browserGlobal, pageGlobal, url, text) {
  const browser = browserGlobal;
  const page = pageGlobal;

  await page.goto(url);
  await page.click(CONNECT_SELECTOR);
  //await page.waitForNavigation();
  await page.click(ADD_MSG_BTN_SELECTOR);
  await page.click(MSG_SELECTOR);
  await page.keyboard.type(text);
  await page.click(SEND_INVITE_TEXT_BTN_SELECTOR);

}

async function followProfile(browserGlobal, pageGlobal, url) {
  const browser = browserGlobal;
  const page = pageGlobal;

  await page.goto(url);
  await page.click(MORE_BTN_SELECTOR);
  await page.click(FOLLOW_SELECTOR);
  //await page.waitFor(100);
  await page.waitForNavigation();
}
