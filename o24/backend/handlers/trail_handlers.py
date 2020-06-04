import o24.backend.handlers.trail_failed_handlers as failed_handlers
import o24.backend.handlers.trail_carryout_handlers as carryout_handlers
import o24.backend.handlers.trail_block_handlers as block_handlers

import os
from o24.globals import *


FAILED_HANDLERS = {
    BAN_ERROR: failed_handlers.banned,
    LOGIN_ACTION_ERROR: failed_handlers.credentials_error,
    LOGIN_ERROR: failed_handlers.credentials_error,
    LOGIN_PAGE_ERROR: failed_handlers.credentials_error,
    SEARCH_ACTION_ERROR: failed_handlers.credentials_error,
    TRAIL_UNKNOWN_ERROR: failed_handlers.system_error
}

CARRYOUT_HANDLERS = {
    LINKEDIN_SEARCH_ACTION: carryout_handlers.linkedin_search_action,
    LINKEDIN_PARSE_PROFILE_ACTION: carryout_handlers.linkedin_parse_profile_action,
    EMAIL_CHECK_REPLY_ACTION: carryout_handlers.email_check_reply,
    CARRYOUT_DEFAULT_HANDLER: carryout_handlers.default_handler
}

BLOCK_HANDLERS = {
    BLOCK_HAPPENED : block_handlers.block_happend,
    NEED_USER_ACTION_RESOLVED : block_handlers.block_resolved,
    BLOCK_DEFAULT_HANDLER : block_handlers.block_default
}