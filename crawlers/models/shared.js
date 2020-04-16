let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let actionSchema = new Schema({
    action_type : {
      type: Number,
      default: 0,
    },

    data : {},

    medium : String,

    key : String,
});

let funnelSchema = new Schema({
    action : {
      type: Schema.Types.ObjectId,
      ref: 'Action',
    },

    paramters : {},

    root : {
      type: Boolean,
      default: false,
    },

    if_true : {
      type: Number,
      default: None,
    },

    if_false : {
      type: Number,
      default: None,
    },

    template : {},
});

let taskQueueSchema = new Schema({
  current_node : {
    type: Schema.Types.ObjectId,
    ref: Funnel,
  },

  action_key : String,

  status : {
    type: Number,
    default: NEW, // ???
  },

  ack : {
    type: Number,
    default: 0,
  },

  credentials_dict : {},

  credentials_id : Number,

  result_data : {},

  prospect_id : {
    type: Number,
    unique: true,
  },

  campaign_id : Number,

  record_type : {
    type: Number,
    default: 0,
  },

  followup_level : {
    type: Number,
    default: 0,
  },

  js_action : {
    type: Boolean,
    default: false,
  },
});

let asyncActionsSchema = new Schema({
  // open, reply
  action_type : Number,

  count : Number,

  // email, linkedin, twitter
  medium : String,

  // based on medium, check different tables: Mailbox, Linkedin, Twitter
  ref : Number,

  action_meta : {},

  created : {
    type: Date,
    default: Date.now,
  }
});

module.exports = {
   Action : mongoose.model('Action', actionSchema),
   Funnel : mongoose.model('Funnel', funnelSchema),
   TaskQueue : mongoose.model('TaskQueue', taskQueueSchema),
   AsyncActions : mongoose.model('AsyncActions', asyncActionsSchema),
}
