const puppeteer = require('puppeteer');
const C = require('./constants');
const USERNAME_SELECTOR = '#username';
const PASSWORD_SELECTOR = '#password';
const CTA_SELECTOR = '#app__container > main > div > form > div.login__form_action_container > button';

async function startBrowser() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  return {browser, page};
}

async function closeBrowser(browser) {
  return browser.close();
}

async function playTest(url) {
  const {browser, page} = await startBrowser();
  page.setViewport({width: 1366, height: 768});
  await page.goto(url);
  await page.click(USERNAME_SELECTOR);
  await page.keyboard.type(C.username);
  await page.click(PASSWORD_SELECTOR);
  await page.keyboard.type(C.password);
  await page.click(CTA_SELECTOR);
  await page.waitForNavigation();
  //await page.screenshot({path: 'linkedin.png'});
}

(async () => {
  await playTest("https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in");
  process.exit(1);
})();


let username = process.argv[2];

let scrape = async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    await page.goto('https://www.linkedin.com/in/'+ username +'/');
    await page.waitFor(1000);
    await page.screenshot({path: 'linkedin.png'});
    const result = await page.evaluate(() => {

        let name = document.querySelector('#name').innerText;
        let title = document.querySelector('.headline').innerText;
        let summary = document.querySelector('.headline').childNodes[0].innerText;

        return {
            "name": name,
            "title": title,
            "summary": summary
        }

    });

    browser.close();
    return result;
};

scrape().then((value) => {
    console.log(value);
});
