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
          :data="campaigns_data.campaigns"
          max-height="500"
          border
        >
          <el-table-column
            v-for="column in campaigns_data.columns"
            :key="column.label"
            :prop="column.prop"
            :label="column.label"
            :fixed="column.label === 'Campaign name' ? true : false"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <a
                @click.prevent="editCampaign(scope.row)"
                href="#"
                v-if="column.label === 'Campaign name'"
              >{{ scope.row[column.prop] }}</a>
              <template v-else>{{ scope.row[column.prop] }}</template>
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
                @click="handleDelete(props.$index, props.row)"
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
import NotificationMessage from "./Wizard/notification.vue";

export default {
  components: {
    CampaignWizard,
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {
    pagedData() {
      return this.campaigns_data.campaigns.slice(this.from, this.to);
    },
    /***
     * Searches through table data and returns a paginated array.
     * Note that this should not be used for table with a lot of data as it might be slow!
     * Do the search and the pagination on the server and display the data retrieved from server instead.
     * @returns {computed.pagedData}
     */
    queriedData() {
      let result = this.campaigns_data.campaigns;
      if (this.searchQuery !== "") {
        result = this.fuseSearch.search(this.searchQuery);
        this.pagination.total = result.length;
      }
      return result.slice(this.from, this.to);
    },
    to() {
      let highBound = this.from + this.pagination.perPage;
      if (this.total < highBound) {
        highBound = this.total;
      }
      return highBound;
    },
    from() {
      return this.pagination.perPage * (this.pagination.currentPage - 1);
    },
    total() {
      this.pagination.total = this.campaigns_data.campaigns.length;
      return this.campaigns_data.campaigns.length;
    }
  },
  data() {
    return {
      pagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      searchQuery: "",

      campaigns_data: {
        columns: [
          {
            prop: "name",
            label: "Campaign name",
            minWidth: 300
          },
          {
            prop: "funnel",
            label: "Type",
            minWidth: 100
          },
          {
            prop: "account",
            label: "From account",
            minWidth: 100
          },
          {
            prop: "prospectsList",
            label: "Prospects list",
            minWidth: 100
          }
        ],

        campaigns: [],

        pagination: {
          perPage: 0,
          currentPage: 1,
          total: 0
        }
      },
    };
  },
  methods: {
    initCampaigns(){
      //TODO: connect server
      this.campaigns_data.campaigns = get_campaigns;
    },
    handleTest(index, row) {
      alert(`Your want to like ${row.name}`);
    },
    handleDelete(index, row) {
      let indexToDelete = this.campaigns_data.campaigns.findIndex(
        tableRow => tableRow.id === row.id
      );
      if (indexToDelete >= 0) {
        this.campaigns_data.campaigns.splice(indexToDelete, 1);
      }
    },
    async addCampaign() {
      await this.$router.push({ path: "CampaignWizard", query: { type: 'add' } }).catch(err => {
        console.log(err);
      });
    },
    async editCampaign(msg_dict) {
      await this.$router.push({ path: "CampaignWizard", query: { type: 'edit', id: msg_dict.id } }).catch(err => {
        console.log(err);
      });
    },
    validate() {
      //this.$store.commit("step_2_email", this.campaigns_data.campaigns);

      return this.$validator.validateAll().then(res => {
        this.$emit("on-validated", 1, res, this.model);
        return res;
      });
    }
  },
  created() {
    this.initCampaigns();
  }
};
</script>
<style>
</style>
