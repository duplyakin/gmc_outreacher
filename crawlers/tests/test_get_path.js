var log = require('loglevel').getLogger("o24_logger");


(async () => {
    try {
        var str = ' https://www.linkedin.com/in/kirill-shilov-25aa8630/?uadsfsdf=fasdfadsfdsf '

        var pathname = new URL(str).pathname
        pathname = pathname.split( '/' )[2]

        log.error("..... res: .....", pathname)
    } catch (err) {
        log.error("..... error: .....", err)
    } finally {
        log.error("..... finally: .....")
    }

})();