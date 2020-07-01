const router = require('express').Router()

const models = require('../../../crawlers/models/models')
const status_codes = require('../../../crawlers/linkedin/status_codes')
const utils = require('./utils')

var log = require('loglevel').getLogger("o24_logger")


async function accountInput(req, res) {
    let credentials_id = req.body.credentials_id
    let input = req.body.input

    if(!credentials_id || !input) {
        log.error("..... accountInput: empty credentials_id or input, body: .....", req.body)
        return res.json({ code: -1 })
    }

    let account = null;

    try {
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.BLOCKED }, { status: status_codes.SOLVING_CAPTCHA }, { new: true, upsert: false });

        if (account == null) {
            log.debug('..... accountInput: There is no account with credentials_id = ' + credentials_id + ' and status = BLOCKED. It\'s may be SOLVING_CAPTCHA .....');
            return res.json({
                code: 1 // SOLVING_CAPTCHA
            });
        }

        // get connect to pupeeter and input data ASYNC
        utils.input_data(account, input);

        return res.json({
            code: 1 // SOLVING_CAPTCHA
        })

    } catch (err) {
        log.error("..... Error in accountInput: ..... ", err.stack);

        if (account != null) {
            log.error("..... Error in accountInput - credentials_id: ..... ", credentials_id);

            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.FAILED }, { upsert: false });
            return res.json({ code: -1 }) // system error
        }

        return res.json({
            code: 1 // SOLVING_CAPTCHA
        });
    }
}


async function accountStatus(req, res) {
    let credentials_id = req.body.credentials_id

    if(!credentials_id) {
        log.error("..... accountStatus: empty credentials_id, body: .....", req.body)
        return res.json({ code: -1 })
    }

    let account = await models.Accounts.findOne({ _id: credentials_id })

    if (account == null) {
        log.error("..... accountStatus - There is no account with credentials_id: ..... ", credentials_id);
        return res.json({ code: -1 })
    }

    if (account.status == null) {
        log.error("..... accountStatus - Empty account status in account: ..... ", account);
        return res.json({ code: -1 })
    }

    //log.debug("..... accountStatus status: ..... ", account.status);

    if (account.status == status_codes.BLOCKED) {
        if (account.blocking_type == null) {
            log.error("..... accountStatus: Empty account.blocking_type for account ..... ", credentials_id);
            return res.json({ code: -1 })
        }

        if (account.blocking_data == null) {
            log.error("..... accountStatus: Empty account.blocking_data for account ..... ", credentials_id);
            return res.json({ code: -1 })
        }

        if(account.blocking_type == "captcha") {
            if (account.blocking_data.sitekey == null) {
                log.error("..... accountStatus: Empty account.blocking_data.sitekey for account ..... ", credentials_id);
                return res.json({ code: -1 })
            }

            res.json({
                code: 2, // wait user action
                blocking_type: 'captcha',
                sitekey: account.blocking_data.sitekey,
            })
        } else if (account.blocking_type == "code") {
            if (account.blocking_data.screenshot == null) {
                log.error("..... accountStatus: Empty account.blocking_data.screenshot for account ..... ", credentials_id);
                return res.json({ code: -1 })
            }

            res.json({
                code: 2, // wait user action
                blocking_type: 'code',
                screenshot: account.blocking_data.screenshot,
            })
        } else {
            log.error("..... accountStatus: Uncknown account.blocking_type for account ..... ", credentials_id + " account.blocking_type: " + account.blocking_type);
            return res.json({ code: -1 })
        }

    } else if (account.status == status_codes.IN_PROGRESS || account.status == status_codes.SOLVING_CAPTCHA) {
        res.json({
            code: 1, // IN_PROGRESS
        })
    } else if (account.status == status_codes.AVAILABLE) {
        res.json({
            code: 0, // SUCCESS
        })
    } else if (account.status == status_codes.BROKEN_CREDENTIALS) {
        res.json({
            code: 4, // BROKEN_CREDENTIALS - NEED REPEAT
        })
    } else if (account.status == status_codes.FAILED) {
        log.error("..... accountStatus: This account with status = FAILED: ..... ", account);
        res.json({
            code: -1, // FAILED - need admin action
        })
    } else {
        log.error("..... accountStatus: Unexpected account.status: ..... ", account.status + "for account:" + account);
        res.json({ // todo: add new code here
            code: -1, // Unknown error - try again later
        })
    }
}


async function accountLogin(req, res) {
    let credentials_id = req.body.credentials_id
	let login = req.body.login
    let password = req.body.password

    if(!credentials_id) {
        log.error("..... accountLogin: Empty credentials_id .....")
        return res.json({ code: -1 }); // empty credentials_id
    }

    if(!login || !password) {
        log.error("..... accountLogin: Empty login or / and password .....")
        return res.json({ code: -2 }); // empty credentials
    }
    
	let account = null;
	try {
        // check if it BROKEN_CREDENTIALS account
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: { $in: [status_codes.BROKEN_CREDENTIALS, status_codes.AVAILABLE] }}, { _id: credentials_id, login: login, password: password, status: status_codes.IN_PROGRESS }, { new: true, upsert: true }); 

        log.debug("..... account status in accountLogin: ..... ", account.status);

		// login linkedin async
		utils.input_login(account);

        return res.json({ code: 1 }); // IN_PROGRESS
        
	} catch (err) { 
        log.error("..... Error in accountLogin: ..... ", err.stack);

	    if (account != null) {
            log.error(".... Error in accountLogin - credentials_id: ....", credentials_id);

            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.IN_PROGRESS }, { status: status_codes.AVAILABLE }, { upsert: false });
            return res.json({ code: -1 }) // system error
        }

        return res.json({ code: 1 }); // IN_PROGRESS 
    }
}


async function accountLoginCookie(req, res) {
    let credentials_id = req.body.credentials_id
    let li_at = req.body.li_at

    if(!credentials_id) {
        log.error("..... accountLogin: Empty credentials_id .....")
        return res.json({ code: -1 }); // empty credentials_id
    }

    if(!li_at) {
        log.error("..... accountLogin: Empty li_at .....")
        return res.json({ code: -2 }); // empty credentials
    }

    li_at = [{
        name : "li_at",
        value : li_at,
        domain : '.' + 'www.linkedin.com',
        path : "/",
        expires : Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
        size : (new TextEncoder().encode(li_at)).length,
        httpOnly : true,
        secure : true,
        session : false,
        sameSite : "None"
        }]
    
	let account = null;
	try {
        // check if it BROKEN_CREDENTIALS account
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: { $in: [status_codes.BROKEN_CREDENTIALS, status_codes.AVAILABLE] }}, { _id: credentials_id, cookies: li_at, status: status_codes.IN_PROGRESS }, { new: true, upsert: true }); 

        log.debug("..... account status in accountLogin: ..... ", account.status);

		// login linkedin async
		utils.input_login(account);

        return res.json({ code: 1 }); // IN_PROGRESS
        
	} catch (err) { 
        log.error("..... Error in accountLogin: ..... ", err.stack);

	    if (account != null) {
            log.error(".... Error in accountLogin - credentials_id: ....", credentials_id);

            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.IN_PROGRESS }, { status: status_codes.AVAILABLE }, { upsert: false });
            return res.json({ code: -1 }) // system error
        }

        return res.json({ code: 1 }); // IN_PROGRESS 
    }
}


router.post('/input/', accountInput)
router.post('/status/', accountStatus)
router.post('/login/', accountLogin)
router.post('/login/cookie/', accountLoginCookie)


module.exports = router