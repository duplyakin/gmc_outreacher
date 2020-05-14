const puppeteer = require(__dirname + "/./../../node_modules/puppeteer");
const selectors = require(__dirname + "/.././selectors");
const LoginAction = require(__dirname + '/loginAction.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class SearchAction {
  constructor(email, password, cookies, searchUrl, pageNum) {
    this.email = email;
    this.password = password;
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
    this.browser.disconnect();
    this.browser.close();
  }

  // do 3 tries to connect URL or goto login
  async gotoCheckerThree(url) {
    for (let i = 0; i < 3; i++) {
      await this.page.goto(url);
      let current_url = await this.page.url();
      if (current_url.includes('login') || current_url.includes('signup')) {
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

    if (current_url.includes('login') || current_url.includes('signup')) {

      let loginAction = new LoginAction.LoginAction(this.email, this.password, this.cookies);
      await loginAction.setContext(this.context);

      let result = await loginAction.login();
      if (!result) {
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

    await this.page.waitForSelector(selectors.SEARCH_ELEMENT_SELECTOR, { timeout: 5000 });

    let currentPage = 1;
    let result_data = {
      code: 0,
      data: {
        arr: [],
        link: this.searchUrl
      }
    };
    let mySelectors = {
      selector1: selectors.SEARCH_ELEMENT_SELECTOR,
      selector2: selectors.LINK_SELECTOR,
      selector3: selectors.FULL_NAME_SELECTOR,
    };

    try {
      while (currentPage <= this.pageNum) {
        let newData = await this.page.evaluate((mySelectors) => {

          let results = [];
          let items = document.querySelectorAll(mySelectors.selector1);

          items.forEach((item) => {
            if (item.querySelector(mySelectors.selector2) !== null && !item.querySelector(mySelectors.selector3).innerText.includes('LinkedIn'))
              results.push({
                user_href: item.href,
                full_name: item.querySelector(mySelectors.selector3).innerText,
              });
          });
          return results;
        }, mySelectors);
        result_data.data.arr = result_data.data.arr.concat(newData);

        await this.autoScroll(this.page);

        //await this.page.waitForSelector(selectors.NEXT_PAGE_SELECTOR, { timeout: 5000 });
        //await this.page.waitFor(1000); // wait selectors loading 

        if (await this.page.$(selectors.NEXT_PAGE_SELECTOR) === null) {
          // TODO: add check-selector for BAN page
          // perhaps it was BAN
          result_data.code = MyExceptions.SearchActionError().code;
          result_data.raw = MyExceptions.SearchActionError('It is BAN (?) in searchAction: ' + err).error;
          console.log('something went wrong - selector not found!');
        }
        if (await this.page.$(selectors.NEXT_PAGE_MUTED_SELECTOR) !== null) {
          // all awailable pages has been scribed
          result_data.code = 1000;
          console.log('all contacts scribed!');
          break;
        }

        await this.page.click(selectors.NEXT_PAGE_SELECTOR);
        await this.page.waitFor(1000); // critical here! to remember last page link!
        result_data.data.link = await this.page.url();

        currentPage++;
      }
    } catch (err) {
      console.log("..... we catch it: .....", err);
      result_data.data = JSON.stringify(result_data.data);
      return result_data;
      //throw MyExceptions.SearchActionError('It is BAN (?) in searchAction: '+ err);
    }

    console.log("..... User Data: .....", result_data)
    //console.log("..... User Data: .....", result_data.data.arr)
    result_data.data = JSON.stringify(result_data.data);
    return result_data;
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

          if (totalHeight >= scrollHeight) {
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
