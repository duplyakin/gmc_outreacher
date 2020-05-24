let mongooseConnect = require('./connect.js');
let mongoose = mongooseConnect.mongoose;
let Schema = mongoose.Schema;

let actionSchema = new Schema({
    action_type : {
      type: Number,
      default: 0,
    },

    data : Object,

    medium : String,

    key : String,
});

let funnelSchema = new Schema({
    action : {
      type: mongoose.ObjectId,
      ref: 'Action',
    },

    paramters : Object,

    funnel_type : {
      type: Number,
      default: 0,
    },

    title : String,

    templates_required : Object,

    template_key : {
      type: String,
      default: '',
    },

    root : {
      type: Boolean,
      default: false,
    },

    if_true : {
      type: Number,
      default: null,
    },

    if_false : {
      type: Number,
      default: null,
    },

    data : Object,
});

let taskQueueSchema = new Schema({
  current_node : {
    type: mongoose.ObjectId,
    ref: 'Funnel',
  },

  action_key : String,

  status : {
    type: Number,
    default: 0, // NEW
  },

  ack : {
    type: Number,
    default: 0,
  },

  next_round : {
    type: Date,
    default: 0,
  },

  input_data : Object,

  result_data : Object,

  credentials_id : mongoose.ObjectId,

  prospect_id : {
    type: mongoose.ObjectId,
    unique: true,
  },

  campaign_id : mongoose.ObjectId,

  record_type : {
    type: Number,
    default: 0,
  },

  followup_level : {
    type: Number,
    default: 0,
  },
/*
  js_action : {
    type: Boolean,
    default: false,
  },
  */
});

let asyncTaskQueueSchema = new Schema({
  campaign_id : {
    type: mongoose.ObjectId,
    unique: true,
  },
  
  input_data : Object,

  result_data : Object,
  
});

module.exports = {
   Action : mongoose.model('Action', actionSchema),
   Funnel : mongoose.model('Funnel', funnelSchema),
   TaskQueue : mongoose.model('TaskQueue', taskQueueSchema),
   AsyncTaskQueue : mongoose.model('AsyncActions', asyncTaskQueueSchema),
}
