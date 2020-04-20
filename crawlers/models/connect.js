// Импортировать модуль mongoose
var mongoose = require(__dirname + '/../node_modules/mongoose');
// Установим подключение по умолчанию
var mongoDB = 'mongodb://127.0.0.1/my_database';

mongoose.connect(mongoDB, function (err) {
 if (err) throw err;
 console.log('... Successfully connected to mongoDB ...');
});

// Позволим Mongoose использовать глобальную библиотеку промисов
mongoose.Promise = global.Promise;
// Получение подключения по умолчанию
var db = mongoose.connection;

// Привязать подключение к событию ошибки  (получать сообщения об ошибках подключения)
db.on('error', console.error.bind(console, '... MongoDB connection error: ...'));

module.exports = {
    mongoose: mongoose,
}
