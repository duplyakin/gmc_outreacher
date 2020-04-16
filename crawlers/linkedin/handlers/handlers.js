const { bull_workers } = require('/./bullWorkersSettings.js');
const { bull_tasks } = require('/./bullTasksSettings.js');
let mongoose = require('mongoose');
let TaskQueue = require('TaskQueue');
const workers = require(__dirname + '/workers/workers.js');

const options = {
  delay: 0,
  attempts: 3
}

bull_tasks.process(async job => {
  let tasks = await checkTaskStatus();
  tasks.forEach((task) => {
    await bull_workers.add(task, options);
  });
});

bull_workers.process(async job => {
  switch (job.task.action_key) {
  case 'linkedin-check-reply':
    await workers.loginWorker(job.task);
    break;
  case 'linkedin-visit-profile':
    await workers.loginWorker(job.task);
    break;
  case 'linkedin-connect':
    await workers.connectWorker(job.task);
    break;
  case 'linkedin-send-message':
    await workers.messageWorker(job.task);
    break;
  case 'delay-linkedin':
    await workers.loginWorker(job.task);
    break;
  case 'finished':
    //await workers.loginWorker(job.task);
    break;
  case 'success':
    //await workers.loginWorker(job.task);
    break;
  case 'linkedin-check-accept':
    await workers.loginWorker(job.task);
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
});

await function checkTaskStatus() {
  let tasks = TaskQueue.find({status: 'IN_PROGRESS', js_action: true});
  return tasks;
}
