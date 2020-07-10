// login
module.exports.USERNAME_SELECTOR = '#username';
module.exports.PASSWORD_SELECTOR = '#password';
module.exports.CTA_SELECTOR = '#app__container > main > div > form > div.login__form_action_container > button';
module.exports.BLOCK_TOAST_SELECTOR = '#app__container > artdeco-toasts > artdeco-toast > div > p';

// checkpoint
module.exports.VERIFICATION_PIN_SELECTOR = '#input__email_verification_pin';
module.exports.VERIFICATION_PIN_BTN_SELECTOR = '#email-pin-submit-button';

// captcha
module.exports.CAPTCHA_SELECTOR = '.g-recaptcha';
module.exports.CAPTCHA_RESPONSE_SELECTOR = '#g-recaptcha-response';
module.exports.SUBMIT_CAPTCHA_BTN_SELECTOR = ''; // delete

// search
module.exports.SEARCH_ELEMENT_SELECTOR = '.search-result__wrapper .search-result__info';
module.exports.LINK_SELECTOR = 'span > .actor-name';
module.exports.FULL_NAME_SELECTOR = 'span > .actor-name';
module.exports.DEGREE_SELECTOR = 'span > .dist-value';
module.exports.NEXT_PAGE_SELECTOR = '.artdeco-pagination__button--next';
module.exports.NEXT_PAGE_MUTED_SELECTOR = '.artdeco-pagination__button--next.artdeco-button--disabled';
module.exports.SEARCH_JOB_SELECTOR = '.search-result__snippets-black';

// search SN
module.exports.SN_CLOSE_HELP_SELECTOR = '#global-nav-help-menu-trigger-button';
module.exports.SN_SEARCH_ELEMENT_SELECTOR = '.search-results__result-item';
module.exports.SN_LINK_SELECTOR = '.result-lockup__name .ember-view';
module.exports.SN_FULL_NAME_SELECTOR = '.result-lockup__name .ember-view';
module.exports.SN_DEGREE_SELECTOR = '.label-16dp.block';
module.exports.SN_NEXT_PAGE_SELECTOR = '.search-results__pagination-next-button';
//module.exports.SN_NEXT_PAGE_MUTED_SELECTOR = '.artdeco-pagination__button--next.artdeco-button--disabled'; // not used
module.exports.SN_JOB_SELECTOR = '.result-lockup__highlight-keyword .t-14.t-bold';
module.exports.SN_JOB_LINK_SELECTOR = '.result-lockup__position-company > a';
module.exports.SN_JOB_NAME_SELECTOR = '.result-lockup__position-company > a > span';

// connect
module.exports.CONNECT_SELECTOR = '.pv-s-profile-actions.pv-s-profile-actions--connect';
module.exports.ADD_MSG_BTN_SELECTOR = '.mr1.artdeco-button.artdeco-button--muted';
module.exports.MSG_SELECTOR = '#custom-message';
module.exports.SEND_INVITE_TEXT_BTN_SELECTOR = '.ml1.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view';

// follow
module.exports.MORE_BTN_SELECTOR = '.ml2.pv-s-profile-actions__overflow-toggle';
module.exports.FOLLOW_SELECTOR = '.pv-s-profile-actions.pv-s-profile-actions--follow';

// phone form
//module.exports.SKIP_PHONE_FORM_SELECTOR = '.linkedin_phone_skip_div';
//module.exports.SKIP_PHONE_PAGE_SELECTOR = 'phone';
module.exports.SKIP_PHONE_BTN_SELECTOR = '.secondary-action';

// message
module.exports.WRITE_MSG_BTN_SELECTOR = '.message-anywhere-button.pv-s-profile-actions.pv-s-profile-actions--message';
module.exports.WRITE_MSG_BTN_DISABLED_SELECTOR = '.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view';
module.exports.CLOSE_MSG_BOX_SELECTOR = '.msg-overlay-bubble-header';
module.exports.MSG_BOX_SELECTOR = '.msg-form__msg-content-container';
//module.exports.MSG_BOX_SELECTOR = '.message-anywhere-button.pv-s-profile-actions.pv-s-profile-actions--message';
module.exports.SEND_MSG_BTN_SELECTOR = '.msg-form__send-button';
module.exports.LAST_MSG_LINK_SELECTOR = '.msg-s-event-listitem__link';
module.exports.LAST_MSG_SELECTOR = '.msg-s-event-listitem__body';

// scribe
module.exports.JOB_LINK_SELECTOR = 'a.full-width.ember-view';
module.exports.JOB_SITE_SELECTOR = 'span.link-without-visited-state';
module.exports.COUNTRY_SELECTOR = '.t-16.t-black.t-normal.inline-block';
module.exports.EDUCATION_SELECTOR = '.pv-entity__school-name';
module.exports.JOB_SELECTOR = '.t-16.t-black.t-bold';
// scribe contact info
module.exports.CONTACT_INFO_SELECTOR = '.inline-block .ember-view';
module.exports.CONTACT_INFO_CLOSE_SELECTOR = 'li-icon > svg';
module.exports.CONTACT_INFO_PHONE_SELECTOR = 'section.pv-contact-info__contact-type.ci-phone > ul > li > span.t-14.t-black.t-normal';
module.exports.CONTACT_INFO_ADDRESS_SELECTOR = 'section.pv-contact-info__contact-type.ci-address > div > a';
module.exports.CONTACT_INFO_EMAIL_SELECTOR = 'section.pv-contact-info__contact-type.ci-email > div > a';
module.exports.CONTACT_INFO_TWITTER_SELECTOR = 'section.pv-contact-info__contact-type.ci-twitter > ul > li > a';
module.exports.CONTACT_INFO_IM_SELECTOR = 'section.pv-contact-info__contact-type.ci-ims > ul > li > span.pv-contact-info__contact-item.t-14.t-black.t-normal'; // like Skype etc
module.exports.CONTACT_INFO_BIRTHDAY_SELECTOR = 'section.pv-contact-info__contact-type.ci-birthday > div > span';
module.exports.CONTACT_INFO_CONNECTED_DATE_SELECTOR = 'section.pv-contact-info__contact-type.ci-connected > div > span';

// connect check
module.exports.SEARCH_CONNECTS_SELECTOR = '#mn-connections-search-input';
module.exports.CONNECTOR_SELECTOR = 'span.mn-connection-card__name';
module.exports.CONNECT_DEGREE_SELECTOR = '.pv-top-card--list .dist-value';

// post engagement
// comments
module.exports.POST_MORE_COMMENTERS_BTN_SELECTOR = '.comments-comments-list__load-more-comments-button';
module.exports.POST_PREVIOUS_REPLIES_BTN_SELECTOR = '.button.show-prev-replies';
module.exports.POST_ELEMENT_SELECTOR = 'article';
module.exports.POST_AUTHOR_TAG_SELECTOR = '.comments-post-meta__author-badge';
module.exports.POST_COMMENTER_LINK_SELECTOR = '.comments-post-meta__profile-link';
module.exports.POST_COMMENTER_NAME_SELECTOR = '.hoverable-link-text';
module.exports.POST_COMMENTER_JOB_SELECTOR = '.comments-post-meta__headline';
// likes
