var log = require('bole')('customers/router')
var router = require('express').Router()

/*
request:
outreacher24.com/bs/api/captcha/put
body = {
    task_id: ...
    captcha_input: ...
}

*/
function captchaInput (req, res) {
    // get input connect to pupeeter and input
    let task_id = req.body.task_id;
    let captcha_input = req.body.captcha_input;

    /*
    find task in database...
    connect to pupetter
    enter input data

    if ok:
        res.json({code: 1})
    else:
        res.json({ 
            code: 0
            screenshot: task.result_data['blocking_data']['screenshot']
        })
    */

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
function captchaStatus (req, res) {
    let task_id = req.params.task_id;
    /* 
    Check status of the task in database.
    if status == NEED_USER_ACTION (6): 
        res.json({ 
            code: 0
            screenshot: task.result_data['blocking_data']['screenshot']
        })
    elif status == NEED_USER_ACTION_RESOLVED(7):
        res.json({code: 1})

    */
}


router.post('/captcha/put', captchaInput)
router.get('/captcha/status/:task_id', captchaStatus)


module.exports = router