let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;

let cookiesSchema = new Schema({
    username : String,

    expires : Number,

    data : Object,
});

module.exports = {
   Cookies : mongoose.model('Cookies', cookiesSchema),
}
