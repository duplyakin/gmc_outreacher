var config = module.exports
var PRODUCTION = process.env.APP_ENV === 'Production'

config.express = {
  port: process.env.EXPRESS_PORT || 3000,
  ip: '127.0.0.1'
}

/*
config.mongodb = {
  port: process.env.MONGODB_PORT || 27017,
  host: process.env.MONGODB_HOST || 'localhost'
}
*/

if (PRODUCTION) {
  // for example
  config.express.ip = '0.0.0.0';
}

// config.db same deal
// config.email etc
// config.log

var log = require('loglevel').getLogger("o24_logger");

var APP_ENV = process.env.APP_ENV;

// 0 = for tests, 4 = for Production
if (APP_ENV == 'Production') {
    log.setLevel("ERROR") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
} else {
    log.setLevel("TRACE") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
}

log.error("... Server started in mode: ...", APP_ENV == null ? 'Test' : APP_ENV)
