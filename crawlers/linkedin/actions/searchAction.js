const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

class SearchAction {
  constructor(email, password, cookies, searchUrl, pageNum) {
    this.email = email;
    this.password = password;
    //this.cookies = JSON.parse(cookies);
    this.cookies = cookies;

    this.searchUrl = searchUrl;
    this.pageNum = pageNum;
  }

  async startBrowser() {
    this.browser = await puppeteer.launch({ headless: false });
    //this.browser = await puppeteer.launch();
    this.context = await this.browser.createIncognitoBrowserContext();
    this.page = await this.context.newPage();
    await this.page.setCookie(...this.cookies);
  }

  async closeBrowser(browser) {
    this.browser.close();
  }

  // do 3 tries to connect URL or goto login
  async gotoCheckerThree(url) {
    for(let i = 0; i < 3; i++) {
      await this.page.goto(url);
      let current_url = await this.page.url();
      if(current_url.includes('login') || current_url.includes('signup')) {
        let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
        await loginAction.startBrowser();
        await loginAction.login();
      } else {
        return true;
      }
    }
    return false;
    // TODO: throw exception
  }

  // do 1 trie to connect URL or goto login
  async gotoChecker(url) {
    await this.page.goto(url);
    let current_url = await this.page.url();
    if(current_url.includes('login') || current_url.includes('signup')) {
      let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
      await loginAction.setContext(this.context);
      let result = await loginAction.login();
      if(!result) {
        // TODO: throw exception
        return false;
      } else {
        await this.page.goto(url);
        return true;
      }
    } else {
      return true;
    }
  }

  async search() {
    await this.gotoChecker(this.searchUrl);
    await this.page.waitForSelector(selectors.SEARCH_ELEMENT_SELECTOR);

    let currentPage = 1;
    let data = [];
    let mySelectors = {
      selector1: selectors.SEARCH_ELEMENT_SELECTOR,
      selector2: selectors.LINK_SELECTOR,
      selector3: selectors.FULL_NAME_SELECTOR,
    };
    while (currentPage <= this.pageNum) {
        let newData = await this.page.evaluate((mySelectors) => {

          let results = [];
          let items = document.querySelectorAll(mySelectors.selector1);

          items.forEach((item) => {
              if(item.querySelector(mySelectors.selector2) !== null)
                results.push({
                    user_href:  item.href,
                    full_name:  item.querySelector(mySelectors.selector3).innerText,
                });
          });
          return results;
        }, mySelectors);
        data = data.concat(newData);

        currentPage++;

        await this.autoScroll(this.page);

        await this.page.waitForSelector(selectors.NEXT_PAGE_SELECTOR);
        await this.page.click(selectors.NEXT_PAGE_SELECTOR);

        //await this.page.waitForNavigation();
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

module.exports = {
    SearchAction: SearchAction
}
