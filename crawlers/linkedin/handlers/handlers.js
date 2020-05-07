const { bull_workers } = require('/./bullWorkersSettings.js');
let mongoose = require('../mongoose');
let TaskQueue = require('TaskQueue');
const workers = require(__dirname + '/workers/workers.js');
const cron = require('../node-cron');

const MyExceptions = require('/../.././exceptions/exceptions.js');


async function bullConsumer() {
  bull_workers.process(async job => {
    try {
      switch (job.data.action_key) {
        case 'linkedin-check-reply':
          await workers.loginWorker(job.data.task_id);
          break;
        case 'linkedin-visit-profile':
          await workers.loginWorker(job.data.task_id);
          break;
        case 'linkedin-connect':
          await workers.connectWorker(job.data.task_id);
          break;
        case 'linkedin-send-message':
          await workers.messageWorker(job.data.task_id);
          break;
        case 'linkedin-check-accept':
          await workers.loginWorker(job.data.task_id);
          break;

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

        default:
          console.log("..... Incorrect task.action_key .....");
      }
    } catch (err) {
      throw new MyExceptions.UnknownError('Handler error - something went wrong: ' + err).code;
    }
  });
}

async function taskStatusListener() {
  // start cron every minute
  cron.schedule("* * * * *", () => {
    let tasks = await TaskQueue.find({ status: 1, js_action: true });
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
