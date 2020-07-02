<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-chart-bar-32"></i> Statistics
          </h3>
        </div>
        <div class="col-8 d-flex flex-row-reverse align-self-center">
          <div>
            <button
              @click.prevent="load_data(1,1)"
              type="button"
              class="btn btn-default btn-success mx-1"
            >Refresh</button>
          </div>
        </div>
      </div>
    </card>

    <card>
      <div class="col-12">
        <el-table
          stripe
          ref="campaigns_data_table"
          style="width: 100%;"
          :data="statistics_data.statistics"
          max-height="500"
          border
        >
          <el-table-column
            v-for="(column,index) in list_data.columns"
            :key="index"
            :prop="column.prop"
            :label="column.label"
            :fixed="column.prop === 'title' ? true : false"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <a
                @click.prevent="detalization(scope.row)"
                href="#"
                v-if="column.prop === 'title'"
              >{{ scope.row.campaign[column.prop] }}</a>
              <template
                v-else
              >{{ column.campaign ? (column.object ? scope.row.campaign[column.prop][column.sub_prop] : scope.row.campaign[column.prop]) : scope.row.aggregated[column.prop] }}</template>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </card>
  </div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";

import axios from '@/api/axios-auth';
import dummy_statistics from "./dummy_statistics"; // test data

const STATISTICS_API_LIST = "/statistics/list";
const STATISTICS_API_DATA = "/statistics/data";

export default {
  components: {
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {},
  data() {
    return {
      pagination: {
        perPage: 0,
        currentPage: 1,
        total: 0
      },
      list_data: {
        columns: [
          {
            prop: "title",
            label: "Titile",
            campaign: true,
            minWidth: 300
          },
          {
            prop: "funnel",
            sub_prop: "title",
            label: "Sequence",
            campaign: true,
            object: true,
            minWidth: 100
          },
          {
            prop: "prospects_list",
            sub_prop: "title",
            label: "Leads list",
            object: true,
            campaign: true,
            minWidth: 100
          },
          {
            prop: "prospects_contacted_total",
            label: "Contacted",
            minWidth: 50
          },
          {
            prop: "prospects_email_opens_total",
            label: "Opened",
            minWidth: 50
          },
          {
            prop: "linkedin_accounts_404",
            label: "Not found",
            minWidth: 50
          },
          {
            prop: "email_bounced_total",
            label: "Bounced",
            minWidth: 50
          },
          {
            prop: "linkedin_messages_failed_total",
            label: "Sent failed",
            minWidth: 50
          },
          {
            prop: "prospects_accepted_linkedin_total",
            label: "Accepted",
            minWidth: 50
          },
          {
            prop: "replied_total",
            label: "Replies",
            minWidth: 50
          }
        ]
      },
      statistics_data: {
        statistics: []
      }
    };
  },
  methods: {
    detalization(msg_dict) {
      this.$router.push({
        path: "statistics_detailed",
        query: { campaign_id: msg_dict.campaign.id }
      });
    },
    next_page() {
      var page = 2;
      this.load_data(page, 0);
    },
    load_data_1() {
      const path = STATISTICS_API_DATA;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading data statistics " + r.msg;
            Notification.error({title: "Error", message: msg});
          } else {
            this.deserialize_data(r, init);
          }
        })
        .catch(error => {
          var msg = "Error loading data statistics " + error;
          Notification.error({title: "Error", message: msg});
        });
    },
    load_statistics() {
      const path = STATISTICS_API_LIST;

      var data = new FormData();
      data.append("_page", 1);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading campaigns statistics " + r.msg;
            Notification.error({title: "Error", message: msg});
          } else {
            this.deserialize_statistics(r, init);
          }
        })
        .catch(error => {
          var msg = "Error loading campaigns statistics " + error;
          Notification.error({title: "Error", message: msg});
        });
    },
    load_data() {
      this.deserialize_statistics(dummy_statistics);
    },
    deserialize_statistics(new_data) {
      for (var key in new_data) {
        if (this.statistics_data.hasOwnProperty(key) && new_data[key]) {
          //var parsed_data = JSON.parse(new_data[key]);
          var parsed_data = new_data[key];
          this.$set(this.statistics_data, key, parsed_data);
        }
      }
      console.log(this.statistics_data);
    },
    deserialize_data(new_data) {
      for (var key in new_data) {
        if (this.statistics_data.hasOwnProperty(key) && new_data[key]) {
          //var parsed_data = JSON.parse(new_data[key]);
          var parsed_data = new_data[key];
          this.$set(this.list_data, key, parsed_data);
        }
      }
      /*
        var pagination_dict = JSON.parse(new_data.pagination);
        this.$set(this, 'pagination', pagination_dict);
        */
      console.log(this.statistics_data);
    }
  },
  async mounted() {
    await this.load_data();
    //await this.load_statistics();
  }
};
</script>
<style>
</style>
