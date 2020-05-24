let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;

let cookiesSchema = new Schema({
    credentials_id : mongoose.ObjectId,

    expires : Number,

    data : Array,
});

module.exports = {
   Cookies : mongoose.model('Cookies', cookiesSchema),
}
