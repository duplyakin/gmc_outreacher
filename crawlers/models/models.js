let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let cookiesSchema = new Schema({
    username : String,

    expires : Number,

    data : Object,
});

module.exports = {
   Cookies : mongoose.model('Cookies', cookiesSchema),
}
