'use strict';

const loginAction = require(__dirname + '/../actions/loginAction')
const { logger } = require(__dirname + "/../../utils/logger");

async function login(task){
    
    let action;
    try{
        var credentials = task.credentials;
        
        action = new loginAction(credentials.email,
                                credentials.password);
        await action.init();
        await action.login();

        const cookies = action.cookies()
        console.log(cookies)

    }catch(err){
        logger.error("Can't login. Error: %s", err);
        // task.fail(err);
    }

    action.destroy();
}

var task = {
    credentials : {
        email : 'ks.shilov@gmail.com',
        password : 'Appatit_23843'
    }
}

login(task);