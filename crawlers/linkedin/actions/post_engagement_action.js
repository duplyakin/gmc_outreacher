const selectors = require("../selectors");
const action = require('./action.js');

const MyExceptions = require('../../exceptions/exceptions.js');
const utils = require("./utils");
var log = require('loglevel').getLogger("o24_logger");

class Post_engagement_action extends action.Action {
    constructor(cookies, credentials_id, url) {
        super(cookies, credentials_id)

        this.url = url
    }

    async engagement() {
        if (!this.url) {
            throw new Error('Empty post url.')
        }

        if (!utils.get_pathname_url(this.url).includes('posts')) {
            throw new Error('Incorrect post url:' + this.url) // add custom error here
        }

        await super.gotoChecker(this.url)

        var result_data = {
            code: 0,
            if_true: true,
            data: {
                post_url: this.url,
                arr: [],
            }
        }

        try {

            // get post general info
            result_data = await this._get_general_info(result_data)

            // get likers
            result_data = await this._get_likers(result_data)

            // get comenters
            result_data = await this._get_commenters(result_data)


        } catch (err) {

        }

        //log.debug("Post_engagement_action: Reult Data: ", result_data)
        log.debug("Post_engagement_action: Users Data: ", result_data.data.arr)
        log.debug("Post_engagement_action: contacts scribed:", result_data.data.arr.length)
        result_data.data = JSON.stringify(result_data.data)
        return result_data
    }


    async _get_general_info(result_data) {
        return result_data
    }


    async _get_likers(result_data) {
        return result_data
    }


    async _get_commenters(result_data) {
        // load all comments
        let check_selector = ''
        while (check_selector != null) {
            await utils.autoScroll(this.page)
            check_selector = await this.page.$(selectors.POST_MORE_COMMENTERS_BTN_SELECTOR)
            if (check_selector != null) {
                await this.page.click(selectors.POST_MORE_COMMENTERS_BTN_SELECTOR)
                await this.page.waitFor(2000)
            }
        }

        // load all sub-comments
        check_selector = ''
        while (check_selector != null) {
            check_selector = await this.page.$(selectors.POST_PREVIOUS_REPLIES_BTN_SELECTOR)
            if (check_selector != null) {
                await this.page.click(selectors.POST_PREVIOUS_REPLIES_BTN_SELECTOR)
                await this.page.waitFor(2000)
            }
        }

        let mySelectors = {
            selector1: selectors.POST_ELEMENT_SELECTOR,
            selector2: selectors.POST_COMMENTER_LINK_SELECTOR,
            selector3: selectors.POST_AUTHOR_TAG_SELECTOR,
            selector4: selectors.POST_COMMENTER_NAME_SELECTOR,
            selector5: selectors.POST_COMMENTER_JOB_SELECTOR,
        }

        result_data.data.arr = await this.page.evaluate((mySelectors) => {
            let results = new Set()
            let items = document.querySelectorAll(mySelectors.selector1)

            for (let item of items) {
                // don't scribe author of post
                if(item.querySelector(mySelectors.selector3) == null) {
                    let result = {}
                    let full_name = item.querySelector(mySelectors.selector4)
                    let linkedin = item.querySelector(mySelectors.selector2)
                    let full_job = item.querySelector(mySelectors.selector5)
                    result.tag = "comment"

                    if (full_name != null) {
                        full_name = full_name.innerText
                        if (full_name.includes(' ')) {
                          result.first_name = full_name.substr(0, full_name.indexOf(' '))
                          result.last_name = full_name.substr(full_name.indexOf(' ') + 1)
                        } else {
                          result.first_name = full_name
                        }
                      }
        
                      if (linkedin != null) {
                        result.linkedin = linkedin.href
                      }

                      if(full_job != null) {
                        full_job = full_job.innerText // -> "Founder & CDO at StreetPod International & Director RUA Architects"
                        if(full_job.includes(' at ')) {
                          result.job_title = full_job.substr(0, full_job.indexOf(' at ')) // -> "Founder & CDO "
                          result.job_name = full_job.substr(full_job.indexOf(' at ') + 4) // -> "StreetPod International & Director RUA Architects"
                        } else {
                          result.job_title = full_job // ? or new param
                        }
                      }

                    results.add(result)
                }
            }

            return [...results]
        }, mySelectors)

        return result_data
    }
}

module.exports = {
    Post_engagement_action: Post_engagement_action
}
