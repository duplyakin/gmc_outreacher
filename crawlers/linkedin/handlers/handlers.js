const { bull_workers } = require('./bullWorkersSettings.js');
const models = require("../../models/shared.js");
const workers = require('../workers/workers.js');
const cron = require('node-cron');

const actionKeys = require('./actionKeys.js');


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
          break;
      }
    } catch (err) {
      let err_result = {
        code: MyExceptions.HandlerError().code,
        raw: MyExceptions.HandlerError("HandlerError error: " + err).error
      };
      await models.TaskQueue.updateOne({ id: job.data.task_id }, { status: -1, result_data: err_result }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB save err: ' + err);
        // updated!
        console.log(success_db_save_text);
      });
    }
  });
}

async function taskStatusListener() {
  // start cron every minute
  cron.schedule("* * * * *", async () => {
    let tasks = await models.TaskQueue.find({ status: 1, action_key: { $in: actionKeys.action_keys }}, function (err, res) {
      if (err) throw MyExceptions.MongoDBError('MongoDB find TASKs err: ' + err);
    });

    if (Array.isArray(tasks) && tasks.length !== 0) {
      tasks.forEach(async (task) => {
        let data = {
          task_id: task.id,
          action_key: task.action_key,
        };
        await bull_workers.add(data);
      });

      console.log('CRON log - TASKs ADDED in queue');
    }
    console.log('this message logs every minute - CRON is active');
  });
}

module.exports = {
  taskStatusListener: taskStatusListener,
  bullConsumer: bullConsumer,
}

