<template>
  <div>
    <card>
      <div class="row">
        <div class="col-12 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-badge"></i> Campaign Detalization
          </h3>
        </div>
      </div>
    </card>

    <card>
      <h3>Email Statistics</h3>
      <div class="container" @mouseover="mouseOver" v-show="mouse_active">
        <div>
          <div class="data-percent grey">{{this.email_data.days}}</div>
          <p class="data-caption">DAYS</p>
        </div>
        <div>
          <div class="data-percent blue">{{this.email_data.emails_sent}}</div>
          <p class="data-caption">EMAILS SENDED</p>
        </div>
        <div>
          <div class="data-percent red">{{this.email_data.emails_bounced}}</div>
          <p class="data-caption">EMAILS BOUNCED</p>
        </div>
        <div>
          <div class="data-percent green">{{this.email_data.emails_opened}}</div>
          <p class="data-caption">EMAILS OPENED</p>
        </div>
        <div>
          <div class="data-percent yellow">{{this.email_data.emails_replies}}</div>
          <p class="data-caption">EMAILS REPLIED</p>
        </div>
      </div>

      <div class="container" v-show="!mouse_active" @mouseleave="mouseLeave">
        <div>
          <div class="data-percent grey">{{this.email_data.days}}</div>
          <p class="data-caption">DAYS</p>
        </div>
        <div>
          <div class="data-percent blue">{{this.email_data.emails_sent}}</div>
          <p class="data-caption">EMAILS SENDED</p>
        </div>
        <div>
          <div
            class="data-percent red"
          >{{Math.round(this.email_data.emails_sent == 0 ? 0 : this.email_data.emails_bounced / this.email_data.emails_sent * 100)}}%</div>
          <p class="data-caption">EMAILS BOUNCED</p>
        </div>
        <div>
          <div
            class="data-percent green"
          >{{Math.round(this.email_data.emails_sent == 0 ? 0 : this.email_data.emails_opened / this.email_data.emails_sent * 100)}}%</div>
          <p class="data-caption">EMAILS OPENED</p>
        </div>
        <div>
          <div
            class="data-percent yellow"
          >{{Math.round(this.email_data.emails_sent == 0 ? 0 : this.email_data.emails_replies / this.email_data.emails_sent * 100)}}%</div>
          <p class="data-caption">EMAILS REPLIED</p>
        </div>
      </div>
    </card>

    <card>
      <h3>LinkedIn Statistics</h3>
      <div class="container" @mouseover="mouseOver" v-show="mouse_active">
        <div>
          <div class="data-percent grey">{{this.linkedin_data.days}}</div>
          <p class="data-caption">DAYS</p>
        </div>
        <div>
          <div class="data-percent blue">{{this.linkedin_data.connect_request}}</div>
          <p class="data-caption">CONNECT REQUESTS SENDED</p>
        </div>
        <div>
          <div class="data-percent purple">{{this.linkedin_data.connect_request_approved}}</div>
          <p class="data-caption">CONNECT REQUESTS APPROVED</p>
        </div>
        <div>
          <div class="data-percent green">{{this.linkedin_data.messages_sent}}</div>
          <p class="data-caption">MESSAGES SENDED</p>
        </div>
        <div>
          <div class="data-percent yellow">{{this.linkedin_data.replies_received}}</div>
          <p class="data-caption">REPLIES RECIEVED</p>
        </div>
      </div>

      <div class="container" v-show="!mouse_active" @mouseleave="mouseLeave">
        <div>
          <div class="data-percent grey">{{this.linkedin_data.days}}</div>
          <p class="data-caption">DAYS</p>
        </div>
        <div>
          <div class="data-percent blue">{{this.linkedin_data.connect_request}}</div>
          <p class="data-caption">CONNECT REQUESTS SENDED</p>
        </div>
        <div>
          <div
            class="data-percent purple"
          >{{Math.round(this.linkedin_data.connect_request == 0 ? 0 : this.linkedin_data.connect_request_approved / this.linkedin_data.connect_request * 100)}}%</div>
          <p class="data-caption">CONNECT REQUESTS APPROVED</p>
        </div>
        <div>
          <div class="data-percent green">{{this.linkedin_data.messages_sent}}</div>
          <p class="data-caption">MESSAGES SENDED</p>
        </div>
        <div>
          <div
            class="data-percent yellow"
          >{{Math.round(this.linkedin_data.messages_sent == 0 ? 0 : this.linkedin_data.replies_received / this.linkedin_data.messages_sent * 100)}}%</div>
          <p class="data-caption">REPLIES RECIEVED</p>
        </div>
      </div>
    </card>

    <chart-card
      :chart-data="barChart.data_email"
      :chart-options="barChart.options"
      :chart-responsive-options="barChart.responsiveOptions"
      chart-type="Bar"
    >
      <template slot="header">
        <h4 class="card-title">Email Daily Statistics</h4>
        <p class="card-category">Statistics for the last 15 days</p>
      </template>
      <template slot="footer">
        <div class="legend">
          <i class="fa fa-circle text-info"></i> Connect requests sended
          <i class="fa fa-circle text-danger"></i> Connect requests approved
          <i class="fa fa-circle text-warning"></i> Messages sended
          <i class="fa fa-circle text-primary"></i> Replies recieved
        </div>
        <hr />
        <div class="stats">
          <i class="fa fa-check"></i> Outreacher24
        </div>
      </template>
    </chart-card>

    <chart-card
      :chart-data="barChart.data_linkedin"
      :chart-options="barChart.options"
      :chart-responsive-options="barChart.responsiveOptions"
      chart-type="Bar"
    >
      <template slot="header">
        <h4 class="card-title">Linkedin Daily Statistics</h4>
        <p class="card-category">Statistics for the last 15 days</p>
      </template>
      <template slot="footer">
        <div class="legend">
          <i class="fa fa-circle text-info"></i> Connect requests sended
          <i class="fa fa-circle text-danger"></i> Connect requests approved
          <i class="fa fa-circle text-warning"></i> Messages sended
          <i class="fa fa-circle text-primary"></i> Replies recieved
        </div>
        <hr />
        <div class="stats">
          <i class="fa fa-check"></i> Outreacher24
        </div>
      </template>
    </chart-card>
  </div>
</template>
<script>
import { Table, TableColumn, Select, Option } from "element-ui";
import { ChartCard, Pagination as LPagination } from "src/components/index";

import axios from "axios";
import dummy_detalization from "./dummy_detalization"; // test data

const STATISTICS_API_DETALIZATION = "http://127.0.0.1:5000/statistics/campaign";

export default {
  components: {
    ChartCard,
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {},
  data() {
    return {
      mouse_active: true,
      campaign_id: "",
      email_data: {
        days: 0,
        //prospects_contacted: 0,
        emails_sent: 0,
        emails_bounced: 0,
        emails_opened: 0,
        emails_replies: 0
      },
      linkedin_data: {
        days: 0,
        //prospects_contacted: 0,
        connect_request: 0,
        connect_request_approved: 0,
        messages_sent: 0,
        replies_received: 0
      },
      list_data: {
        campaign: {},
        statistics: {
          email: [],
          linkedin: []
        }
      },
      labels: ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],
      barChart: {
        data_email: {
            labels: [],
            series: [],
        },
        data_linkedin: {
            labels: [],
            series: [],
        },
        options: {
          seriesBarDistance: 10,
          axisX: {
            showGrid: false
          },
          height: "245px"
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc(value) {
                  return value[0];
                }
              }
            }
          ]
        ]
      }
    };
  },
  methods: {
    mouseOver: function() {
      this.mouse_active = false;
    },
    mouseLeave: function() {
      this.mouse_active = true;
    },
    calculate() {
      // email
      let email_obj = {
        days: 0,
        emails_sent: 0,
        emails_bounced: 0,
        emails_opened: 0,
        emails_replies: 0
      };

      // email chart-bar !
      let emails_sent_arr = [];
      let emails_bounced_arr = [];
      let emails_opened_arr = [];
      let emails_replies_arr = [];

      this.list_data.statistics.email.forEach(function(item) {
        email_obj.days++;
        email_obj.emails_sent += item.emails_sent;
        email_obj.emails_bounced += item.emails_bounced;
        email_obj.emails_opened += item.emails_opened;
        email_obj.emails_replies += item.emails_replies_total;

        emails_sent_arr.push(item.emails_sent);
        emails_bounced_arr.push(item.emails_bounced);
        emails_opened_arr.push(item.emails_opened);
        emails_replies_arr.push(item.emails_replies_total);
      });
      //this.$set(this, "barChart.data_email", {labels: this.labels, series: [emails_sent_arr, emails_bounced_arr, emails_opened_arr, emails_replies_arr]});
      this.$set(this.barChart.data_email.series, 0, emails_sent_arr);
      this.$set(this.barChart.data_email.series, 1, emails_bounced_arr);
      this.$set(this.barChart.data_email.series, 2, emails_opened_arr);
      this.$set(this.barChart.data_email.series, 3, emails_replies_arr);

      this.$set(this, "email_data", email_obj);

      // linkedin
      let linkedin_obj = {
        days: 0,
        connect_request: 0,
        connect_request_approved: 0,
        messages_sent: 0,
        replies_received: 0
      };

      // linkedin chart-bar !
      let connect_request_arr = [];
      let connect_request_approved_arr = [];
      let messages_sent_arr = [];
      let replies_received_arr = [];
      this.list_data.statistics.linkedin.forEach(function(item) {
        linkedin_obj.days++;
        linkedin_obj.connect_request += item.connect_request_total;
        linkedin_obj.connect_request_approved += item.connect_request_approved_total;
        linkedin_obj.messages_sent += item.linkedin_messages_sent_total;
        linkedin_obj.replies_received += item.linkedin_replies_received;

        connect_request_arr.push(item.connect_request_total);
        connect_request_approved_arr.push(item.connect_request_approved_total);
        messages_sent_arr.push(item.linkedin_messages_sent_total);
        replies_received_arr.push(item.linkedin_replies_received);
      });
      this.$set(this.barChart.data_linkedin.series, 0, connect_request_arr);
      this.$set(this.barChart.data_linkedin.series, 1, connect_request_approved_arr);
      this.$set(this.barChart.data_linkedin.series, 2, messages_sent_arr);
      this.$set(this.barChart.data_linkedin.series, 3, replies_received_arr);

      this.$set(this, "linkedin_data", linkedin_obj);
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
            alert(msg);
          } else {
            this.deserialize_data(r, init);
          }
        })
        .catch(error => {
          var msg = "Error loading campaign statistics " + error;
          alert(msg);
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
  }
};
</script>
<style lang="scss">
.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 20px;
}
.data {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  max-width: 100px;

  &-percent {
    height: 35px;
    margin: 0 0 10px;
    font-size: 35px;
    font-weight: 600;
    color: #000;
  }

  &-caption {
    line-height: 20px;
    text-transform: uppercase;
    font-size: 15x;
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
