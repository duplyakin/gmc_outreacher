const handlers = require('./linkedin/handlers/handlers.js');
var log = require('loglevel').getLogger("o24_logger");

(async () => {
    try {
        var APP_ENV = process.env.APP_ENV;

        // 0 = for tests, 4 = for Production
        if (APP_ENV == 'Production') {
            log.setLevel("ERROR") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
        } else {
            log.setLevel("TRACE") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
        }
        
        log.debug("..... init started in mode: .....", process.env.APP_ENV)

        await handlers.bullConsumer()
        await handlers.taskStatusListener()

    } catch (err) {
        log.error("..... init error: .....", err)
    }

})();