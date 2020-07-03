<template>
  <div>
    <card>
      <div class="row">
        <div class="col-12 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-chart-bar-32"></i> Campaign Detalization
          </h3>
        </div>
      </div>
    </card>

    <card>
      <card>
        <div class="container">
          <div class="row align-items-end mb-3">
            <div class="col-7">
              <span class="demonstration">Statistics period</span>
              <el-date-picker
                v-model="date"
                type="daterange"
                align="right"
                unlink-panels
                range-separator="|"
                start-placeholder="Start date"
                end-placeholder="End date"
                :picker-options="pickerOptions"
              ></el-date-picker>
            </div>
            <div class="col-5">
              <button
                @click.prevent="load_data"
                type="button"
                class="btn btn-default btn-success mx-1"
              >Get statistics</button>
            </div>
          </div>
        </div>
      </card>

      <card>
        <div class="d-flex">
          Enrich credits left: <strong class="ml-2">{{credits_left}}</strong>
          <p class="text-danger ml-2"> (buy more email credits)</p>
        </div>
      </card>

      <div v-show="!mouse_active" @mouseleave="mouseLeave">
          <div class="container">
            <div class="row">
              <div v-for="col in columns" class="col justify-content-center">
                <div v-if="col.field != 'credits-left'" class="counter">
                  <div v-if="statistics.hasOwnProperty(col.field)" class="text-info text-center h3">
                    <strong>{{statistics[col.field]}}</strong>
                  </div>
                  <div v-else class="text-info text-center h3">
                    <strong>0</strong>
                  </div>
                  <p class="text-center">
                    <small>{{col.label}}</small>
                  </p>
                </div>
              </div>
            </div>
          </div>

      </div>

      <!--hover-->

      <div @mouseover="mouseOver" v-show="mouse_active">
          <div class="container">
            <div class="row">
              <div v-for="col in columns" class="col justify-content-center">
                <div v-if="col.field != 'credits-left'" class="counter">
                  <div
                    v-if="col.field == 'prospects_total' && statistics.hasOwnProperty('prospects_total')"
                    class="text-info text-center h3"
                  >
                    <strong>{{statistics[col.field]}}</strong>
                  </div>
                  <div
                    v-else-if="statistics.hasOwnProperty(col.field)"
                    class="text-info text-center h3"
                  >
                    <strong>{{statistics_abs[col.field]}}%</strong>
                  </div>
                  <div v-else class="text-info text-center h3">
                    <strong>0%</strong>
                  </div>
                  <p class="text-center">
                    <small>{{col.label}}</small>
                  </p>
                </div>
              </div>
            </div>
          </div>

      </div>

      <card>
        <h4 class="card-title">Daily Statistics</h4>
        <p class="card-category">Statistics for selected days</p>
        <line-chart :chart-data="datacollection" :options="chartOptions"></line-chart>
        <div class="stats">
          <i class="fa fa-check"></i> Outreacher24
        </div>
      </card>
    </card>
  </div>
</template>
<script>
import { DatePicker, Notification, Select, Option } from "element-ui";
import LineChart from "./LineChart.js";

import axios from "@/api/axios-auth";
import dummy_detalization from "./dummy_detalization"; // test data

const STATISTICS_API_DETALIZATION = "/statistics/campaign";

export default {
  components: {
    LineChart,
    [DatePicker.name]: DatePicker,
    [Select.name]: Select,
    [Option.name]: Option
  },
  computed: {},
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
        shortcuts: [
          {
            text: "Last week",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "Last month",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "Last 3 months",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      date: [], // period of statistics

      mouse_active: true,
      campaign_id: "",

      statistics: {},
      statistics_abs: {},

      columns: [],

      credits_left: 0,

      // row data
      list_data: {
        columns: [],
        statistics: []
      },

      // chart
      datacollection: {},
      colors: [
        "rgb(16, 53, 99)",
        "rgb(85, 153, 199)",
        "rgb(121, 88, 148)",
        "rgb(97, 184, 97)",
        "rgb(255, 158, 74)",
        "rgba(215, 255, 68, 0.959)",
        "rgb(255, 221, 68)",
        "rgb(255, 174, 68)",
        "rgb(109, 68, 255)",
        "rgb(68, 143, 255)",

      ],

      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,

        barThickness: 1,
        maxBarThickness: 1,
        
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
        }
      }
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
      if (this.statistics == null || !this.statistics.hasOwnProperty("prospects_total")) {
        return
      }

      if (this.statistics["prospects_total"] <= 0) {
        return
      }

      let statistics_abs = {}

      for (let key in this.statistics) {
        if (key != "prospects_total") {
          statistics_abs[key] = Math.round(this.statistics["prospects_total"] == 0 ? 0 : (this.statistics[key] / this.statistics["prospects_total"]) * 100);
        }
      }

      this.statistics_abs = statistics_abs
    },

    load_data() {
      if (this.date == null || this.date.length != 2) {
        Notification.error({ title: "Error", message: "Choose period" });
        return;
      }

      const path = STATISTICS_API_DETALIZATION;

      var data = new FormData();
      data.append("_campaign_id", this.campaign_id);
      data.append("_from_date", this.date[0]);
      data.append("_to_date", this.date[1]);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          r = dummy_detalization; // test
          if (r.code <= 0) {
            var msg = "Error loading campaign statistics " + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.deserialize_data(r);
          }
        })
        .catch(error => {
          var msg = "Error loading campaign statistics. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },

    deserialize_data(new_data) {
      if (new_data == null) {
        return
      }

      for (var key in new_data) {
        if (this.list_data.hasOwnProperty(key) && new_data[key]) {
          //var parsed_data = JSON.parse(new_data[key])
          var parsed_data = new_data[key]
          this.$set(this.list_data, key, parsed_data)
        }
      }

      let statistics = {}
      let columns = []

      // statistics
      if (this.list_data.statistics.length > 0) {
        for (let stat of this.list_data.statistics) {

          if (stat._id.hasOwnProperty("action_key")) {

            if (statistics[stat._id.action_key] == null) {
              statistics[stat._id.action_key] = stat.total

            } else {
              statistics[stat._id.action_key] += stat.total
            }
          }
        }

        let credits_left = this.list_data.statistics.find(function(element) {
          return element._id == "credits-left" ? element : 0
        })

        if (credits_left != 0 && credits_left.total != null) {
          this.credits_left = credits_left.total
        }
      }

      this.$set(this, 'statistics', statistics)
      this.$set(this, 'columns', this.list_data.columns)
      
      this.calculate()
      this.get_chart_data()
    },

    get_chart_data() {
      // delete not relevant data
      let sorted_statistics = this.list_data.statistics.filter( a => {
        if(a._id.hasOwnProperty('month_day') && a._id.hasOwnProperty('action_key')) {
          return a
        }
      })

      // sort days
      sorted_statistics = sorted_statistics.sort( (a, b) => {
        let a_set = a._id.month_day.split('-')
        let a_val = Number.parseInt(a_set[0]) * 30 + Number.parseInt(a_set[1])

        let b_set = b._id.month_day.split('-')
        let b_val = Number.parseInt(b_set[0]) * 30 + Number.parseInt(b_set[1])

        if(a_val < b_val) {
          return -1
        }
        if(a_val > b_val) {
          return 1
        }
        return 0
      })

      let days_set = new Set()
      let data_set = new Set()

      // get unique days and action_keys
      sorted_statistics = sorted_statistics.map(stat => {
        days_set.add(stat._id.month_day)

        let label = this.columns.find( col => {
          if(col.field == stat._id.action_key) {
            return col
          }
        }).label
        if(label != null) {
          data_set.add( label )
        }

        return stat
      })

      // create template of chart_data with unique set
      let chart_data = []
      let i = 0
      for(let data of data_set) {
        //chart_data.push({label: data, data: []})
        chart_data.push({label: data, backgroundColor: this.colors[i], data: []})
        i++
      }

      // push sorted data in each array in chart_data by action_key and day
      for(let day of days_set) {
        for(let data of chart_data) {
          let stat_value = sorted_statistics.find( stat => {

            let action_key = this.columns.find( col => {
              if(col.label == data.label) {
                return col
              }
            }).field

            if(stat._id.action_key == action_key && stat._id.month_day == day) {
              return stat
            }
          })

          if(stat_value != null) {
            data.data.push(stat_value.total)
          } else {
            data.data.push(0)
          }
        }
      }

      this.$set(this, 'datacollection', {labels: [...days_set], datasets: [...chart_data]})

      //console.log('sorted_statistics:', sorted_statistics)
      //console.log("days:", days_set)
      //console.log('chart_data:', chart_data)
    },
  },

  mounted() {
    this.campaign_id = this.$route.query.campaign_id || ""

    const end = new Date()
    const start = new Date()
    start.setTime(start.getTime() - 3600 * 1000 * 24 * 20) // last 20 days

    this.$set(this, 'date', [start, end])

    this.load_data()
  }
};
</script>
<style lang="scss">
</style>
