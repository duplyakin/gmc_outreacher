const log = require('bole')('customers/router')
const router = require('express').Router()

const models_shared = require('../../../crawlers/models/shared')
const status_codes = require('../../../crawlers/linkedin/status_codes')
const utils = require('./utils')

const MyExceptions = require('../../../crawlers/exceptions/exceptions.js');

/*
request:
outreacher24.com/bs/api/captcha/put
body = {
    task_id: ...
    captcha_input: ...
}

*/
async function captchaInput(req, res) {
    try {
        let task_id = req.body.task_id;
        let captcha_input = req.body.captcha_input;

        let task = await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id, status: status_codes.NEED_USER_ACTION }, { status: status_codes.NEED_USER_ACTION_PROGRESS }, { new: true });

        if (task == null) {
            console.log('There is no task with task._id = ' + task_id + ' and status NEED_USER_ACTION.');
            return res.json({
                code: 1 // IN_PROGRESS
            });
            //throw new Error('There is no task with task._id = ' + task_id + ' and status NEED_USER_ACTION.');
        }

        if (!captcha_input) {
            throw new Error("Input can't be empty");
        }

        // get connect to pupeeter and input data
        utils.input_captcha(task, captcha_input);

        return res.json({
            code: 1 // IN_PROGRESS
        })

    } catch (err) {
        console.log("..... Error in captchaInput : ..... ", err);

        if(err.code != null) {
            await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { status: status_codes.NEED_USER_ACTION });
            return res.json({ code: err.code })
        } else {
            await models_shared.TaskQueue.findOneAndUpdate({ _id: task_id }, { status: status_codes.FAILED });
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
async function captchaStatus(req, res) {
    let task_id = req.params.task_id;

    let task = await models_shared.TaskQueue.findOne({ _id: task_id, ack: 0 });

    if (task == null) {
        console.log("..... There is no task with task._id : ..... ", task_id);
        return res.json({ code: -2 })
        //throw new Error('There is no task with task._id = ' + task_id);
    }

    if (task.status == status_codes.NEED_USER_ACTION) {
        if (task.result_data == null) {
            console.log("..... There is no task.result_data. ..... ", task_id);
            return res.json({ code: -2 })
            //throw new Error('There is no task.result_data.');
        }

        if (task.result_data.blocking_data == null) {
            console.log("..... There is no task.result_data.blocking_data. ..... ", task_id);
            return res.json({ code: -2 })
            //throw new Error('There is no task.result_data.blocking_data.');
        }

        res.json({
            code: -1, // wait user action
            blocking_data: task.result_data.blocking_data,
        })
    } else if (task.status == status_codes.NEED_USER_ACTION_PROGRESS) {
        res.json({
            code: 1,  // IN_PROGRESS
        })
    } else if (task.status == status_codes.NEED_USER_ACTION_RESOLVED) {
        res.json({
            code: 0, // SUCCESS
        })
    } else {
        res.json({
            code: -2, // Unknown error - try again later
        })
    }

    return res;
}


router.post('/captcha/put', captchaInput)
router.get('/captcha/status/:task_id', captchaStatus)


module.exports = router