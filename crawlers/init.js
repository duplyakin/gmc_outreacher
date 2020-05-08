const handlers = require(__dirname + '/linkedin/handlers/handlers.js');

(async () => {
    console.log("..... init started: .....", __filename);
    try {
        handlers.bullConsumer();
        handlers.taskStatusListener();
    } catch (err) {
        console.log("..... handler error: .....", err);
    }

})();
