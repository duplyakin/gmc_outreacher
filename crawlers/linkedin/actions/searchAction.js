const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');
var log = require('loglevel').getLogger("o24_logger");

class SearchAction extends action.Action {
  constructor(cookies, credentials_id, searchUrl, interval_pages) {
    super(cookies, credentials_id);

    this.searchUrl = searchUrl;
    this.interval_pages = interval_pages;
  }

  async search() {
    if(!this.searchUrl) {
      throw new Error('Empty search url.');
    }
    
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

      let mySelectors = {
        selector1: selectors.SEARCH_ELEMENT_SELECTOR,
        selector2: selectors.LINK_SELECTOR,
        selector3: selectors.FULL_NAME_SELECTOR,
        selector4: selectors.FIRST_DEGREE_SELECTOR,
      };

      while (currentPage <= this.interval_pages) {
        await super.autoScroll(this.page);

        // wait selector here
        //await super.check_success_selector(selectors.SEARCH_ELEMENT_SELECTOR, this.page);

        if (await this.page.$(selectors.SEARCH_ELEMENT_SELECTOR) == null) {
          // TODO: add check-selector for BAN page
          // perhaps it was BAN
          result_data.code = MyExceptions.SearchActionError().code;
          result_data.raw = MyExceptions.SearchActionError('something went wrong - NEXT_PAGE_SELECTOR not found! page.url: ' + this.page.url()).error;
          log.error('SearchAction: something went wrong - NEXT_PAGE_SELECTOR not found! page.url: ', this.page.url());
          break;
        }

        let newData = await this.page.evaluate((mySelectors) => {

          let results = [];
          let items = document.querySelectorAll(mySelectors.selector1);

          for(let item of items) {
            // don't add: noName LinkedIn members and 1st degree connections
            if (item.querySelector(mySelectors.selector2) !== null && !item.querySelector(mySelectors.selector3).innerText.includes('LinkedIn') && !item.querySelector(mySelectors.selector4).innerText.includes('1st')) {
              let str = item.querySelector(mySelectors.selector3).innerText;
              results.push({
                linkedin: item.href,
                first_name: str.substr(0, str.indexOf(' ')),
                last_name: str.substr(str.indexOf(' ') + 1),
              });
            }
          }
          return results;
        }, mySelectors);
        result_data.data.arr = result_data.data.arr.concat(newData);
        result_data.data.link = this.page.url();

        if (await this.page.$(selectors.NEXT_PAGE_SELECTOR) == null) {
          // TODO: add check-selector for BAN page
          // perhaps it was BAN
          result_data.code = MyExceptions.SearchActionError().code;
          result_data.raw = MyExceptions.SearchActionError('something went wrong - NEXT_PAGE_SELECTOR not found! page.url: ' + this.page.url()).error;
          log.error('SearchAction: something went wrong - NEXT_PAGE_SELECTOR not found! page.url: ', this.page.url());
          break;
        }

        // wait selector here
        //await super.check_success_selector(selectors.NEXT_PAGE_SELECTOR, this.page, result_data);

        if (await this.page.$(selectors.NEXT_PAGE_MUTED_SELECTOR) != null) {
          // all awailable pages has been scribed
          result_data.code = 1000
          log.debug('SearchAction: All awailable pages has been scribed!')
          break
        }

        await this.page.click(selectors.NEXT_PAGE_SELECTOR);
        await this.page.waitFor(2000) // critical here!?
        // here we have to check BAN page
        result_data.data.link = this.page.url() // we have to send NEXT page link in task

        currentPage++
      }
    } catch (err) {
      log.error("SearchAction: we catch something strange:", err)
      result_data.code = -1000
      result_data.data = JSON.stringify(result_data.data)
      return result_data
    }

    //log.debug("SearchAction: Reult Data: ", result_data)
    //log.debug("SearchAction: Users Data: ", result_data.data.arr)
    result_data.data = JSON.stringify(result_data.data);
    return result_data;
  }
}

module.exports = {
  SearchAction: SearchAction
}
