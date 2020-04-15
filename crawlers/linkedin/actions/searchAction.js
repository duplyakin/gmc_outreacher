const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");

class SearchAction {
  constructor(searchUrl, pageNum, cookies) {
    this.searchUrl = searchUrl;
    this.pageNum = pageNum;

    this.cookies = JSON.parse(cookies);
  }

  async startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async closeBrowser(browser) {
    this.browser.close();
  }

  async search() {
    await this.page.goto(this.searchUrl);
    await this.page.waitForNavigation();

    let currentPage = 1;
    let data = [];
    while (currentPage <= this.pageNum) {
        let newData = await this.page.evaluate((selectors.SEARCH_ELEMENT_SELECTOR, selectors.LINK_SELECTOR, selectors.FULL_NAME_SELECTOR) => {

          let results = [];
          let items = document.querySelectorAll(selectors.SEARCH_ELEMENT_SELECTOR);

          items.forEach((item) => {
              if(item.querySelector(selectors.LINK_SELECTOR) !== null)
                results.push({
                    user_href:  item.href,
                    full_name:  item.querySelector(selectors.FULL_NAME_SELECTOR).innerText,
                });
          });
          return results;
        }, selectors.SEARCH_ELEMENT_SELECTOR, selectors.LINK_SELECTOR, selectors.FULL_NAME_SELECTOR);
        data = data.concat(newData);

        currentPage++;

        await autoScroll(this.page);

        await page.waitForSelector(selectors.NEXT_PAGE_SELECTOR);
        await page.click(selectors.NEXT_PAGE_SELECTOR);

        await this.page.waitForNavigation();
    }

    //console.log("..... User Data: .....", data)
    return data;
  }

  async autoScroll(page) {
      await page.evaluate(async () => {
          await new Promise((resolve, reject) => {
              var totalHeight = 0;
              var distance = 100;
              var timer = setInterval(() => {
                  var scrollHeight = document.body.scrollHeight;
                  window.scrollBy(0, distance);
                  totalHeight += distance;

                  if(totalHeight >= scrollHeight) {
                      clearInterval(timer);
                      resolve();
                  }
              }, 100);
          });
      });
  }

}
