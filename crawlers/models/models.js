let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;


let accountsSchema = new Schema({
    task_id: {
        type: mongoose.ObjectId,
        default: null,
    },

    status: {
        type: Number,
        default: 0,
    },

    login: String,

    password: String,

    expires: Number,

    cookies: Array,

    blocking_type: {
        type: String,
        default: null,
    },

    blocking_data: {
        type: Object,
        default: null,
    },

});


let cronLockSchema = new Schema({
    lock: {
        type: String,
        unique: true, // it's needed to prevent creating new documents. always 1 document with lock = cron_lock
    },

    ack: {
        type: Number,
        default: 0,
    },

});

module.exports = {
    Accounts: mongoose.model('Accounts', accountsSchema),
    CronLock: mongoose.model('CronLock', cronLockSchema),
}
