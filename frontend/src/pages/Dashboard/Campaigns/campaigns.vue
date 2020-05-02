<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <span font->
            <h3>
              <i class="nc-icon nc-badge"></i> Campaigns
            </h3>
          </span>
        </div>
        <div class="col-8 d-flex flex-row-reverse align-self-center">
          <div>
            <button
              @click.prevent="addCampaign()"
              type="button"
              class="btn btn-default btn-success mx-1"
            >Add Campaign</button>
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
          :data="list_data.campaigns"
          max-height="500"
          border
        >
          <el-table-column
            v-for="column in list_data.columns"
            :key="column.label"
            :prop="column.prop"
            :label="column.label"
            :fixed="column.label === 'title' ? true : false"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
                <a @click.prevent="editCampaign(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                <template v-else> {{ column.data ? scope.row.data[column.prop] : scope.row[column.prop] }} </template>
            </template> 
          </el-table-column>
          <el-table-column :min-width="50" fixed="right" label="Spam test">
            <template slot-scope="props">
              <a
                v-tooltip.top-center="'Test'"
                class="btn-info btn-simple btn-link"
                @click="handleTest(props.$index, props.row)"
              >
                <i class="fa fa-heart"></i>
              </a>
            </template>
          </el-table-column>
          <el-table-column :min-width="50" fixed="right" label="Delete">
            <template slot-scope="props">
              <a
                v-tooltip.top-center="'Delete'"
                class="btn-danger btn-simple btn-link"
                @click="handleDelete(props.row)"
              >
                <i class="fa fa-times"></i>
              </a>
            </template>
          </el-table-column>
        </el-table>
      </div>

    </card>
  </div>
</template>
<script>
import { Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";
import get_campaigns from "./dummy_campaigns";
import Fuse from "fuse.js";
import CampaignWizard from "./campaignWizard.vue";
import Campaign from "./campaign.vue";
import NotificationMessage from "./Wizard/notification.vue";
import axios from "axios";

const CAMPAIGNS_API_LIST = 'http://127.0.0.1:5000/campaigns/list';
const CAMPAIGNS_API_DELETE = 'http://127.0.0.1:5000/campaigns/delete';

export default {
  components: {
    Campaign,
    CampaignWizard,
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {
  },
  data() {
    return {
        list_data : {
            campaigns : [],
            credentials: [],
            prospects_list : [],
            funnels : [],
            columns : [],

            pagination : {
                perPage : 0,
                currentPage : 1,
                perPageOptions: [5, 10, 25, 50],
                total : 0
          }
        },

      searchQuery: "",
    };
  },
  methods: {
    handleTest(index, row) {
      alert(`Your want to test ${row.name}`);
    },
    handleDelete(row) {
      let indexToDelete = this.list_data.campaigns.findIndex( tableRow => tableRow.id === row.id);
      console.log("indexToDelete: ", indexToDelete);
      if (indexToDelete >= 0) {
        //this.list_data.campaigns.splice(indexToDelete, 1);
        if (confirm("Are you sure?")) {
          console.log('delete: ', row._id.$oid);
          this.deleteCampaign(row._id.$oid);
        }
      }
    },
    deleteCampaign(id){
      const path = CAMPAIGNS_API_DELETE;

      var data = new FormData();
      data.append("_campaign_id", id);

      //console.log(data);
      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error deleting campaign " + r.msg;
            alert(msg);
          } else {
            console.log('deleted!');
            this.listData();
          }
        })
        .catch(error => {
          var msg = "Error deleting campaign " + error;
          alert(msg);
        });
    },
    initCampaigns(){
      this.listData(1,1);
    },
    listData(page=1, init=0){
        const path = CAMPAIGNS_API_LIST;
        
        var data = new FormData();
        if (init == 1){
            data.append('_init', 1);
        }
        data.append('_page', page);
        
        //console.log(data);
        axios.post(path, data)
          .then((res) => {
            var r = res.data;
            if (r.code <= 0){
              var msg = "Error loading campaigns " + r.msg;
              alert(msg);
            }else{  
              //console.log('res: ', r);
              this.update_data(r, init);
            }
          })
          .catch((error) => {
            var msg = "Error loading campaigns " + error;
            alert(msg);
          });

    },
    update_data(newJson, init){
        if (init == 1){
          this.list_data.prospects_list = JSON.parse(newJson.prospects_list);
          this.list_data.columns = JSON.parse(newJson.columns);
          this.list_data.funnels = JSON.parse(newJson.funnels);
          this.list_data.credentials = JSON.parse(newJson.credentials);
        }

        /* This will help to prevent: JSON parse error in console */
        if (newJson.campaigns){
          this.list_data.campaigns = JSON.parse(newJson.campaigns);
        }
        this.list_data.pagination = newJson.pagination;
        console.log('load from server: ', this.list_data);
    },
    async addCampaign() {
      await this.$router.push({ path: "Campaign", query: { type: 'add' } }).catch(err => {
        console.log(err);
      });
    },
    async editCampaign(msg_dict, smth) {
      await this.$router.push({ path: "Campaign", query: { type: 'edit', id: msg_dict._id.$oid } }).catch(err => {
        console.log(err);
      });
    },
  },
  created() {
    this.initCampaigns();
  }
};
</script>
<style>
</style>
