var log = require('loglevel').getLogger("o24_logger");


(async () => {
    try {
        // info: https://learn.javascript.ru/url
        var str = ' https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97 '
        const SEARCH_URL_2 = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded=103644278&industryIncluded=80&logHistory=false&page=98&preserveScrollPosition=false&rsLogId=343536385&searchSessionId=DY4JJTjhRH6qJ2ZZIKMtXw%3D%3D";

        var res = new URL(SEARCH_URL_2).search

        str = "Текущая должность: Product Marketing Manager – Morningstar"
        res = str.split(': ')[1]
        //res = res.split(' – ')
        let res1 = res.substr(0, res.indexOf('–'))
        let res2 = res.substr(res.indexOf('–') + 2)

        log.error("..... res: .....", res1)
    } catch (err) {
        log.error("..... error: .....", err)
    } finally {
        log.error("..... finally: .....")
    }

})();