let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;

let accountsSchema = new Schema({
    //credentials_id: mongoose.ObjectId,

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

    blocking_data: {
        type: Object,
        default: null,
    },
});

module.exports = {
    Accounts: mongoose.model('Accounts', accountsSchema),
}
