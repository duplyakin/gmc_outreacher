const workers = require('./../linkedin/workers/workers.js');
var log = require('loglevel').getLogger("o24_logger");

// test

(async () => {
  log.setLevel("DEBUG");
  log.debug("..... test started: .....", __filename);

  let task = "000003a80a2de70af2b00000";

  //await workers.loginWorker(task);
  //await workers.searchWorker(task);
  //await workers.connectWorker(task);
  await workers.messageWorker(task);
  //await workers.scribeWorker(task);
  //await workers.messageCheckWorker(task);
  //await workers.connectCheckWorker(task);
  //await workers.visitProfileWorker(task);

})();