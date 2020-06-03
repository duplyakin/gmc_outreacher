const { bull_workers } = require('./bullWorkersSettings.js');

const models_shared = require("../../models/shared.js");
const workers = require('../workers/workers.js');

const cron = require('node-cron');

const actionKeys = require('./actionKeys.js');
const status_codes = require('../status_codes')


async function bullConsumer() {
  bull_workers.process(async job => {
    try {
      switch (job.data.action_key) {
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
          await workers.messageCheckWorker(job.data.task_id);
          break;
        case 'linkedin-profile-view':
          await workers.visitProfileWorker(job.data.task_id);
          break;

        default:
          break;
      }
    } catch (err) {
      console.log('Bull queue - something went wrong: ', err);

      let err_result = {
        code: MyExceptions.HandlerError().code,
        raw: MyExceptions.HandlerError("HandlerError error: " + err).error
      };
      
      await models_shared.TaskQueue.updateOne({ _id: job.data.task_id }, { status: -1, result_data: err_result }, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB save err: ' + err);
        // updated!
        console.log('MongoDB save success.');
      });
    }
  });
}

async function taskStatusListener() {
  var handler_lock = 0;

  // start cron every minute
  cron.schedule("* * * * *", async () => {

    if(handler_lock === 0) {
      let tasks = await models_shared.TaskQueue.find({ status: status_codes.IN_PROGRESS, is_queued: 0, action_key: { $in: actionKeys.action_keys }}, function (err, res) {
        if (err) throw MyExceptions.MongoDBError('MongoDB find TASKs err: ' + err);
      });

      if (Array.isArray(tasks) && tasks.length !== 0) {
        handler_lock = 1;

        tasks.forEach(async (task) => {
          let data = {
            task_id: task.id,
            action_key: task.action_key,
          };
          await bull_workers.add(data);

          await models_shared.TaskQueue.findOneAndUpdate({ _id: task.id }, { is_queued: 1 }, function (err, res) {
            if (err) throw MyExceptions.MongoDBError('MongoDB findOneAndUpdate TASK err: ' + err);
          });

          console.log('task added in handler, status: ' + task.status + ' action_key: ' + task.action_key); // test
        });

        handler_lock = 0;
        console.log('CRON log - TASKs ADDED in queue');
      }
    }

    console.log('this message logs every minute - CRON is active');
  });
}

module.exports = {
  taskStatusListener: taskStatusListener,
  bullConsumer: bullConsumer,
}

