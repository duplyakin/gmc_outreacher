var express = require('express')

var app = express()

app.use('/bs/api', require('./api/router'))
app.use(express.json())
app.use(express.urlencoded())

// FINALLY, use any error handlers
//app.use(require('app/errors/not-found'))

// Export the app instance for unit testing via supertest
module.exports = app