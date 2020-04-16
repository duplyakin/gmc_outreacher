const workers = require(__dirname + '/workers/workers.js');

const myCookies = [
  {
    "name": "lidc",
    "value": "\"b=VB53:g=2624:u=29:i=1586520891:t=1586607042:s=AQEGLBNtBZFK46tpyKtj08EQC2ZZEWvA\"",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1586607043.770101,
    "size": 85,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "UserMatchHistory",
    "value": "AQJ7uMTUgoSINwAAAXFkA7O-i2S7WQR3DxtxR_TZEHiCN0ulh0Mu_nxOlL5fW61_TxNO07u3f3BvzszV9NTdh4kCyPehanUyFwv2pD0",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1589112897.295887,
    "size": 119,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "li_oatml",
    "value": "AQGSyI9JUYL20QAAAXFkA7N-8sNl_J2_Gwcf6FduSdtSvIK7Z9r8VU9myBYolnGMwpBz4q6ytb41Z61lGBhDIobWheLcucTk",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1589112897.225405,
    "size": 104,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "_gat",
    "value": "1",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1586521496,
    "size": 5,
    "httpOnly": false,
    "secure": false,
    "session": false
  },
  {
    "name": "lang",
    "value": "v=2&lang=en-us",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": -1,
    "size": 18,
    "httpOnly": false,
    "secure": true,
    "session": true,
    "sameSite": "None"
  },
  {
    "name": "sl",
    "value": "v=1&jVU-X",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1594296891.724158,
    "size": 11,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "bscookie",
    "value": "\"v=1&20200410121449ba6dcd28-a972-491e-8def-f1c94fa28874AQFR8C2Ki8OXa8P0A-EPXh-QujGHoF5d\"",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1649634742.613966,
    "size": 96,
    "httpOnly": true,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "lissc1",
    "value": "1",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1589112890.614017,
    "size": 7,
    "httpOnly": true,
    "secure": true,
    "session": false,
    "sameSite": "Lax"
  },
  {
    "name": "lissc2",
    "value": "1",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1589112890.614036,
    "size": 7,
    "httpOnly": true,
    "secure": true,
    "session": false
  },
  {
    "name": "liap",
    "value": "true",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1594296891.724104,
    "size": 8,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "li_at",
    "value": "AQEDARcxwXEElgG3AAABcWQDna4AAAFxiBAhrk0ApLp67bVy0VtuVcidI-pKw58VnBlEtaNkJLBE_H6d3IfZMCmGC9bPgqrZOz1r6n8oQ9EqC2OZUfOkJQIOc8IyNezO3w2qN2eYWxi6G9txl96ePN1O",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1618056891.724137,
    "size": 157,
    "httpOnly": true,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "JSESSIONID",
    "value": "\"ajax:8885430537912243318\"",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1594296891.724232,
    "size": 36,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "lissc",
    "value": "1",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1618056890.61399,
    "size": 6,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "_ga",
    "value": "GA1.2.1749558115.1586520897",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1649592896,
    "size": 30,
    "httpOnly": false,
    "secure": false,
    "session": false
  },
  {
    "name": "bcookie",
    "value": "\"v=2&4bc20fb2-8d13-438c-84b3-b040963dacda\"",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1649634742.613933,
    "size": 49,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "_guid",
    "value": "c74d2322-d7b5-4550-a0fe-bc5948a655cc",
    "domain": ".linkedin.com",
    "path": "/",
    "expires": 1594296897.295835,
    "size": 41,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  },
  {
    "name": "UserMatchHistory",
    "value": "AQLirvg8nDGU0wAAAXFkA61x3AZ67H5oh0rmu0kXZYSDU8V1J-uqvHiV_--ob7QXDhIOE5Y6GJC4k8OiD13m40lfaSPYfG3-DpR7gzhQ8hkYb92Oi7rpnVapxEF_NQpFwYC7sscfUuSBj9qvPmY4DmuO4qEGRt2G9YkyDxcZYc7wWj4rBnNITS_Kjft4DsJSEkg-bA",
    "domain": ".www.linkedin.com",
    "path": "/",
    "expires": 1589112896,
    "size": 214,
    "httpOnly": false,
    "secure": true,
    "session": false,
    "sameSite": "None"
  }
]

// test running

  console.log("..... current dirname: .....", __dirname);

  let task = {
    email: "grinnbob@rambler.ru",
    password: "linked123",
    url: "https://www.linkedin.com/in/kirill-shilov-25aa8630/",
    cookies: myCookies,

  }

  workers.loginWorker(task);
  //console.log("..... current dirname: .....", task);
