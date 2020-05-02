<template>
<div>
<card>
<div class="row">
    <div class="col-4 d-flex align-self-center">
        <h3>
        <i class="nc-icon nc-badge"></i> Campaigns
        </h3>
    </div>
    <div class="col-8 d-flex flex-row-reverse align-self-center">
    <div>
        <button
            @click.prevent="addCampaign()"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Add Campaign</button>
        <button
            @click.prevent="load_data(1,1)"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Reload table</button>

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
                v-for="(column,index) in list_data.columns"
                :key="index"
                :prop="column.prop"
                :label="column.label"
                :fixed="column.prop === 'title' ? true : false"
                show-overflow-tooltip>
                <template slot-scope="scope">
                    <a @click.prevent="editCampaign(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                    <template v-else> {{ column.data ? scope.row.data[column.prop] : scope.row[column.prop] }} </template>
                </template> 
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Delete">
                <template slot-scope="props">
                <a
                    v-tooltip.top-center="'Delete'"
                    class="btn-danger btn-simple btn-link"
                    @click="delete_campaign(props.row._id.$oid, props.$index)"
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

import CampaignForm from "./campaign_form.vue";
import axios from "axios";

const CAMPAIGNS_API_LIST = 'http://127.0.0.1:5000/campaigns/list';

const CAMPAIGNS_API_DELETE = 'http://127.0.0.1:5000/campaigns/delete';
const CAMPAIGNS_API_START = 'http://127.0.0.1:5000/campaigns/start';
const CAMPAIGNS_API_PAUSE = 'http://127.0.0.1:5000/campaigns/pause';

export default {
components: {
    CampaignForm,
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
    };
},
methods: {
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
                    alert(msg);
                } else {
                    this.campaigns.splice(index, 1);
                }
                })
                .catch(error => {
                    var msg = "Error deleting campaign " + error;
                    alert(msg);
                });
        }
    },
    addCampaign() {
        this.$router.push({ path: "campaign_form", query: { action_type: 'add' } })
    },
    editCampaign(msg_dict, index) {
        this.$router.push({ path: "campaign_form", query: { action_type: 'edit', campaign_id: msg_dict._id.$oid } })
    },
    next_page(){
        var page = 2;
        this.load_data(page,0);
    },
    load_data(page=1, init=0){
        const path = CAMPAIGNS_API_LIST;

        var data = new FormData();
        data.append("_init", init);
        data.append("_page", page);

        axios
            .post(path, data)
            .then(res => {
            var r = res.data;
            if (r.code <= 0) {
                var msg = "Error loading campaigns " + r.msg;
                alert(msg);
            } else {
                this.update_data(r,init);
            }
            })
            .catch(error => {
                var msg = "Error loading campaigns " + error;
                alert(msg);
            });
    },
    update_data(new_data, init){
        if (init == 1){
            this.list_data.prospects_list = JSON.parse(new_data.prospects_list);
            this.list_data.columns = JSON.parse(new_data.columns);
            this.list_data.funnels = JSON.parse(new_data.funnels);
            this.list_data.credentials = JSON.parse(new_data.credentials);
        }

        if (new_data.campaigns){
            this.list_data.campaigns = JSON.parse(new_data.campaigns);
        }
    },
},
mounted() {
    this.load_data(1,1);
}
};
</script>
<style>
</style>
