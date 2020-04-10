const puppeteer = require("./node_modules/puppeteer");
const selectors = require(__dirname + "/./selectors");

export class SearchAction {
  constructor(searchUrl, pageNum, cookies) {
    this.searchUrl = searchUrl;
    this.pageNum = pageNum;

    this.cookies = JSON.parse(cookies);
  }

  async function startBrowser() {
    //this.browser = await puppeteer.launch({ headless: false });
    this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await page.setCookie(...this.cookies);
  }

  async function closeBrowser(browser) {
    this.browser.close();
  }

  async function search() {

    await this.page.goto(this.searchUrl);
    let currentPage = 1;
    let currentPageLink = this.searchUrl;
    if(!this.searchUrl.includes('&page='))
      currentPageLink = this.searchUrl + '&page=1';
    else {
      let i = this.searchUrl.indexOf('&page='); // todo: if there pages like 11, 123, 1234 - it will not work, juat for first 9 pages
      currentPage = this.searchUrl.charAt(i + 6);
    }
    let data = [];
    while (currentPage <= this.pageNum) {
        let newData = await this.page.evaluate(() => {
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
        });
        data = data.concat(newData);

        currentPage++;
        currentPageLink = currentPageLink.slice(0, -1) + currentPage.toString(); // add page number to the link, works for first 9 pages...

        await this.page.goto(currentPageLink);
    }

    //console.log("..... User Data: .....", data)
    return data;
  }
}
