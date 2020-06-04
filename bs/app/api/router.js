const log = require('bole')('customers/router')
const router = require('express').Router()

const models_shared = require('../../../crawlers/models/shared')
const models = require('../../../crawlers/models/models')
const status_codes = require('../../../crawlers/linkedin/status_codes')
const utils = require('./utils')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');

/*
request:
outreacher24.com/bs/api/captcha/put
body = {
    task_id: ...
    user_data: ...
}

*/
async function accountInput(req, res) {
    let credentials_id = req.body.credentials_id;
    let user_data = req.body.user_data;

    if(!credentials_id || !user_data) {
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
        utils.input_data(account, user_data);

        return res.json({
            code: 1 // IN_PROGRESS
        })

    } catch (err) {
        console.log("..... Error in accountInput : ..... ", err.stack);

        if (account != null) {
            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.SOLVING_CAPTCHA }, { status: status_codes.FAILED });
            return res.json({ code: -1 }) // system error
        }
    }
}


/*
request:
outreacher24.com/bs/api/captcha/status?task_id=<task_id>

response json:
{
    code: 0,
    screenshot: <base64>
}
*/
async function accountStatus(req, res) {
    let credentials_id = req.params.credentials_id;

    let account = await models.Accounts.findOne({ _id: credentials_id });

    if (account == null) {
        console.log("..... There is no account with credentials_id._id: ..... ", credentials_id);
        return res.json({ code: -1 })
    }

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
            blocking_data: account.blocking_data.screenshot,
        })
    } else if (account.status == status_codes.IN_PROGRESS) {
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
    } 
    else {
        res.json({
            code: -1, // Unknown error - try again later
        })
    }
}


async function accountlogin(req, res) {
	let credentials_id = req.body.credentials_id;
	let login = req.body.login;
	let password = req.body.password;
    
    if(!credentials_id || !login || !password) {
        return res.json({ code: -2 }); // empty credentials
    }
    
	let account = null;
	try {
        // check if it BROKEN_CREDENTIALS account
        account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.BROKEN_CREDENTIALS }, {credentials_id: credentials_id, login: login, password: password, status: status_codes.IN_PROGRESS}, { new: true, upsert: false }); 
        
        if (account == null){
            // if not - create new AVAILABLE account
            account = await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.AVAILABLE }, {credentials_id: credentials_id, login: login, password: password, status: status_codes.IN_PROGRESS}, { new: true, upsert: true }); 
        }

        if (account == null){
            return res.json({ code: -1 }); // system error
        }

		// login linkedin async
		utils.input_login(account);

        return res.json({ code: 1 }); // IN_PROGRESS
        
	} catch (err) { 
        console.log("..... Error in loginLinkedin : ..... ", err.stack);

	    if (account != null) {
            await models.Accounts.findOneAndUpdate({ _id: credentials_id, status: status_codes.IN_PROGRESS }, { status: status_codes.AVAILABLE }, { upsert: false });
            return res.json({ code: -1 }) // system error
        }
    }
}



router.post('/input:credentials_id&user_data', accountInput)
router.post('/status/:credentials_id', accountStatus)
router.post('/login/:credentials_id&login&password', accountlogin)


module.exports = router