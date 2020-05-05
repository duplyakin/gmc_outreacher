<template>
<div>
<card>
<div class="row">
    <div class="col-4 d-flex align-self-center">
        <span font-><h3><i class="nc-icon nc-badge"></i> Prospects</h3></span>
    </div>
    <div class="col-8 d-flex flex-row-reverse align-self-center">

        <div v-if="multipleSelection.length > 0">
        <button @click.prevent="unassignProspects" type="button" class="btn btn-default btn-success mx-1">Unassign</button>
        <button @click.prevent="assignProspects" type="button" class="btn btn-default btn-success mx-1">Assign</button>
        <button @click.prevent="deleteProspects" type="button" class="btn btn-wd btn-danger mx-1">Delete</button>
        </div>
        
        <div v-if="multipleSelection.length == 0">
        <button @click.prevent="addProspect" type="button" class="btn btn-default btn-success mx-1">Add manually</button>
        <button @click.prevent="uploadProspect" type="button" class="btn btn-default btn-success mx-1">Upload</button>
        </div>
    
    </div>

</div>
</card>    

<div class="row">
<div class="col-12">
    <card title="">
    <div> 
        <div class="col-12 d-flex">
        <card title="Filter prospects by:">
            <form @submit.prevent="submit_filter">
            <div class="row">
            <div class="col-3">
                <el-select
                class="select-default mb-3"
                v-model="filters.column"
                value-key="label"
                placeholder="Filter by column">
                <el-option
                    class="select-default"
                    v-for="(column, index) in list_data.columns"
                    :key="index"
                    :label="column.label"
                    :value="column">
                </el-option>
                </el-select>      
    
            </div>
            <div class="col-5">
                <fg-input name="filterInput"
                class="mb-3"
                :disabled="filters.column.value === '' ? true : false"
                placeholder="Contains value..."
                v-model="filters.contains"/>
            </div>
            <div class="col-2">
                <el-select
                class="select-default mb-3"
                v-model="filters.assign_to"
                placeholder="Select campaign">
                <el-option
                    class="select-default"
                    v-for="campaign in list_data.campaigns"
                    :key="campaign._id.$oid"
                    :label="campaign.title"
                    :value="campaign._id.$oid">
                </el-option>
                </el-select>      
            </div>
            <div class="col-2">
                <el-select
                class="select-default mb-3"
                v-model="filters.assign_to_list"
                placeholder="Select list">
                <el-option
                    class="select-default"
                    v-for="list in list_data.lists"
                    :key="list._id.$oid"
                    :label="list.title"
                    :value="list._id.$oid">
                </el-option>
                </el-select>
    
            </div>
            </div>
            <div class="row">
                <div class="col-6 d-flex">
                    <p class="text-danger" v-if="this.service_fields.error != ''">
                    {{ this.service_fields.error }}
                    </p>  
                </div>
                <div class="col-6 d-flex flex-row-reverse">
                <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Apply Filter</button>
                <button v-on:click="filterClear" type="button" class="btn btn-outline btn-wd btn-danger">Clear Filter</button>
                </div>
            </div>
            </form>
        </card>

        </div>
        <div class="col-12">
        <el-table stripe
                    ref="prospects_data_table"
                    style="width: 100%;"
                    @selection-change="handleSelectionChange"
                    :data="prospects_data.prospects"
                    max-height="500"
                    border>
            <el-table-column
                    type="selection"
                    width="55"
                    v-if="prospects_data.prospects"
                    fixed>
            </el-table-column>
            <el-table-column v-for="(column, index) in list_data.columns"
                    :key="index"
                    :prop="column.prop"
                    :label="column.label"
                    :fixed="column.prop == 'email' ? true : false"
                    show-overflow-tooltip>
                    <template slot-scope="scope">
                        <a @click.prevent="editProspect(scope.row, scope.$index)" href="#"  v-if="column.prop == 'email'">{{ scope.row.data[column.prop] }}</a>
                        <template v-else> {{ column.data ? scope.row.data[column.prop] : scope.row[column.prop][column.field] }} </template>
                    </template>     
            </el-table-column>
        </el-table>
        </div>
    </div>
    <div slot="footer" class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
        <div class="">
        <p class="card-category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>
        </div>
        <prospect-pagination class="pagination-no-border"
                    v-model="pagination.currentPage"
                    :per-page="pagination.perPage"
                    :total="pagination.total"
                    v-on:switch-page="switchPage">
        </prospect-pagination>
    </div>      
    </card>
</div>
</div>
<div v-if="test" class="row">
    <div class="col-12">
        {{ this.prospects_data.prospects }}
    </div>
</div>

<modal
:width = "720"
name="major_modal">
</modal>

</div>
</template>
<script>
import { Table, TableColumn, Select, Option } from 'element-ui'
import ProspectPagination from './prospectPagination.vue'
import NotificationMessage from './notification.vue';

import ProspectEdit from './prospectEdit.vue'
import ProspectAssign from './prospectAssign.vue'
import CsvUpload from './upload_csv/upload.vue'

import users from './dummy.js'
import Fuse from 'fuse.js'
import axios from 'axios'

const PROSPECTS_API_DATA = 'http://127.0.0.1:5000/prospects/data';
const PROSPECTS_API_LIST = 'http://127.0.0.1:5000/prospects/list';

const PROSPECTS_API_EDIT = 'http://127.0.0.1:5000/prospects/edit';
const PROSPECTS_API_CREATE = 'http://127.0.0.1:5000/prospects/create';
const PROSPECTS_API_DELETE = 'http://127.0.0.1:5000/prospects/remove';
const PROSPECTS_API_UNASSIGN = 'http://127.0.0.1:5000/prospects/unassign';
const PROSPECTS_API_ASSIGN = 'http://127.0.0.1:5000/prospects/assign';
const PROSPECTS_API_UPLOAD = 'http://127.0.0.1:5000/prospects/upload';

export default {
components: {
    ProspectPagination,
    ProspectEdit,
    CsvUpload,
    ProspectAssign,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
computed: {
    to () {
    let highBound = this.from + this.prospects_data.pagination.perPage
    if (this.total < highBound) {
        highBound = this.total
    }
    return highBound
    },
    from () {
    return this.prospects_data.pagination.perPage * (this.prospects_data.pagination.currentPage - 1)
    },
    total () {
    return this.prospects_data.pagination.total;
    }
},
data () {     
    return {
        test : false,
        
        list_data : {
            columns : [],
            lists : [],
            campaigns: [],
        },
        pagination : {
            perPage : 0,
            currentPage : 1,
            total : 0
        },

        prospects_data: {
            prospects : [],
        },
        
        multipleSelection: [],

        filters: {
            assign_to : {
                label: 'Campaign assigned',
                value: ''
            },
            assign_to_list : {
                label : 'List assigned',
                value : ''
            },
            column : {
                label : 'Filter by colunmn',
                value : ''
            },
            contains: ''
        },

        service_fields : {
            error : '',
            message : '',
            filterOn : false
        }
    }
},
watch: {
    filters(val){
        if (val){
            this.service_fields.filterOn = true; //don't want to wait for nexttick
            this.$set(this.service_fields, 'filterOn', true);
        }
    }
},
methods: {
    switchPage(page){
        if (this.isFilterOn()){
            this.submit_filter(null, page);
        }else{
            this.load_prospects(page);
        }
    },
    deserialize_data(from_data){            
        for (var key in from_data){
            if (this.list_data.hasOwnProperty(key) && from_data[key]){
                var parsed_data = JSON.parse(from_data[key])
                this.$set(this.list_data, key, parsed_data);
            }
        }
    },
    deserialize_prospects(from_data){
        var pagination_dict = JSON.parse(from_data.pagination);
        this.$set(this, 'pagination_dict', pagination_dict);

        if (from_data.prospects){
            var prospects = JSON.parse(from_data.prospects)
            this.$set(this.prospects_data, 'prospects', prospects);
        }
    },
    isFilterOn(){
        this.service_fields.filterOn;
    },
    filterClear(){
        for (var key in this.filters){
            if (typeof this.filters[key] == Object){
                this.$set(this.filters[key], value, '');
            }else{
                this.$set(this.filters, key, '');
            }
        }

        this.service_fields.filterOn = false; //Don't want to wait for tick
        this.$set(this.service_fields, 'filterOn', false);
        this.load_prospects();
    },
    submit_filter(event, page=1) {
        if ((this.filters.value != '') & (this.filters.contains == '')){
            this.$set(this.service_fields, 'error', 'Input value for column filter...')
            return false;
        }
        this.$set(this.service_fields, 'error', '')

        this.load_prospects(page);
    },
    load_data(){
        const path = PROSPECTS_API_DATA;
    
        var data = new FormData();

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading data. " + r.msg;
                alert(msg);
            }else{
                this.deserialize_data(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading data. ERROR: " + error;
                alert(msg);
            });
    },
    load_prospects(page=1){
        const path = PROSPECTS_API_LIST;
    
        var data = new FormData();
        data.append('_page', page);
        if (this.isFilterOn()){
            data.append('_filters', JSON.stringify(this.filters))
        }

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading prospects." + r.msg;
                alert(msg);
            }else{
                this.deserialize_prospects(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading prospects. ERROR: " + error;
                alert(msg);
            });
    },
    uploadProspect(){
        this.$modal.show(CsvUpload, {
            api_url : PROSPECTS_API_UPLOAD,
            lists: this.list_data.lists,
            valueUpdated:(uploaded) => {
                this.$notify(
                {
                    component: NotificationMessage,
                    message: 'Prospect uploaded Success. The data will be available soon. Update the page in 10 seconds',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                })
            }
            },
            {
            width: '720',
            height: 'auto'
            })
    },
    addProspect(){
        const _table = this.$refs.prospects_data_table;
        this.$modal.show(ProspectEdit, {
            prospectObj: {},
            modalTitle: "Prospect create",
            action: 'create',
            api_url : PROSPECTS_API_CREATE,
            valueUpdated:(newValue) => {
                this.$notify(
                {
                    component: NotificationMessage,
                    message: 'Prospect created Success',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                })
                this.load_prospects();   
            }
            },
            {
            width: '720',
            height: 'auto'
            })
    },
    editProspect(prospect_dict, row_index) {
        const current_index = row_index;
        const _table = this.$refs.prospects_data_table;

        this.$modal.show(ProspectEdit, {
            prospectObj: prospect_dict,
            api_url : PROSPECTS_API_EDIT,
            action: 'edit',
            modalTitle: "Prospect edit",
            valueUpdated:(newValue) => {
                this.$set(this.prospects_data.prospects, current_index, newValue);
                _table.$forceUpdate();
                this.$notify(
                {
                    component: NotificationMessage,
                    message: 'Updated Success',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                })
            }
            },
            {
            width: '720',
            height: 'auto'
            })
    },
    handleSelectionChange(val) {
        this.multipleSelection = val;
    },
    assignProspects(){
    var prospects = this.multipleSelection;
    this.$modal.show(ProspectAssign, {
        campaigns: this.list_data.campaigns,
        valueUpdated: (campaign_id) => {
                
                const path = PROSPECTS_API_ASSIGN;

                var assignData = new FormData();
                assignData.append('_prospects', JSON.stringify(prospects));
                assignData.append('_campaign_id', campaign_id);


                axios.post(path, assignData)
                .then((res) => {
                    var r = res.data;
                    if (r.code <= 0){
                    var msg = "Error " + r.msg;
                    alert(msg);
                    }else{
                    this.$notify(
                    {
                        component: NotificationMessage,
                        message: 'Assign success',
                        icon: 'nc-icon nc-bulb-63',
                        type: 'success'
                    });

                    this.initProspects();
                    
                    }
                })
                .catch((error) => {
                    var msg = "Error " + error;
                    alert(msg);
                });

            //End here
        }
        },
        {
        width: '720',
        height: 'auto'
        })

    },
    unassignProspects(){
    if (confirm("Are you sure? This will stop all campaigns for prospects")){
        const path = PROSPECTS_API_UNASSIGN;

        var unassignData = new FormData();
        unassignData.append('_unassign', JSON.stringify(this.multipleSelection));

        axios.post(path, unassignData)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
            var msg = "Error " + r.msg;
            alert(msg);
            }else{
            this.$notify(
            {
                component: NotificationMessage,
                message: 'Unassign success',
                icon: 'nc-icon nc-bulb-63',
                type: 'success'
            });
            this.initProspects();
            }
        })
        .catch((error) => {
            var msg = "Error " + error;
            alert(msg);
        });

    }
    },
    deleteProspects(){
    if (confirm("Are you sure? This action CAN'T be undone")){
        const path = PROSPECTS_API_DELETE;

        var deleteData = new FormData();
        deleteData.append('_delete', JSON.stringify(this.multipleSelection));

        axios.post(path, deleteData)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
            var msg = "Error deleting prospects " + r.msg;
            alert(msg);
            }else{
            this.$notify(
            {
                component: NotificationMessage,
                message: 'Delete success',
                icon: 'nc-icon nc-bulb-63',
                type: 'success'
            });
            this.initProspects();
            }
        })
        .catch((error) => {
            var msg = "Error loading prospects " + error;
            alert(msg);
        });

    }
    },
},
async mounted () {
    await this.load_data();
    await this.load_prospects();
},
created() {

},
}
</script>
<style>
</style>
