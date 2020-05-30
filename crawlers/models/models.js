let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;

let cookiesSchema = new Schema({
    credentials_id : mongoose.ObjectId,

    expires : Number,

    data : Array,
});

let contextSchema = new Schema({
    credentials_id : mongoose.ObjectId,

    endpoint : String,

    context_id : String,

    url: String,

    screenshot: Buffer,
});

module.exports = {
   Cookies : mongoose.model('Cookies', cookiesSchema),
   Context : mongoose.model('Context', contextSchema),
}
