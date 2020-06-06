var express = require('express')

var app = express()

app.use('/bs/api', require('./api/router'))
app.use(express.json())
app.use(express.urlencoded())

/* DON'T WORK
var cors = require('cors');

// use it before all route definitions
app.use(cors({origin: 'http://192.168.43.202:8080'}));


// Add headers
app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'http://192.168.43.202:8080');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    //res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});
*/

// FINALLY, use any error handlers
//app.use(require('app/errors/not-found'))

// Export the app instance for unit testing via supertest
module.exports = app