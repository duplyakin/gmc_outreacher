const workers = require(__dirname + '/../linkedin/workers/workers.js');

const myCookies = {
  username: "grinnbob@rambler.ru",
  expires: 1618056891.724137,
  data: [
    {
      "name": "lidc",
      "value": "\"b=OGST04:g=1942:u=1:i=1587146277:t=1587232677:s=AQHe2HR9u3691kEFWgcghUnQqA7gLp5k\"",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1587232676.389235,
      "size": 86,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "UserMatchHistory",
      "value": "AQIvh1ECsH7PhQAAAXGJSkKb6p9U6r15K4CeZ96fD4II-yEWW-AlbGaMyalR-X8AFw1N3jwIa50f9eCnJRw7ZxBhPYh6jS_YengLnQE",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1589738276.20355,
      "size": 119,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "li_oatml",
      "value": "AQH1H1VGcNhCZAAAAXGJSkJBYME5IU6-CiZjjc8Y8TE0Q7PbUID6jmS5dPHAGd-2_eT13zP1Y4EEFkEh8PMvL7uGLB7yzly1",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1589738276.130973,
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
      "expires": 1587146875,
      "size": 5,
      "httpOnly": false,
      "secure": false,
      "session": false
    },
    {
      "name": "bscookie",
      "value": "\"v=1&20200417175751cdf97d7a-a8d9-43d7-8831-b22cb62b4c40AQED7zjNNCARFQ1McdX2xzYDVWffRHx6\"",
      "domain": ".www.linkedin.com",
      "path": "/",
      "expires": 1650260122.827247,
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
      "expires": 1589738269.827293,
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
      "expires": 1589738269.827312,
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
      "expires": 1594922271.188026,
      "size": 8,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
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
      "value": "v=1&oK09k",
      "domain": ".www.linkedin.com",
      "path": "/",
      "expires": 1594922271.187992,
      "size": 11,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "li_at",
      "value": "AQEDARcxwXEE7A5uAAABcYlKLtcAAAFxrVay104AD_sJ-krUSLzyPHpH0pnks373U_Js1c1VYse00AO48jv_hXpNZOFJ2LMj14eJ4WO_cUfigEpkG-NOunEU-puzeSq2u337V9XtORTzPvib6TzpLKDR",
      "domain": ".www.linkedin.com",
      "path": "/",
      "expires": 1618682271.188044,
      "size": 157,
      "httpOnly": true,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "JSESSIONID",
      "value": "\"ajax:8209290789964582145\"",
      "domain": ".www.linkedin.com",
      "path": "/",
      "expires": 1594922271.188127,
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
      "expires": 1618682270.827271,
      "size": 6,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "_ga",
      "value": "GA1.2.1498332345.1587146276",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1650218275,
      "size": 30,
      "httpOnly": false,
      "secure": false,
      "session": false
    },
    {
      "name": "bcookie",
      "value": "\"v=2&2793d8be-3ccd-4c71-8223-976e4cf29008\"",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1650260122.827215,
      "size": 49,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "_guid",
      "value": "f34e5c4f-9c47-4119-882d-617b86a40703",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1594922276.203498,
      "size": 41,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    },
    {
      "name": "UserMatchHistory",
      "value": "AQKiogVTua5PSAAAAXGJSj0FeTXvQDu6nficVc-VY72h6C1eLUAEkOKi77UHQfB72Z5ztx74sMw3l6-2taPZF-gp-j7iSnSBpFewnirp76Ytfr2g2rjjQdZMyjqQg9yjCrpZaVbBHRy-1kCVqrq-huMDMGAGWSHg796A-VMKfU_CAWN5EC6IqJpQytN4db1DYIY3aA",
      "domain": ".www.linkedin.com",
      "path": "/",
      "expires": 1589738275,
      "size": 214,
      "httpOnly": false,
      "secure": true,
      "session": false,
      "sameSite": "None"
    }
  ],
};

const SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";

// test running

(async () => {
  console.log("..... test started: .....", __filename);

  let task = {
    email: "grinnbob@rambler.ru",
    password: "linked123",
    url: SEARCH_URL,
    cookies: myCookies,
    pageNum: 9,
  };

  //await workers.loginWorker(task);
  await workers.searchWorker(task);

})();
