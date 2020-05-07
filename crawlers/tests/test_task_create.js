const workers = require(__dirname + '/../linkedin/workers/workers.js');


const SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=marketer&origin=GLOBAL_SEARCH_HEADER";
const CONNECT_URL = "https://www.linkedin.com/in/kirill-shilov-25aa8630/";
const MY_URL = "https://www.linkedin.com/in/grigoriy-polyanitsin/";

// test running

(async () => {
  console.log("..... test_task_create started: .....", __filename);

  let task = {
    email: "grinnbob@rambler.ru",
    password: "linked123",
    url: CONNECT_URL,
    pageNum: 9,
    text: 'test',
    connectName: 'Kirill Shilov',
  };

   // delete users from DB
      //await cookieModel.Cookies.deleteMany({username: this.email}, function (err) {
      //if (err) return handleError(err);
      // deleted!
      //console.log('........deleted in mongoDB.......');
      //});

   // add / update task in DB
   let task = await cookieModel.Cookies.findOne({ taskname: this.email });
   //console.log('........find object: ........', task);
   if (task === undefined || task === null) {
     // create new task
     let newCookiesDocument = await new cookieModel.Cookies({ taskname: this.email, expires: newExpires, data: newCookies });
     await newCookiesDocument.save(function (err) {
       if (err) return handleError(err);
       // saved!
       console.log('........saved in mongoDB.......');
     });
   } else {
     // update task info
     await task.updateOne({ expires: newExpires, data: newCookies }, function (err, res) {
       // updated!
       console.log('........updated in mongoDB.......');
     });
   }

})();
