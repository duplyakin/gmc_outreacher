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
          <div class="col-4">
            <p>Filter by medium</p>
            <el-select
              class="select-default mb-3"
              v-on:change="onChangeMedium"
              style="width: 100%;"
              placeholder="Select medium"
              v-model="filter"
              value-key="title"
            >
              <el-option
                class="select-default"
                v-for="filter in filter_data"
                :key="filter.id"
                :label="filter.title"
                :value="filter.title"
              ></el-option>
            </el-select>
          </div>
        </div>
      </card>

      <card>
        <div class="container">
          <div>
            <p class="data-caption">Title</p>
            <p class="info">{{list_data.campaign.title}}</p>
          </div>
          <div>
            <p class="data-caption">Funnel</p>
            <p class="info">{{list_data.campaign.funnel.title}}</p>
          </div>
          <div>
            <p class="data-caption">Accounts</p>
            <div v-for="acc in list_data.campaign.credentials">
              <p class="purple">{{acc.medium}}: </p><p class="info">{{acc.data.email}}</p>
            </div>
          </div>
        </div>
      </card>

      <card v-if="filter!=''">
        <h3>{{filter}} Statistics</h3>
        <div class="container" @mouseover="mouseOver" v-show="mouse_active">
          <div v-for="obj in medium_data">
            <div v-bind:class="obj.class">{{obj.value}}</div>
            <p class="data-caption">{{obj.label}}</p>
          </div>
        </div>

        <div class="container" v-show="!mouse_active" @mouseleave="mouseLeave">
          <div v-for="obj in medium_data">
            <div
              v-bind:class="obj.class"
            >{{obj.relatively !== '' ? calcPercent(obj.value, medium_data[obj.relatively].value)+'%' : obj.value}}</div>
            <p class="data-caption">{{obj.label}}</p>
          </div>
        </div>
      </card>

      <div v-if="filter!=''">
        <h4 class="card-title">{{filter}} Daily Statistics</h4>
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
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";
import LineChart from "./LineChart.js";

import axios from '@/api/axios-auth';;
import dummy_detalization from "./dummy_detalization"; // test data

const STATISTICS_API_DETALIZATION = "/statistics/campaign";

export default {
  components: {
    LineChart,
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {},
  data() {
    return {
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

      datacollection: {},
      datacollectionEmail: {},
      datacollectionLinkedin: {},
      filter: "",
      filter_data: [],

      mouse_active: true,
      campaign_id: "",

      medium_data: {},
      email_data: {
        days: {
          class: "data-percent grey",
          relatively: "",
          label: "Days",
          value: 0
        },
        prospects_contacted: {
          class: "data-percent blue",
          relatively: "",
          label: "Prospects contacted",
          chart_color: "rgb(16, 53, 99)",
          value: 0
        },
        emails_sent: {
          class: "data-percent purple",
          relatively: "",
          label: "Emails sent",
          chart_color: "rgb(85, 153, 199)",
          value: 0
        },
        emails_bounced: {
          class: "data-percent red",
          relatively: "emails_sent",
          label: "Emails bounced",
          chart_color: "rgb(204, 0, 0)",
          value: 0
        },
        emails_opened: {
          class: "data-percent green",
          relatively: "emails_sent",
          label: "Emails opened",
          chart_color: "rgb(97, 184, 97)",
          value: 0
        },
        emails_replies: {
          class: "data-percent yellow",
          relatively: "emails_sent",
          label: "Emails replied",
          chart_color: "rgb(255, 158, 74)",
          value: 0
        }
      },

      linkedin_data: {
        days: {
          class: "data-percent grey",
          relatively: "",
          label: "Days",
          value: 0
        },
        prospects_contacted: {
          class: "data-percent purple",
          relatively: "",
          label: "Prospects contacted",
          chart_color: "rgb(16, 53, 99)",
          value: 0
        },
        connect_request: {
          class: "data-percent blue",
          relatively: "",
          label: "Connect request sended",
          chart_color: "rgb(85, 153, 199)",
          value: 0
        },
        connect_request_approved: {
          class: "data-percent purple",
          relatively: "connect_request",
          label: "Connect request approved",
          chart_color: "rgb(121, 88, 148)",
          value: 0
        },
        messages_sent: {
          class: "data-percent green",
          relatively: "",
          label: "Messages sended",
          chart_color: "rgb(97, 184, 97)",
          value: 0
        },
        replies_received: {
          class: "data-percent yellow",
          relatively: "messages_sent",
          label: "Replies resieved",
          chart_color: "rgb(255, 158, 74)",
          value: 0
        }
      },

      list_data: {
        campaign: {},
        statistics: {
          email: [],
          linkedin: []
        }
      }
    };
  },
  methods: {
    calcPercent(value, abs_value) {
      return Math.round(abs_value == 0 ? 0 : (value / abs_value) * 100);
    },
    onChangeMedium() {
      //console.log('filter: ', this.filter)
      this.$set(this, "medium_data", []);

      if (this.filter == "Email") {
        this.$set(this, "medium_data", this.email_data);
        this.datacollection = this.datacollectionEmail;
      }
      if (this.filter == "Linkedin") {
        this.$set(this, "medium_data", this.linkedin_data);
        this.datacollection = this.datacollectionLinkedin;
      }
    },
    mouseOver: function() {
      this.mouse_active = false;
    },
    mouseLeave: function() {
      this.mouse_active = true;
    },
    calculate() {
      // email
      let days = 0;
      let prospects_contacted = 0;
      let emails_sent = 0;
      let emails_bounced = 0;
      let emails_opened = 0;
      let emails_replies = 0;

      // email chart-bar !
      let days_arr = [];
      let prospects_contacted_arr = [];
      let emails_sent_arr = [];
      let emails_bounced_arr = [];
      let emails_opened_arr = [];
      let emails_replies_arr = [];

      this.list_data.statistics.email.forEach(function(item) {
        days++;
        prospects_contacted += item.prospects_email_contacted_total;
        emails_sent += item.emails_sent;
        emails_bounced += item.emails_bounced;
        emails_opened += item.emails_opened;
        emails_replies += item.emails_replies_total;

        days_arr.push(item.date);
        prospects_contacted_arr.push(item.prospects_email_contacted_total);
        emails_sent_arr.push(item.emails_sent);
        emails_bounced_arr.push(item.emails_bounced);
        emails_opened_arr.push(item.emails_opened);
        emails_replies_arr.push(item.emails_replies_total);
      });
      // email chart
      this.datacollectionEmail = {
        labels: days_arr,
        datasets: [
          {
            label: this.email_data.prospects_contacted.label,
            backgroundColor: this.email_data.prospects_contacted.chart_color,
            data: prospects_contacted_arr
          },
          {
            label: this.email_data.emails_sent.label,
            backgroundColor: this.email_data.emails_sent.chart_color,
            data: emails_sent_arr
          },
          {
            label: this.email_data.emails_bounced.label,
            backgroundColor: this.email_data.emails_bounced.chart_color,
            data: emails_bounced_arr
          },
          {
            label: this.email_data.emails_opened.label,
            backgroundColor: this.email_data.emails_opened.chart_color,
            data: emails_opened_arr
          },
          {
            label: this.email_data.emails_replies.label,
            backgroundColor: this.email_data.emails_replies.chart_color,
            data: emails_replies_arr
          }
        ]
      };

      // email data
      this.email_data.days.value = days;
      this.email_data.prospects_contacted.value = prospects_contacted;
      this.email_data.emails_sent.value = emails_sent;
      this.email_data.emails_bounced.value = emails_bounced;
      this.email_data.emails_opened.value = emails_opened;
      this.email_data.emails_replies.value = emails_replies;

      // linkedin
      days = 0;
      prospects_contacted = 0;
      let connect_request = 0;
      let connect_request_approved = 0;
      let messages_sent = 0;
      let replies_received = 0;

      // linkedin chart-bar !
      days_arr = [];
      prospects_contacted_arr = [];
      let connect_request_arr = [];
      let connect_request_approved_arr = [];
      let messages_sent_arr = [];
      let replies_received_arr = [];

      this.list_data.statistics.linkedin.forEach(function(item) {
        days++;
        prospects_contacted += item.prospects_linkedin_contacted_total;
        connect_request += item.connect_request_total;
        connect_request_approved += item.connect_request_approved_total;
        messages_sent += item.linkedin_messages_sent_total;
        replies_received += item.linkedin_replies_received;

        days_arr.push(item.date);
        prospects_contacted_arr.push(item.prospects_linkedin_contacted_total);
        connect_request_arr.push(item.connect_request_total);
        connect_request_approved_arr.push(item.connect_request_approved_total);
        messages_sent_arr.push(item.linkedin_messages_sent_total);
        replies_received_arr.push(item.linkedin_replies_received);
      });
      // linkedin chart
      this.datacollectionLinkedin = {
        labels: days_arr,
        datasets: [
          {
            label: this.linkedin_data.prospects_contacted.label,
            backgroundColor: this.linkedin_data.prospects_contacted.chart_color,
            data: prospects_contacted_arr
          },
          {
            label: this.linkedin_data.connect_request.label,
            backgroundColor: this.linkedin_data.connect_request.chart_color,
            data: connect_request_arr
          },
          {
            label: this.linkedin_data.connect_request_approved.label,
            backgroundColor: this.linkedin_data.connect_request_approved
              .chart_color,
            data: connect_request_approved_arr
          },
          {
            label: this.linkedin_data.messages_sent.label,
            backgroundColor: this.linkedin_data.messages_sent.chart_color,
            data: messages_sent_arr
          },
          {
            label: this.linkedin_data.replies_received.label,
            backgroundColor: this.linkedin_data.replies_received.chart_color,
            data: replies_received_arr
          }
        ]
      };

      // linkedin data
      this.linkedin_data.days.value = days;
      this.linkedin_data.prospects_contacted.value = prospects_contacted;
      this.linkedin_data.connect_request.value = connect_request;
      this.linkedin_data.connect_request_approved.value = connect_request_approved;
      this.linkedin_data.messages_sent.value = messages_sent;
      this.linkedin_data.replies_received.value = replies_received;
    },
    filterDefine() {
      if (this.list_data.statistics.hasOwnProperty('email')) {
        this.filter_data.push({ title: "Email" });
      }
      if (this.list_data.statistics.hasOwnProperty('linkedin')) {
        this.filter_data.push({ title: "Linkedin" });
      }

      this.filter = this.filter_data[0].title || '';
      this.onChangeMedium();
    },
    load_data_1() {
      const path = STATISTICS_API_DETALIZATION;

      var data = new FormData();
      data.append("_campaign_id", this.campaign_id);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading campaign statistics " + r.msg;
            Notification.error({title: "Error", message: msg});
          } else {
            this.deserialize_data(r, init);
          }
        })
        .catch(error => {
          var msg = "Error loading campaign statistics " + error;
          Notification.error({title: "Error", message: msg});
        });
    },
    load_data() {
      this.deserialize_data(dummy_detalization);
      this.calculate();
    },
    deserialize_data(new_data) {
      for (var key in new_data) {
        if (this.list_data.hasOwnProperty(key) && new_data[key]) {
          //var parsed_data = JSON.parse(new_data[key]);
          var parsed_data = new_data[key];
          this.$set(this.list_data, key, parsed_data);
        }
      }
      console.log(this.list_data);
    }
  },
  mounted() {
    this.campaign_id = this.$route.query.campaign_id || "";
    this.load_data();

    this.filterDefine();
  }
};
</script>
<style lang="scss">
.info {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  font-size: 22px;
  font-weight: 600;
  text-align: center;
  line-height: 0px;
  color: rgb(119, 119, 119);
}
.container {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding: 10px 20px;
}
.data {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  max-width: 100px;
  min-height: 105px;

  &-percent {
    height: 35px;
    margin: 0 0 10px;
    font-size: 35px;
    font-weight: 600;
    color: #000;
    text-align: center;
  }

  &-caption {
    line-height: 20px;
    text-transform: uppercase;
    font-size: 13px;
    text-align: center;
  }
}
.red {
  color: rgb(204, 0, 0);
}
.green {
  color: rgb(97, 184, 97);
}
.blue {
  color: rgb(85, 153, 199);
}
.purple {
  color: rgb(121, 88, 148);
}
.grey {
  color: rgb(174, 172, 172);
}
.yellow {
  color: rgb(255, 158, 74);
}
</style>
