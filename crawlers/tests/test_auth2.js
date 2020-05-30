const puppeteer = require("puppeteer");

(async () => {
    console.log("..... test_auth started: .....", __filename);


        var endpoint = 'ws://127.0.0.1:58222/devtools/browser/1fd2d8aa-5101-490c-a632-854a4504c486';
        
        
        var browser = await puppeteer.connect({
            browserWSEndpoint: endpoint
        });

        let contexts = await browser.browserContexts();
        let c = contexts[1];
        
        let pages = await c.pages();
        let p = pages[0];
        
        let url = await p.url();
        console.log(url);
        //var page = await browser.newPage();
       // console.log( '..........here 1..........',  current_context)
       await p.goto('https://www.linkedin.com/uas/login');

       // let current_url = await page.url();

})();