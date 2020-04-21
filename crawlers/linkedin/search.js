// URL for login: https://www.linkedin.com/login
// URL for search: https://www.linkedin.com/search/results/companies/?keywords=blockchain&page=100
// URL for 
// IF 
'use strict';

const Nick = require("nickjs");
const nick = new Nick({
    "debug": true,
    "printNavigation": true,
    "printResourceErrors": true,
    "printPageErrors": true,
    "timeout": 10000,
});

const cookies = [
    {
      name: 'JSESSIONID',
      value: '"ajax:6699346475309001165"',
      domain: '.www.linkedin.com',
      path: '/',
      expires: 1593008153.052888,
      size: 36,
      httpOnly: false,
      secure: true,
      session: false
    },
    {
      name: 'bcookie',
      value: '"v=2&f61b8e16-dd8a-40c3-8d0a-d6298f092080"',
      domain: '.linkedin.com',
      path: '/',
      expires: 1648346002.441529,
      size: 49,
      httpOnly: false,
      secure: true,
      session: false
    },
    {
      name: 'bscookie',
      value: '"v=1&20200326141810b11331fb-03f4-4f3e-892b-e801488e2834AQE6V-igwOYfmXQX0YGE6ace3f8wOJgj"',
      domain: '.www.linkedin.com',
      path: '/',
      expires: 1648346002.441579,
      size: 96,
      httpOnly: true,
      secure: true,
      session: false
    },
    {
      name: 'demdex',
      value: '87324122047005516674279547965179624501',
      domain: '.demdex.net',
      path: '/',
      expires: 1600784152.872453,
      size: 44,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg',
      value: '1',
      domain: '.linkedin.com',
      path: '/',
      expires: -1,
      size: 42,
      httpOnly: false,
      secure: false,
      session: true
    },
    {
      name: 'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg',
      value: '-1303530583%7CMCIDTS%7C18348%7CMCMID%7C87822805404193080884299579815917522942%7CMCAAMLH-1585836952%7C6%7CMCAAMB-1585836952%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1585239352s%7CNONE%7CvVersion%7C3.3.0',
      domain: '.linkedin.com',
      path: '/',
      expires: 1648304152,
      size: 266,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'aam_uuid',
      value: '87324122047005516674279547965179624501',
      domain: '.linkedin.com',
      path: '/',
      expires: 1587824152,
      size: 46,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'fr',
      value: '0fAughCgBrLjU4tpg..BefLmk...1.0.BefLmk.',
      domain: '.facebook.com',
      path: '/',
      expires: 1593008152.643831,
      size: 41,
      httpOnly: true,
      secure: true,
      session: false
    },
    {
      name: 'IDE',
      value: 'AHWqTUlnPG3BbsKNJQitRE7cy2LZv9apdILjH0kIq4qr_rH6oreESwWHh2-mVZ37',
      domain: '.doubleclick.net',
      path: '/',
      expires: 1648304152.781487,
      size: 67,
      httpOnly: true,
      secure: true,
      session: false
    },
    {
      name: 'dextp',
      value: '771-1-1585232152696|1123-1-1585232152799',
      domain: '.demdex.net',
      path: '/',
      expires: 1600784152,
      size: 45,
      httpOnly: false,
      secure: true,
      session: false,
      sameSite: 'None'
    },
    {
      name: 'dpm',
      value: '87324122047005516674279547965179624501',
      domain: '.dpm.demdex.net',
      path: '/',
      expires: 1600784152.8725,
      size: 41,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'personalization_id',
      value: '"v1_xXdwNv2tvx751uA6IkEN6Q=="',
      domain: '.twitter.com',
      path: '/',
      expires: 1648304153.050665,
      size: 47,
      httpOnly: false,
      secure: true,
      session: false
    },
    {
      name: 'liap',
      value: 'true',
      domain: '.linkedin.com',
      path: '/',
      expires: 1593008153.052721,
      size: 8,
      httpOnly: false,
      secure: true,
      session: false
    },
    {
      name: 'sl',
      value: 'v=1&JS_li',
      domain: '.www.linkedin.com',
      path: '/',
      expires: 1593008153.05279,
      size: 11,
      httpOnly: false,
      secure: true,
      session: false
    },
    {
      name: 'li_at',
      value: 'AQEDAQaQ6eYAatAWAAABcRc1Ku0AAAFxO0Gu7VYAFcofEYif1v4bEYtquWb36rQt8-OaXa_VR4aIKsXnaltoG0ik3078d3ZYE7M91P2ZQPn_Lfg2gG7alA_0W-M4dPILv-Xs1LyKF37POM6rd8JwnTS1',
      domain: '.www.linkedin.com',
      path: '/',
      expires: 1616768153.052855,
      size: 157,
      httpOnly: true,
      secure: true,
      session: false
    },
    {
      name: 'lang',
      value: 'v=2&lang=en-us',
      domain: '.linkedin.com',
      path: '/',
      expires: -1,
      size: 18,
      httpOnly: false,
      secure: true,
      session: true
    },
    {
      name: 'lidc',
      value: '"b=OB58:g=2028:u=226:i=1585232292:t=1585311704:s=AQH4vMJd86z2kd_WzZOd_0TdGNkbr8kr"',
      domain: '.linkedin.com',
      path: '/',
      expires: 1585311564.510148,
      size: 86,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'UIDR',
      value: '1585232295',
      domain: '.scorecardresearch.com',
      path: '/',
      expires: 1647440155.837313,
      size: 14,
      httpOnly: false,
      secure: false,
      session: false
    },
    {
      name: 'UID',
      value: '15A95a10188a13a5456b7cg1585232295',
      domain: '.scorecardresearch.com',
      path: '/',
      expires: 1647440155.837264,
      size: 36,
      httpOnly: false,
      secure: false,
      session: false
    }
  ]

const search_url = "https://www.linkedin.com/search/results/all/?keywords=%22founder%20blockchain%22&origin=GLOBAL_SEARCH_HEADER";

const set_cookie = async (cookies) => {
    console.log('Start')
  
    for (let index = 0; index < cookies.length; index++) {
        const cookie = cookies[index];
        await nick.setCookie(cookie)
    }
  
    console.log('End')
}
  


const scrape_profiles = (arg, done) => {
    // In this case, the current page uses a typical jQuery declared as $
    var data = []

    $(".search-result__wrapper").each((index, element) => {
        data.push({
          full_name: $(element).find(".name.actor-name").text(),
          url: $(element).find(".search-result__result-link.ember-view").attr("href")
        })
    });

    done(null, data);
}

async function get_profiles(tab){
    try {
        var profiles = await tab.evaluate(scrape_profiles, {})
        console.log("Scraped profiles:", profiles)
    } catch (err) {
        console.log("Something went wrong:", err)
    }

}


(async () => {

    const tab = await nick.newTab()
    
    await set_cookie(cookies);

	await tab.open(search_url)

    await tab.screenshot("search-page-initial.jpg")

	await tab.waitUntilVisible(".search-result__wrapper"); // Make sure we have loaded the page

	await tab.inject("https://code.jquery.com/jquery-3.4.1.slim.min.js"); // We're going to use jQuery to scrape

    await get_profiles(tab);
    
        // Iterate through pages
    const iter_throuh_pages = async (pages) => {
        
        for (let index = 0; index < pages.length; index++) {
            const num = pages[index];
            
            await tab.click("button.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view");
            await tab.waitUntilVisible("button.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view")

            var url = await tab.getUrl()
            console.log("....Url..", url)

            await get_profiles(tab);

        }
    }


    await iter_throuh_pages([1,2]);
    

})()
.then(() => {
	console.log("Job done!")
	nick.exit()
})
.catch((err) => {
	console.log(`Something went wrong: ${err}`)
	nick.exit(1)
})