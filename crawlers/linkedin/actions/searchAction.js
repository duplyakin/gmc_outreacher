const selectors = require(__dirname + "/.././selectors");
const action = require(__dirname + '/action.js');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');

class SearchAction extends action.Action {
  constructor(email, password, cookies, searchUrl, pageNum) {
    super(email, password, cookies);

    this.searchUrl = searchUrl;
    this.pageNum = pageNum;
  }

  async search() {
    await super.gotoChecker(this.searchUrl);

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
            if (item.querySelector(mySelectors.selector2) !== null && !item.querySelector(mySelectors.selector3).innerText.includes('LinkedIn')) {
              let str = item.querySelector(mySelectors.selector3).innerText;
              results.push({
                linkedin: item.href,
                first_name: str.substr(0, str.indexOf(' ')),
                last_name: str.substr(str.indexOf(' ') + 1),
              });
            }
          });
          return results;
        }, mySelectors);
        result_data.data.arr = result_data.data.arr.concat(newData);

        await super.autoScroll(this.page);

        //await this.page.waitForSelector(selectors.NEXT_PAGE_SELECTOR, { timeout: 5000 });
        //await this.page.waitFor(1000); // wait selectors loading 

        if (await this.page.$(selectors.NEXT_PAGE_SELECTOR) === null) {
          // TODO: add check-selector for BAN page
          // perhaps it was BAN
          result_data.code = MyExceptions.SearchActionError().code;
          result_data.raw = MyExceptions.SearchActionError('It is BAN (?) in searchAction: ' + err).error;
          console.log('something went wrong - selector not found!');
          break;
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
      //result_data.code = -1 //?
      result_data.data = JSON.stringify(result_data.data);
      return result_data;
      //throw MyExceptions.SearchActionError('It is BAN (?) in searchAction: '+ err);
    }

    console.log("..... User Data: .....", result_data)
    console.log("..... User Data: .....", result_data.data.arr)
    result_data.data = JSON.stringify(result_data.data);
    return result_data;
  }
}

module.exports = {
  SearchAction: SearchAction
}
