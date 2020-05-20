const { bull_workers } = require(__dirname + '/./bullWorkersSettings.js');
const taskModel = require(__dirname + "/../.././models/shared.js");
const workers = require(__dirname + '/.././workers/workers.js');
const cron = require(__dirname + '/../node-cron');

const MyExceptions = require(__dirname + '/../.././exceptions/exceptions.js');


async function bullConsumer() {
  bull_workers.process(async job => {
    try {
      switch (job.data.action_key) {
        case 'linkedin-check-reply':
          await workers.loginWorker(job.data.task_id);
          break;
        case 'linkedin-connect':
          await workers.connectWorker(job.data.task_id);
          break;
        case 'linkedin-send-message':
          await workers.messageWorker(job.data.task_id);
          break;
        case 'linkedin-check-accept':
          await workers.connectCheckWorker(job.data.task_id);
          break;
        case 'linkedin-search':
          await workers.searchWorker(job.data.task_id);
          break;
        case 'linkedin-parse-profile':
          await workers.scribeWorker(job.data.task_id);
          break;
        case 'linkedin-check-reply':
          await workers.messageCheck(job.data.task_id);
          break;
/*
        case 'finished':
          //await workers.loginWorker(job.task);
          break;
        case 'success':
          //await workers.loginWorker(job.task);
          break;
        case 'delay-linkedin':
          console.log("..... task.action_key: ..... delay-linkedin");
          break;
        case 'email-send-message':
          console.log("..... task.action_key: ..... email-send-message");
          break;
        case 'delay-email':
          console.log("..... task.action_key: ..... delay-email");
          break;
        case 'email-check-reply':
          console.log("..... task.action_key: ..... email-check-reply");
          break;
*/
        default:
          console.log("..... Incorrect task.action_key .....: ", job.data.action_key);
          // throw exception ?
      }
    } catch (err) {
      let err_result = {
        code: MyExceptions.HandlerError().code,
        raw: MyExceptions.HandlerError("HandlerError error: " + err).error
      };
      await taskModel.TaskQueue.updateOne({ id: job.data.task_id }, { status: -1, result_data: err_result }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB save err: ' + err);
        // updated!
        console.log(success_db_save_text);
      });
    }
  });
}

async function taskStatusListener() {
  // start cron every minute
  cron.schedule("* * * * *", () => {
    let tasks = await taskModel.TaskQueue.find({ status: 1, js_action: true }, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find err: ' + err);
    });
    if (Array.isArray(tasks) && tasks.length !== 0) {
      tasks.forEach((task) => {
        let data = {
          task_id: task.id,
          action_key: task.action_key,
        };
        await bull_workers.add(data);
      });

      console.log('this message logs every minute - TASKs ADDED in queue');
    }
  });
}

module.exports = {
  taskStatusListener: taskStatusListener,
  bullConsumer: bullConsumer,
}

