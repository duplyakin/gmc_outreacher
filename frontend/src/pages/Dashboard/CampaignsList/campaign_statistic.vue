<template>
  <div>
    <card>
      <card>
        <div class="row">
          <div class="col-12 d-flex align-self-center">
            <h3>
              <i class="nc-icon nc-chart-bar-32"></i> Campaign Detalization
            </h3>
          </div>
        </div>
      </card>

      <div class="container">
        <div class="row align-items-end mb-3">
          <div class="col-7">
            <div class="block">
              <span class="demonstration">Statistic period</span>
              <el-date-picker
                v-model="date"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="|"
                start-placeholder="Start date"
                end-placeholder="End date"
                :picker-options="pickerOptions">
              </el-date-picker>
            </div>
          </div>
          <div class="col-5">
            <button
                @click.prevent="load_data"
                type="button"
                class="btn btn-default btn-success mx-1"
            >Get statistic</button>
          </div>
        </div>
      </div>

      <card>
        <div>Enrich credits left: {{credits_left}} (buy more email credits)</div>
      </card>


        <div v-show="!mouse_active" @mouseleave="mouseLeave">
        <div class="container">
          <div class="row">
            
            <div v-for="col in up_row" class="col-4 justify-content-center">
              <card class="bg-light">
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
              <card class="bg-light">
                <div v-if="statistics.hasOwnProperty(col.field)" class="text-info text-center h2"><strong>{{statistics[col.field]}}</strong></div>
                <div v-else class="text-info text-center h2"><strong>0</strong></div>
                <p class="text-center"><small>{{col.label}}</small></p>
              </card>
            </div>

          </div>
        </div>
        </div>

        <!--hover-->

        <div @mouseover="mouseOver" v-show="mouse_active">
        <div class="container">
          <div class="row">
            
            <div v-for="col in up_row" class="col-4 justify-content-center">
              <card class="bg-light">
                <div v-if="col.field == 'prospects_total' && statistics.hasOwnProperty('prospects_total')" class="text-info text-center h2"><strong>{{statistics[col.field]}}</strong></div>
                <div v-else-if="statistics.hasOwnProperty(col.field)" class="text-info text-center h2"><strong>{{statistics_abs[col.field]}}%</strong></div>
                <div v-else class="text-info text-center h2"><strong>0%</strong></div>
                <p class="text-center"><small>{{col.label}}</small></p>
              </card>
            </div>

          </div>
        </div>

        <div class="container">
          <div class="row">

            <div v-for="col in down_row" class="col-2 d-flex justify-content-center">
              <card class="bg-light">
                <div v-if="statistics_abs.hasOwnProperty(col.field)" class="text-info text-center h2"><strong>{{statistics_abs[col.field]}}%</strong></div>
                <div v-else class="text-info text-center h2"><strong>0%</strong></div>
                <p class="text-center"><small>{{col.label}}</small></p>
              </card>
            </div>

          </div>
        </div>
        </div>


      <div>
        <h4 class="card-title">Daily Statistics (comming soon)</h4>
        <p class="card-category">Statistics for the last days</p>
        <line-chart :chart-data="datacollection" :options="chartOptions"></line-chart>
        <div class="stats">
          <i class="fa fa-check"></i> Outreacher24
        </div>
      </div>
      
    </card>
  </div>
</template>
<script>
import { DatePicker, Notification, Select, Option } from "element-ui";
import LineChart from "./LineChart.js";

import axios from '@/api/axios-auth';;
import dummy_detalization from "./dummy_detalization"; // test data

const STATISTICS_API_DETALIZATION = "/statistics/campaign";

export default {
  components: {
    LineChart,
    [DatePicker.name]: DatePicker,
    [Select.name]: Select,
    [Option.name]: Option,
  },
  computed: {},
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
            return time.getTime() > Date.now();
          },
        shortcuts: [{
          text: 'Last week',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: 'Last month',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: 'Last 3 months',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }]
      },
      date: [],

      mouse_active: true,
      campaign_id: "",

      statistics: {},
      statistics_abs: {},

      down_row: [],
      up_row: [],

      credits_left: 0,

      // row data
      list_data: {
        columns: [],
        statistics: [],
      },

      // chart
      datacollection: {},

      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,

        //barThickness: 1,
        //maxBarThickness: 1,
        
        /*
        scales: {
          xAxes: [
            {
              stacked: true
            }
          ],
          yAxes: [
            {
              stacked: true
            }
          ]
        }*/
      },
    };
  },
  methods: {
    calcPercent(value, abs_value) {
      return Math.round(abs_value == 0 ? 0 : (value / abs_value) * 100);
    },
    mouseOver: function() {
      this.mouse_active = false;
    },
    mouseLeave: function() {
      this.mouse_active = true;
    },
    calculate() {
      if(this.statistics == null || !this.statistics.hasOwnProperty('prospects_total')) {
        return
      }

      if(this.statistics['prospects_total'] <= 0) {
        return
      }

      let statistics_abs = {}

      for(let key in this.statistics) {
        if(key != 'prospects_total') {
          statistics_abs[key] = Math.round(this.statistics['prospects_total'] == 0 ? 0 : (this.statistics[key] / this.statistics['prospects_total']) * 100)
        }
      }

      this.statistics_abs = statistics_abs
      console.log(this.statistics_abs)
    },

    load_data() {
      if(this.date == null || this.date.length != 2) {
        Notification.error({title: "Error", message: "Choose period"});
        return
      }

      const path = STATISTICS_API_DETALIZATION

      var data = new FormData()
      data.append("_campaign_id", this.campaign_id)
      data.append("_from_date", this.date[0])
      data.append("_to_date", this.date[1])

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          r = dummy_detalization // test
          if (r.code <= 0) {
            var msg = "Error loading campaign statistic " + r.msg;
            Notification.error({title: "Error", message: msg});
          } else {
            this.deserialize_data(r);
          }
        })
        .catch(error => {
          var msg = "Error loading campaign statistic " + error;
          Notification.error({title: "Error", message: msg});
        });
    },

    deserialize_data(new_data) {
      if(new_data == null) {
        return
      }

      for (var key in new_data) {
        if (this.list_data.hasOwnProperty(key) && new_data[key]) {
          //var parsed_data = JSON.parse(new_data[key]);
          var parsed_data = new_data[key]
          this.$set(this.list_data, key, parsed_data)
        }
      }

      let statistics = {}
      let days = {}
      let down_row = []
      let up_row = []

      // statistics
      if (this.list_data.statistics.length > 0) {
        for(let stat of this.list_data.statistics) {
          //days[stat._id.month_day] = { stat._id.action_key : ui }
          if(stat._id.hasOwnProperty('action_key')) {
            if(statistics[stat._id.action_key] == null) {
              statistics[stat._id.action_key] = stat.total
            } else {
              statistics[stat._id.action_key] += stat.total
            }
          }
          
        }

        let credits_left = this.list_data.statistics.find(function (element) {
            return (element._id == "credits-left" ? element : 0)
        })

        if(credits_left != 0 && credits_left.total != null) {
          this.credits_left = credits_left.total
        }
      }

      // columns
      if (this.list_data.columns.length > 0) {
        up_row = this.list_data.columns.filter(col => {
          if(col.field == 'prospects_total' || col.field == 'email-send-message' || col.field == 'linkedin-send-message') {
            return col
          }
        })

        down_row = this.list_data.columns.filter(col => {
          if(col.field != 'prospects_total' && col.field != 'email-send-message' && col.field != 'linkedin-send-message' && col.field != 'credits-left') {
            return col
          }
        })
      }

      this.statistics = statistics
      this.down_row = down_row
      this.up_row = up_row

      //console.log('statistics:', this.statistics)

      this.calculate()
    },
  },

  mounted() {
    this.campaign_id = this.$route.query.campaign_id || "";

    const end = new Date();
    const start = new Date();
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 20); // last 20 days

    this.date = [start, end]
    this.load_data()
  }
};
</script>
<style lang="scss">
</style>
