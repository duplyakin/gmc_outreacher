var express = require('express')

var app = express()

app.use(express.json())
app.use(express.urlencoded())


// Add headers
app.use(function (req, res, next) {

    /*
    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'http://192.168.43.202:8080');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    */
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE");
    res.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");


    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    //res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
})


// FINALLY, use any error handlers
//app.use(require('app/errors/not-found'))


app.use('/bs/api', require('./api/router')) // IT MUST BE HERE! DONT TOUCH.
// Export the app instance for unit testing via supertest
module.exports = app