<template>
<div>
<card>
<div class="row">
    <div class="col-4 d-flex align-self-center">
        <h3>
        <i class="nc-icon nc-badge"></i> Statistics
        </h3>
    </div>
    <div class="col-8 d-flex flex-row-reverse align-self-center">
    <div>
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
            :data="list_data.statistics"
            max-height="500"
            border
            >
            <el-table-column type="expand">
                <template slot-scope="props">
                    <p>Emails opened: {{ props.row.aggregated.prospects_email_opens_total }}</p>
                    <p>LinkedIn 404 acconts: {{ props.row.aggregated.linkedin_accounts_404 }}</p>
                    <p>Bounced emails: {{ props.row.aggregated.email_bounced_total }}</p>
                    <p>LinkedIn messages failed: {{ props.row.aggregated.linkedin_messages_failed_total }}</p>
                </template>
            </el-table-column>
            <el-table-column
                v-for="(column,index) in columns"
                :key="index"
                :prop="column.prop"
                :label="column.label"
                :fixed="column.prop === 'title' ? true : false"
                show-overflow-tooltip>
                <template slot-scope="scope">
                    <a @click.prevent="detalization(scope.row)" href="#" v-if="column.prop === 'title'">{{ scope.row.campaign[column.prop] }}</a>
                    <template v-else> {{ column.campaign ? (column.prop === 'prospects_list' ? scope.row.campaign[column.prop].title : scope.row.campaign[column.prop]) : scope.row.aggregated[column.prop] }} </template>
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

import axios from "axios";
import dummy_statistics from "./dummy_statistics"; // test data

const STATISTICS_API_LIST = 'http://127.0.0.1:5000/statistics/list';

export default {
components: {
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
        columns: [
            {
                prop: "title",
                label: "Titile",
                campaign: true,
                minWidth: 300
            },
            {
                prop: "funnel",
                label: "Funnel",
                campaign: true,
                minWidth: 100
            },
            {
                prop: "prospects_list",
                label: "Prospects list",
                campaign: true,
                minWidth: 100
            },
            {
                prop: "prospects_contacted_total",
                label: "Prospects contacted",
                minWidth: 50
            },

            {
                prop: "prospects_accepted_linkedin_total",
                label: "LinkedIn accepts",
                minWidth: 50
            },
            {
                prop: "replied_total",
                label: "Replies",
                minWidth: 50
            }
        ],
        list_data : {
            statistics : [],
        },
    };
},
methods: {
    detalization(msg_dict) {
        this.$router.push({ path: "statistics_detailed", query: { campaign_id: msg_dict.campaign.id } })
    },
    next_page(){
        var page = 2;
        this.load_data(page, 0);
    },
    load_data_1(){
        const path = STATISTICS_API_LIST;

        var data = new FormData();
        data.append("_page", 1);

        axios
            .post(path, data)
            .then(res => {
            var r = res.data;
            if (r.code <= 0) {
                var msg = "Error loading campaigns statistics " + r.msg;
                alert(msg);
            } else {
                this.deserialize_data(r, init);
            }
            })
            .catch(error => {
                var msg = "Error loading campaigns statistics " + error;
                alert(msg);
            });
    },
    load_data(){
        this.deserialize_data(dummy_statistics);
    },
    deserialize_data(new_data){
        for (var key in new_data){
                if (this.list_data.hasOwnProperty(key) && new_data[key]){
                    //var parsed_data = JSON.parse(new_data[key]);
                    var parsed_data = new_data[key];
                    this.$set(this.list_data, key, parsed_data);
                }
        }
        console.log(this.list_data)

    },
},
mounted() {
    this.load_data();
}
};
</script>
<style>
</style>
