<template>
  <div>

      <card>
        <div class="col-12 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-air-baloon"></i> Dashboard
          </h3>
        </div>
      </card>

      <card>
        <card>
          <div class="mb-3">Enrich credits left: {{statistics['credits-left']}} (buy more email credits)</div>
        </card>

        <card>
        <div class="container">
          <div class="row">
            
            <div v-for="col in up_row" class="col-4 justify-content-center">
              <card v-if="col.field != 'credits-left'" class="bg-light">
                <div v-if="statistics.hasOwnProperty(col.field)" class="text-info text-center h2"><strong>{{statistics[col.field]}}</strong></div>
                <div v-else class="text-info text-center h2"><strong>0</strong></div>
                <p class="text-center"><small>{{col.label}}</small></p>
              </card>
            </div>

          </div>
        </div>

        <div class="container">
          <div class="row">

            <div v-for="col in down_row" class="col-2 d-flex justify-content-center">
              <card v-if="col.field != 'credits-left'" class="bg-light">
                <div v-if="statistics.hasOwnProperty(col.field)" class="text-info text-center h2"><strong>{{statistics[col.field]}}</strong></div>
                <div v-else class="text-info text-center h2"><strong>0</strong></div>
                <p class="text-center"><small>{{col.label}}</small></p>
              </card>
            </div>

          </div>
        </div>
        </card>
      </card>

  </div>
</template>
<script>
import axios from "@/api/axios-auth"

const STATISTICS_LIST = "/statistics/total"

export default {
  data() {
    return {
      columns: [],
      statistics: {},

      down_row: [],
      up_row: [],


      dummy_data: {
        code: 1, 
        columns: [
                    {"label": "Prospects contacted", "field": "prospects_total"}, 
                    {"label": "Emails sent", "field": "email-send-message"}, 
                    {"label": "Emails replied", "field": "email-check-reply"}, 
                    {"label": "Emails opened", "field": "email_opens"}, 
                    {"label": "Emails enriched", "field": "emails-enriched-success"}, 
                    {"label": "Linkedin invites sent", "field": "linkedin-connect"}, 
                    {"label": "Linkedin profiles viewed", "field": "linkedin-visit-profile"}, 
                    {"label": "Linkedin messages sent", "field": "linkedin-send-message"}, 
                    {"label": "Linkedin replied", "field": "linkedin-check-reply"}, 

                    {"label": "Enrich credits left", "field": "credits-left"}
                    ], 
        msg: 'Success', 
        statistics: [{"_id": "email_opens", "total": 24}, 
                     {"_id": "credits-left", "total": 999}]
    }
    };
  },
  methods: {
    load_statistics() {
      const path = STATISTICS_LIST

      var data = new FormData()

      axios
        .post(path, data)
        .then(res => {
          var r = res.data
          r = this.dummy_data // test
          if (r.code <= 0) {
            var msg = "Error loading statistics." + r.msg;
            Notification.error({ title: "Error", message: msg });

          } else {
              this.deserialize_data(r)
          }
        })
        .catch(error => {
          var msg = "Error loading statistics. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_data(from_data) {
      let statistics = {}
      let columns = []

      let down_row = []
      let up_row = []

      if (from_data.statistics != null) {
        //statistics_arr = JSON.parse(from_data.statistics)
        let statistics_arr = from_data.statistics

        for(let stat of statistics_arr) {
          statistics[stat._id] = stat.total
        }

        if(!statistics.hasOwnProperty('credits-left')) {
          statistics['credits-left'] = 0
        }
      }

      if (from_data.columns != null) {
        //columns = JSON.parse(from_data.columns)
        columns = from_data.columns

        up_row = columns.filter(col => {
          if(col.field == 'prospects_total' || col.field == 'email-send-message' || col.field == 'linkedin-send-message') {
            return col
          }
        })

        down_row = columns.filter(col => {
          if(col.field != 'prospects_total' && col.field != 'email-send-message' && col.field != 'linkedin-send-message' && col.field != 'credits-left') {
            return col
          }
        })
      }

      this.$set(this, 'statistics', statistics)
      this.$set(this, 'down_row', down_row)
      this.$set(this, 'up_row', up_row)
    },
  },
  mounted() {
    this.load_statistics()
  }
};
</script>
<style>

</style>
