<template>
<div>
<card>
    <div class="container">
        <div class="row">
            <div class="col-4 d-flex align-self-center">
                <h3>
                <i class="nc-icon nc-bullet-list-67"></i> Campaigns
                </h3>
            </div>
            <div class="col-8 d-flex flex-row-reverse align-self-center">
                <button
                    @click.prevent="addCampaign"
                    type="button"
                    class="btn btn-default btn-success mx-1"
                >Create a Campaign</button>
                <button
                    @click.prevent="reload_campaigns"
                    type="button"
                    class="btn btn-default btn-success mx-1"
                >Refresh</button>
            </div>
        </div>
    </div>
</card>

<card>
        <div class="col-12">
            <pulse-loader :loading="loading" :color="color"></pulse-loader>
            <el-table
            v-if="!loading"
            stripe
            ref="campaigns_data_table"
            style="width: 100%;"
            :data="campaigns_data.campaigns"
            max-height="500"
            border
            >
            <el-table-column
                v-for="(column,index) in list_data.columns"
                :key="index"
                :prop="column.prop"
                :label="column.label"
                :fixed="column.prop === 'title' ? true : false"
                show-overflow-tooltip>
                <template slot-scope="scope">
                    <a @click.prevent="editCampaign(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                    <template v-else-if="column.prop === 'status'">{{  status[scope.row[column.prop]] }}</template>
                    <template v-else> {{ show_data(scope.row, column) }} </template>
                </template>
            </el-table-column>
            <el-table-column :min-width="50" fixed="left" label="">
                <template slot-scope="props">
                <a
                    v-tooltip.top-center="'View full statistics'"
                    class="btn-simple btn-link"
                    @click.prevent="detalization(props.row._id.$oid)"
                    href="#"
                >View stats
                </a>
                </template>
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Action">
                <template slot-scope="props">
                <a
                    class="btn-simple btn-link"
                    @click.prevent="make_action(props.row, props.$index)"
                    href="#"
                >
                    {{ props.row.status == 1 ? 'Pause' : 'Start' }}
                </a>
                </template>
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Delete">
                <template slot-scope="props">
                <a
                    v-tooltip.top-center="'Delete'"
                    class="btn-danger btn-simple btn-link"
                    @click.prevent="delete_campaign(props.row._id.$oid, props.$index)"
                >
                    <i class="fa fa-times"></i>
                </a>
                </template>
            </el-table-column>
            </el-table>
        </div>

        </card>

        <div v-if="test" class="row">
            <div class="col-12">
                <pre>{{ this.campaigns_data}}</pre>
            </div>

            <div class="col-12">
                {{ this.list_data }}
            </div>
        </div>

</div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js';

import axios from '@/api/axios-auth';

const CAMPAIGNS_API_DATA = '/campaigns/data'
const CAMPAIGNS_API_LIST = '/campaigns/list';

const CAMPAIGNS_API_DELETE = '/campaigns/delete';
const CAMPAIGNS_API_START = '/campaigns/start';
const CAMPAIGNS_API_PAUSE = '/campaigns/pause';

export default {
components: {
    PulseLoader,
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
        test : false,
        loading: true,
        color: "#a7a7ff",
        
        status : {
            0 : 'New',
            1 : 'In progress',
            2 : 'On Pause',
           '-1' : 'Failed',
           '-2' : 'Unknown'
        },
        pagination : {
            perPage : 0,
            currentPage : 1,
            perPageOptions: [5, 10, 25, 50],
            total : 0
        },
        list_data : {
            columns : [],
        },
        campaigns_data : {
            campaigns : []
        }
    };
},
methods: {
    detalization(campaign_id) {
      this.$router.push({
        path: "campaign_statistic",
        query: { campaign_id: campaign_id }
      });
    },
    make_action(campaign, index){
        var path = CAMPAIGNS_API_START;
        if (campaign.status == 1){
            path = CAMPAIGNS_API_PAUSE;
        }
        if (confirm("Are you sure?")) {
            var data = new FormData();
            data.append("_campaign_id", campaign._id.$oid);

            const row_index = index;
            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Action error " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_campaigns();
                }
                })
                .catch(error => {
                    var msg = "Action error " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
    },
    show_data(scope_row, column){
        var data = column.data || '';
        if (data){
            return scope_row.data[column.prop] || '';
        }else{
            var field = column.field || '';
            if (field){
                return scope_row[column.prop][field] || '';
            }else{
                return scope_row[column.prop] || '';
            }
        }

        return '';
    },
    delete_campaign(campaign_id, row_index){
        if (confirm("Are you sure?")) {
            const path = CAMPAIGNS_API_DELETE;

            var data = new FormData();
            data.append("_campaign_id", campaign_id);

            const index = row_index;
            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error deleting campaign " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_campaigns();
                }
                })
                .catch(error => {
                    var msg = "Error deleting campaign " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
    },
    addCampaign() {
        this.$router.push({path: "campaign_form"});
    },
    editCampaign(msg_dict, index) {
        var status = -2;
        if (msg_dict.hasOwnProperty('status')){
            status = msg_dict['status'];
        }
        if (status == -2 || status == 1){
            Notification.error({title: "Error", message: "Pause campaign for edit, current status: " + status});
            return false;
        }

        this.$router.push({ path: "campaign_edit_form", query: { campaign_id: msg_dict._id.$oid } })
    },
    next_page(){
        var page = 2;
        this.load_data(page,0);
    },
    reload_campaigns(event){
        return this.load_campaigns(1);
    },
    load_campaigns(page=1){
        const path = CAMPAIGNS_API_LIST;

        var data = new FormData();
        data.append('_page', page);

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading campaigns." + r.msg;
                Notification.error({title: "Error", message: msg});
            }else{
                this.deserialize_campaigns(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading campaigns. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });

    },
    load_data(){
        const path = CAMPAIGNS_API_DATA;

        var data = new FormData();
        axios
            .post(path, data)
            .then(res => {
            var r = res.data;
            if (r.code <= 0) {
                var msg = "Error loading data " + r.msg;
                Notification.error({title: "Error", message: msg});
            } else {
                this.deserialize_data(r);
            }
            })
            .catch(error => {
                var msg = "Error loading data " + error;
                Notification.error({title: "Error", message: msg});
            });
    },
    deserialize_data(from_data){
        for (var key in from_data){
            if (this.list_data.hasOwnProperty(key) && from_data[key]){
                var parsed_data = JSON.parse(from_data[key])
                this.$set(this.list_data, key, parsed_data);
            }
        }
    },
    deserialize_campaigns(from_data){
        if (from_data.pagination){
            var pagination_dict = JSON.parse(from_data.pagination);
            this.$set(this, 'pagination', pagination_dict);
        }

        if (from_data.columns){
            var columns = JSON.parse(from_data.columns);
            this.$set(this.list_data, 'columns', columns);
        }

        if (from_data.campaigns){
            var campaigns = JSON.parse(from_data.campaigns)
            this.$set(this.campaigns_data, 'campaigns', campaigns);
        }

        this.loading = false
    },

},
async mounted() {
    //await this.load_data();
    /* // loading
    let loadingInstance = Loading.service();
    this.$nextTick(() => { // Loading should be closed asynchronously
        loadingInstance.close();
    });
    let loading = this.$loading({ fullscreen: true })
    setTimeout(() => { loading.close() }, 1000)
    // https://juejin.im/post/5c8e151df265da67eb15fe09
    */

    await this.load_campaigns();
}
};
</script>
<style>
</style>
