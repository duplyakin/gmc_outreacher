const puppeteer = require('puppeteer');
const C = require('./constants');
const USERNAME_SELECTOR = '#username';
const PASSWORD_SELECTOR = '#password';
const CTA_SELECTOR = '#app__container > main > div > form > div.login__form_action_container > button';
const PAGE_NUM = 1;
const = SIGNIN_LINK = "https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in"
const = SEARCH_LINK = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER"

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

  run(PAGE_NUM).then(console.log).catch(console.error);
}

(async () => {
  await playTest(SIGNIN_LINK);
  process.exit(1);
})();


function run (pagesToScrape) {
    return new Promise(async (resolve, reject) => {
        try {
            if (!pagesToScrape) {
                pagesToScrape = 1;
            }
            const page = await browser.newPage();
            await page.goto(SEARCH_LINK);
            let currentPage = 1;
            let urls = [];
            while (currentPage <= pagesToScrape) {
                let newUrls = await page.evaluate(() => {
                    let results = [];
                    let items = document.querySelectorAll('a.name actor-name');
                    items.forEach((item) => {
                        results.push({
                            url:  item.getAttribute('href'),
                            text: item.innerText,
                        });
                    });
                    return results;
                });
                urls = urls.concat(newUrls);
                if (currentPage < pagesToScrape) {
                    await Promise.all([
                        await page.click('a.morelink'),
                        await page.waitForSelector('a.storylink')
                    ])
                }
                currentPage++;
            }
            browser.close();
            return resolve(urls);
        } catch (e) {
            return reject(e);
        }
    })
}
