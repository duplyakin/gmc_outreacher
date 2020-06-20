var log = require('loglevel').getLogger("o24_logger");


(async () => {
    try {
        var str = ' https://www.linkedin.com/search/results/all/?keywords=acronis&origin=GLOBAL_SEARCH_HEADER&page=97 '

        var pathname = new URL(str).pathname
        //pathname = pathname.split( '/' )[2]

        log.error("..... res: .....", pathname)
    } catch (err) {
        log.error("..... error: .....", err)
    } finally {
        log.error("..... finally: .....")
    }

})();