const log = require('bole')('customers/router')
const router = require('express').Router()

const models_shared = require('../../../crawlers/models/shared')
const models = require('../../../crawlers/models/models')
const status_codes = require('../../../crawlers/linkedin/status_codes')
const utils = require('./utils')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');


async function accountInput(req, res) {
    let credentials_id = req.body.credentials_id;
    let input = req.body.input;
    //console.log("accountInput started with body: ", input);

    if(!credentials_id || !input) {
        return res.json({ code: -1 })
    }

    let account = null;

    try {
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.BLOCKED }, { status: status_codes.SOLVING_CAPTCHA }, { new: true, upsert: false });

        if (account == null) {
            console.log('There is no account with credentials_id = ' + credentials_id + ' and status BLOCKED.');
            return res.json({
                code: 1 // IN_PROGRESS
            });
        }

        // get connect to pupeeter and input data ASYNC
        utils.input_data(account, input);

        return res.json({
            code: 1 // IN_PROGRESS
        })

    } catch (err) {
        console.log("..... Error in accountInput : ..... ", err.stack);

        if (account != null) {
            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.FAILED });
            return res.json({ code: -1 }) // system error
        }

        return res.json({
            code: 1 // IN_PROGRESS
        });
    }
}


async function accountStatus(req, res) {
    let credentials_id = req.body.credentials_id;

    let account = await models.Accounts.findOne({ _id: credentials_id });

    if (account == null) {
        console.log("..... There is no account with credentials_id: ..... ", credentials_id);
        return res.json({ code: -1 })
    }

    if (account.status == null) {
        console.log("..... There is no account status: ..... ", account);
        return res.json({ code: -1 })
    }
    console.log("..... status: ..... ", account.status);

    if (account.status == status_codes.BLOCKED) {
        if (account.blocking_data == null) {
            console.log("..... Empty account.blocking_data. ..... ", credentials_id);
            return res.json({ code: -1 })
        }

        if (account.blocking_data.screenshot == null) {
            console.log("..... Empty account.blocking_data.screenshot. ..... ", credentials_id);
            return res.json({ code: -1 })
        }

        res.json({
            code: 2, // wait user action
            screenshot: account.blocking_data.screenshot,
        })
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
        res.json({
            code: -1, // FAILED - need admin action
        })
    } else {
        console.log("..... Unexpected account.status: ..... ", account.status);
        res.json({ // todo: add new code here
            code: -1, // Unknown error - try again later
        })
    }
}


async function accountLogin(req, res) {
	let credentials_id = req.body.credentials_id;
	let login = req.body.login;
    let password = req.body.password;
    
    if(!login || !password) {
        return res.json({ code: -2 }); // empty credentials
    }

    if(!credentials_id) {
        return res.json({ code: -1 }); // empty credentials_id
    }

    
	let account = null;
	try {
        // check if it BROKEN_CREDENTIALS account
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: { $in: [status_codes.BROKEN_CREDENTIALS, status_codes.AVAILABLE] }}, { _id: credentials_id, login: login, password: password, status: status_codes.IN_PROGRESS }, { new: true, upsert: true }); 

        //console.log("..... account status in accountLogin : ..... ", account.status);

		// login linkedin async
		utils.input_login(account);

        return res.json({ code: 1 }); // IN_PROGRESS
        
	} catch (err) { 
        console.log("..... Error in accountLogin : ..... ", err.stack);

	    if (account != null) {
            console.log(".... account: ....", account);

            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.IN_PROGRESS }, { status: status_codes.AVAILABLE }, { upsert: false });
            return res.json({ code: -1 }) // system error
        }

        return res.json({ code: 1 }); // IN_PROGRESS 
    }
}



router.post('/input/', accountInput)
router.post('/status/', accountStatus)
router.post('/login/', accountLogin)


module.exports = router