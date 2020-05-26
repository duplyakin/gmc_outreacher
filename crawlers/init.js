const handlers = require('./linkedin/handlers/handlers.js');

(async () => {
    console.log("..... init started: .....", __filename);
    try {
        await handlers.bullConsumer();
        await handlers.taskStatusListener();
    } catch (err) {
        console.log("..... handler error: .....", err);
    }

})();
