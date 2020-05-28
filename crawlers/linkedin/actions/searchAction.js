const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');

class SearchAction extends action.Action {
  constructor(email, password, li_at, cookies, credentials_id, searchUrl, page_count) {
    super(email, password, li_at, cookies, credentials_id);

    this.searchUrl = searchUrl;
    this.page_count = page_count;
  }

  async search() {
    await super.gotoChecker(this.searchUrl);

    let currentPage = 1;
    let result_data = {
      code: 0,
      if_true: true,
      data: {
        arr: [],
        link: this.searchUrl
      }
    };
    
    try {
      await this.page.waitForSelector(selectors.SEARCH_ELEMENT_SELECTOR, { timeout: 5000 });

      let mySelectors = {
        selector1: selectors.SEARCH_ELEMENT_SELECTOR,
        selector2: selectors.LINK_SELECTOR,
        selector3: selectors.FULL_NAME_SELECTOR,
      };

      while (currentPage <= this.page_count) {
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
        result_data.data.link = await this.page.url();

        await super.autoScroll(this.page);

        if (await this.page.$(selectors.NEXT_PAGE_SELECTOR) === null) {
          // TODO: add check-selector for BAN page
          // perhaps it was BAN
          result_data.code = MyExceptions.SearchActionError().code;
          result_data.raw = MyExceptions.SearchActionError('It is BAN (?) in searchAction.').error;
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
        await this.page.waitFor(1000); // critical here!?
        // here we have to check BAN page
        result_data.data.link = await this.page.url(); // we have to send NEXT page link in task

        currentPage++;
      }
    } catch (err) {
      console.log("..... we catch it: .....", err);
      //result_data.code = -1 // it should be = 0 !
      //result_data.if_true = false // ?
      result_data.data = JSON.stringify(result_data.data);
      return result_data;
      //throw MyExceptions.SearchActionError('It is BAN (?) in searchAction: '+ err);
    }

    //console.log("..... User Data: .....", result_data)
    //console.log("..... User Data: .....", result_data.data.arr)
    result_data.data = JSON.stringify(result_data.data);
    return result_data;
  }
}

module.exports = {
  SearchAction: SearchAction
}
