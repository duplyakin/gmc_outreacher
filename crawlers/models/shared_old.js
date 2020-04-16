let mongoose = require('mongoose')

let actionSchema = new mongoose.Schema({

    event: {
        type: Boolean,
        default: false
    },
    data : {}
})

let funnelSchema = new mongoose.Schema({

    action: {
        type: Boolean,
        default: false
    },
    frequency : {},
    parent: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Funnel"
      },
    
    if_true: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Funnel"
    },

    if_false: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Funnel"
    }

})

let TaskQueueSchema = new mongoose.Schema({
    current: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Funnel"
    },

    status : {
        type: Number,
        default : 0
    },
    
    data : {},
    result : {},
    credentials : {}
})


module.exports = {
   Action : mongoose.model('Action', actionSchema),
   Funnel : mongoose.model('Funnel', funnelSchema),
   TaskQueue : mongoose.model('TaskQueue', TaskQueueSchema)
}