<template>
<div>
    <card>
    <div class="row">
        <div class="col-12 d-flex flex-row-reverse align-self-center">
        <div>            
            <button @click.prevent="initCampaigns()" type="button" class="btn btn-default btn-success mx-1">Init List Campaigns</button>
            <button @click.prevent="listCampaigns()" type="button" class="btn btn-default btn-success mx-1">List Campaigns page</button>
            <button @click.prevent="createCampaign()" type="button" class="btn btn-default btn-success mx-1">Create Campaign</button>
            <button @click.prevent="editCampaign()" type="button" class="btn btn-default btn-success mx-1">Edit Campaign</button>
        </div>
        </div>
    </div>
    <div class="row">
        <div class="col-12 d-flex align-self-center">
            <p>Response from server</p>
        </div>
        <div class="col-12 d-flex align-self-center">
        <textarea style="width:100%;height: 500px;" ref="response_json">
            {{ response_json }}
        </textarea>
        </div>
    </div>
    <div class="row">
            <div class="col-12">
                <card title="">
                <div> 
                    <div class="col-12">
                    <el-table stripe
                                ref="campaigns_data_table"
                                style="width: 100%;"
                                :data="list_campaigns.campaigns"
                                max-height="500"
                                border>
                        <el-table-column v-for="column in list_campaigns.columns"
                                :key="column.label"
                                :prop="column.prop"
                                :label="column.label"
                                :fixed="column.prop === 'title' ? true : false"
                                show-overflow-tooltip>
                                <template slot-scope="scope">
                                    <a v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                                    <template v-else> {{ column.data ? scope.row.data[column.prop] : scope.row[column.prop] }} </template>
                                </template>     
                        </el-table-column>
                    </el-table>
                    </div>
                </div>    
                </card>
            </div>
            </div>
    </card>
</div>
</template>
<script>
import axios from 'axios'
import { Table, TableColumn, Select, Option } from 'element-ui'

const CAMPAIGNS_API_LIST = 'http://127.0.0.1:5000/campaigns';
const CAMPAIGNS_API_CREATE = 'http://127.0.0.1:5000/campaigns/create';


export default {
components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
data() {
    return {
        response_json : '',
        
        list_campaigns : {
            campaigns : [],
            prospect_lists : [],
            funnels : [],
            columns : [],

            pagination : {
                perPage : 0,
                currentPage : 1,
                total : 0
          }
        },

        create_campaign : {

        },

        delete_campaign : {

        },

        edit_campaign : {

        }
    }
},
methods: {
    update_campaigns(newJson, init){
        if (init == 1){
          this.list_campaigns.campaigns = JSON.parse(newJson.campaigns);
          this.list_campaigns.prospect_lists = JSON.parse(newJson.prospect_lists);
          this.list_campaigns.columns = JSON.parse(newJson.columns);
          this.list_campaigns.funnels = JSON.parse(newJson.funnels);
        }

        /* This will help to prevent: JSON parse error in console */
        if (newJson.campaigns){
          this.list_campaigns.campaigns = JSON.parse(newJson.campaigns);

          /*FOR TEST ONLY - to show response in textarea. NO NEED in production */
          this.response_json = newJson;
        }
        this.list_campaigns.pagination = JSON.parse(newJson.pagination);

    },
    initCampaigns(){
        this.listCampaigns(1,1);
    },
    listCampaigns(page=1, init=0){
        const path = CAMPAIGNS_API_LIST;
        
        var data = new FormData();
        if (init == 1){
            data.append('_init', 1);
        }
        data.append('_page', page);

        axios.post(path, data)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error loading campaigns " + r.msg;
              alert(msg);
            }else{                
              this.update_campaigns(r, init);
            }
          })
          .catch((error) => {
            var msg = "Error loading campaigns " + error;
            alert(msg);
          });

    },
    createCampaign(){
        const path = CAMPAIGNS_API_CREATE;
        
        var  campaign = {
            title: 'Test campaign',
            funnel: '5ea85e28b0bc52fb021b0fcf',
            credentials: ['5ea85e27b0bc52fb021b0f93', '5ea85e27b0bc52fb021b0f95'],
            prospectsList: '5ea85e2fb0bc52fb021b0fe6',
            messagesListEmail: '',
            messagesListLinkedin: '',
            timeTable: {
                from: 'String',
                till: '',
                timezone: 'String',
                days: '',
            },
        }

        var createData = new FormData();
        createData.append('_add_campaign', created_campaign);

        axios.post(path, createData)
          .then((res) => {
            var r = res.data;
            if (r.code <= 0){
              var msg = "Error creating campaign " + r.msg;
              alert(msg);
            }else{                
              this.initCampaigns();
            }
          })
          .catch((error) => {
            var msg = "Error creating campaign " + error;
            alert(msg);
          });
    },
    editCampaign(){

    }
},
mounted() {
    //this.fuseSearch = new Fuse(this.tableData, {keys: ['name', 'email']});
}
};
</script>
<style>
</style>
