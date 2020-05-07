const ERROR_CODES = require(__dirname + '/error_codes.js');

//Define exceptions.
const UnknownError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.UNKNOWN_ERROR
});

const WorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.WORKER_ERROR
});

const ActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.ACTION_ERROR
});

const MongoDBError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.MONGODB_ERROR
});

//------Actions-------
const LoginActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.LOGIN_ACTION_ERROR
});
const LoginError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.LOGIN_ERROR
});
const ConnectActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.CONNECT_ACTION_ERROR
});
const ConnectCheckActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.CONNECT_CHECK_ACTION_ERROR
});
const MessageActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.MESSAGE_ACTION_ERROR
});
const MessageCheckActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.MESSAGE_CHECK_ACTION_ERROR
});
const SkribeWorkActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SCRIBE_WORK_ACTION_ERROR
});
const SearchActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SEARCH_ACTION_ERROR
});

module.exports = {
  UnknownError: UnknownError,
  WorkerError: WorkerError,
  ActionError: ActionError,
  MongoDBError: MongoDBError,

  LoginActionError: LoginActionError,
  LoginError: LoginError,
  ConnectActionError: ConnectActionError,
  ConnectCheckActionError: ConnectCheckActionError,
  MessageActionError: MessageActionError,
  MessageCheckActionError: MessageCheckActionError,
  SkribeWorkActionError: SkribeWorkActionError,
  SearchActionError: SearchActionError,
}
