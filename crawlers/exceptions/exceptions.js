const ERROR_CODES = require(__dirname + '/error_codes.js');

//Define exceptions.
const UnknownError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.UNKNOWN_ERROR
});

const HandlerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.HANDLER_ERROR
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

//------Workers-------
const LoginWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.LOGIN_WORKER_ERROR
});
const ConnectWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.CONNECT_WORKER_ERROR
});
const ConnectCheckWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.CONNECT_CHECK_WORKER_ERROR
});
const MessageWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.MESSAGE_WORKER_ERROR
});
const MessageCheckWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.MESSAGE_CHECK_WORKER_ERROR
});
const ScribeWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SCRIBE_WORKER_ERROR
});
const SearchWorkerError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SEARCH_WORKER_ERROR
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
const LoginPageError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.LOGIN_PAGE_ERROR
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
const ScribeActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SCRIBE_ACTION_ERROR
});
const SearchActionError = (message) => ({
  error: new Error(message),
  code: ERROR_CODES.SEARCH_ACTION_ERROR
});

module.exports = {
  UnknownError: UnknownError,
  HandlerError: HandlerError,
  WorkerError: WorkerError,
  ActionError: ActionError,
  MongoDBError: MongoDBError,

  LoginWorkerError: LoginWorkerError,
  ConnectWorkerError: ConnectWorkerError,
  ConnectCheckWorkerError: ConnectCheckWorkerError,
  MessageWorkerError: MessageWorkerError,
  MessageCheckWorkerError: MessageCheckWorkerError,
  ScribeWorkerError: ScribeWorkerError,
  SearchWorkerError: SearchWorkerError,

  LoginActionError: LoginActionError,
  LoginError: LoginError,
  LoginPageError: LoginPageError,
  ConnectActionError: ConnectActionError,
  ConnectCheckActionError: ConnectCheckActionError,
  MessageActionError: MessageActionError,
  MessageCheckActionError: MessageCheckActionError,
  ScribeActionError: ScribeActionError,
  SearchActionError: SearchActionError,
}
