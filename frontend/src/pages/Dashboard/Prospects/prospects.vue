<template>
<div>
<card>
<div class="row">
    <div class="col-3 d-flex align-self-center">
        <span font-><h3><i class="nc-icon nc-layers-3"></i> Leads</h3></span>
    </div>
    <div class="col-9 d-flex flex-row-reverse align-self-center">

        <div v-if="multipleSelection.length > 0">
        <button @click.prevent="unassignProspects" type="button" class="btn btn-default btn-success mx-1">Unassign from Campaign</button>
        <button @click.prevent="assignProspects" type="button" class="btn btn-default btn-success mx-1">Assign to Campaign</button>
        <button @click.prevent="listAddProspects" type="button" class="btn btn-default btn-success mx-1">Add to list</button>
        <button @click.prevent="listRemoveProspects" type="button" class="btn btn-default btn-success mx-1">Remove from list</button>
        <button @click.prevent="stopSequenceProspects" type="button" class="btn btn-wd btn-danger mx-1">Pause actions</button>
        <button @click.prevent="deleteProspects" type="button" class="btn btn-wd btn-danger mx-1">Delete</button>
        </div>
        
        <div v-if="multipleSelection.length == 0">
        <button @click.prevent="addProspect" type="button" class="btn btn-default btn-success mx-1">Add manually</button>
        <button @click.prevent="uploadProspect" type="button" class="btn btn-default btn-success mx-1">Upload CSV</button>
        <button @click.prevent="exportAllProspects" type="button" class="btn btn-default btn-success mx-1">Export All</button>
        <button @click.prevent="reload_prospects" type="button" class="btn btn-default btn-success mx-1">Refresh</button>
        </div>
    
    </div>

</div>
</card>    

<div class="row">
<div class="col-12">
    <card title="">
    <div> 
        <div class="col-12 d-flex">
        <card title="Filter leads by:">
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
                :disabled="filters.column.prop ? false : true"
                placeholder="Contains value..."
                v-model="filters.contains"/>
            </div>
            <div class="col-2">
                <el-select
                class="select-default mb-3"
                v-model="filters.assign_to"
                value-key="title"
                placeholder="Select campaign">
                <el-option
                    class="select-default"
                    v-for="campaign in list_data.campaigns"
                    :key="campaign._id.$oid"
                    :label="campaign.title"
                    :value="campaign">
                </el-option>
                </el-select>      
            </div>
            <div class="col-2">
                <el-select
                class="select-default mb-3"
                v-model="filters.assign_to_list"
                value-key="title"
                placeholder="Select list">
                <el-option
                    class="select-default"
                    v-for="list in list_data.lists"
                    :key="list._id.$oid"
                    :label="list.title"
                    :value="list">
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
        <pulse-loader :loading="loading" :color="color"></pulse-loader>
        <div v-if="prospects_data.prospects.length > 0" class="col-12">
        <el-table stripe
                    v-if="!loading"
                    ref="prospects_data_table"
                    style="width: 100%;"
                    @selection-change="handleSelectionChange"
                    :data="prospects_data.prospects"
                    max-height="500"
                    border>
            <el-table-column
                    type="selection"
                    width="55"
                    fixed>
            </el-table-column>
            <el-table-column v-for="(column, index) in list_data.columns"
                    :key="index"
                    :prop="column.prop"
                    :label="column.label"
                    :fixed="column.prop == 'email' ? true : false"
                    show-overflow-tooltip>
                    <template slot-scope="scope">
                        <a @click.prevent="editProspect(scope.row, scope.$index)" href="#"  v-if="column.prop == 'email'">{{ show_data(scope.row, column) }}</a>
                        <template v-else> {{ show_data(scope.row, column) }} </template>
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
        <p>"LIST_DATA"</p>
        <pre>{{ this.list_data }}</pre>
    </div>
    <div class="col-12">
            <p>"pagination"</p>
            <pre>{{ this.pagination }}</pre>
        </div>   
    <div class="col-12">
        <p>"Prospects_data"</p>
        <pre>{{ this.prospects_data }}</pre>
    </div>
</div>

<modals-container/>

</div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from 'element-ui'
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'

const ProspectPagination = () => import('./prospectPagination.vue')
const NotificationMessage = () => import('./notification.vue')

const ProspectEdit = () => import('./prospectEdit.vue')
const ProspectAssign = () => import('./prospectAssign.vue')
const ProspectListAdd = () => import('./prospectListAdd.vue')

const CsvUpload = () => import('./upload_csv/upload.vue')

import Fuse from 'fuse.js'
import axios from '@/api/axios-auth'

const PROSPECTS_API_DATA = '/prospects/data';
const PROSPECTS_API_LIST = '/prospects/list';

const PROSPECTS_API_EDIT = '/prospects/edit';
const PROSPECTS_API_CREATE = '/prospects/create';
const PROSPECTS_API_DELETE = '/prospects/remove';
const PROSPECTS_SEQUENCE_STOP_API = '/prospects/sequence/stop';

const PROSPECTS_API_UNASSIGN = '/prospects/campaign/unassign';
const PROSPECTS_API_ASSIGN = '/prospects/campaign/assign';
const PROSPECTS_API_UPLOAD = '/prospects/upload';

const PROSPECTS_API_LIST_REMOVE = '/prospects/list/remove';
const PROSPECTS_API_LIST_ADD = '/prospects/list/add';

const PROSPECTS_EXPORT = '/prospects/export';

var FileSaver = require('file-saver');

export default {
components: {
    PulseLoader,
    ProspectPagination,
    ProspectEdit,
    ProspectListAdd,
    CsvUpload,
    ProspectAssign,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
computed: {
    to () {
    let highBound = this.from + this.pagination.perPage
    if (this.total < highBound) {
        highBound = this.total
    }
    return highBound
    },
    from () {
    return this.pagination.perPage * (this.pagination.currentPage - 1)
    },
    total () {
    return this.pagination.total;
    }
},
data () {     
    return {
        test : false,

        loading: true,
        color: "#a7a7ff",
        
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
            assign_to : '',
            assign_to_list : '',
            column : '',
            contains: '',
        },

        service_fields : {
            error : '',
            message : '',
            filterOn : false
        }
    }
},
watch: {
    filters: {
        handler(val){
            var empty = true;
            if (this.filters.assign_to != '' ||
                this.filters.assign_to_list != '' ||
                this.filters.column != ''){
                    empty = false;
                }

            if (!empty){
                console.log("handlers");
                this.service_fields.filterOn = true; //don't want to wait for nexttick
                this.$set(this.service_fields, 'filterOn', true);
            }
        },
        deep: true   
    }
},
methods: {
    show_data(scope_row, column){
        var data = column.data || false;
        var value = '-';

        if (data){
            value = scope_row.data[column.prop] || '-';
        }else{
            var field = column.field || ''; 
            if (field !== ''){
                if (scope_row[column.prop]){
                    value = scope_row[column.prop][column.field] || '-';
                }else{
                    value = '-';
                }
            }else{
                value = scope_row[column.prop] || '-';
            }
        }

        return value;
    },
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
        this.$set(this, 'pagination', pagination_dict);

        if (from_data.prospects){
            var prospects = JSON.parse(from_data.prospects)
            this.$set(this.prospects_data, 'prospects', prospects);
        }

        this.loading = false
    },
    serialize_fitler(filter){
        var res = {
            column : '',
            contains: '',
            assign_to : '',
            assign_to_list : '',
        }
        
        var column = filter.column.prop || '';
        if (column){
            res.column = column;
            res.contains = filter.contains;
        }

        var assign_to = filter.assign_to._id || '';
        if (assign_to){
            res.assign_to = assign_to.$oid || '';
        }

        var assign_to_list = filter.assign_to_list._id || '';
        if (assign_to_list){
            res.assign_to_list = assign_to_list.$oid || '';
        }

        console.log(res);
        return JSON.stringify(res)
    },
    isFilterOn(){
        return this.service_fields.filterOn;
    },
    filterClear(){
        for (var key in this.filters){
            this.$set(this.filters, key, '');
        }

        this.service_fields.filterOn = false; //Don't want to wait for tick
        this.$set(this.service_fields, 'filterOn', false);
        this.$set(this.service_fields, 'error', '');

        this.load_prospects();
    },
    submit_filter(event, page=1) {
        if (!this.isFilterOn()){
            return false;
        }

        if ((this.filters.column != '') & (this.filters.contains == '')){
            this.$set(this.service_fields, 'error', 'Input value for column filter...')
            return false;
        }
        this.$set(this.service_fields, 'error', '')

        console.log(this.filters);
        console.log(this.service_fields);

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
                Notification.error({title: "Error", message: msg});
            }else{
                this.deserialize_data(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading data. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });
    },
    reload_prospects(event){
        this.load_prospects();
    },
    load_prospects(page=1){
        const path = PROSPECTS_API_LIST;
    
        var data = new FormData();
        data.append('_page', page);
        if (this.isFilterOn()){
            console.log("sending with fitler");
            var filters = this.serialize_fitler(this.filters);
            data.append('_filters', filters);
        }

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading leads." + r.msg;
                Notification.error({title: "Error", message: msg});
            }else{
                this.deserialize_prospects(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading leads. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });
    },
    uploadProspect(){
        this.$modal.show(CsvUpload, {
            api_url : PROSPECTS_API_UPLOAD,
            lists: this.list_data.lists,
            valueUpdated:(uploaded) => {
                this.load_prospects();
                Notification.success({title: "Success", message: "Upload could take some time, please wait and press RELOAD"});
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    exportAllProspects(){
        if (confirm("Are you sure? (It will take some time)")){
            const path = PROSPECTS_EXPORT;

            var data = new FormData();

            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code <= 0){
                    var msg = "Error code: " + r.msg;
                    Notification.error({title: "Error", message: msg});
                }else{
                    var csv =r.csv;
                    if (csv){
                        var file = new File([csv], "export.csv", {type: "text/csv;charset=utf-8"});
                        FileSaver.saveAs(file);
                    }else{
                        var msg = "Something went wrong, try again or contact support: " + r.msg;
                        Notification.error({title: "Error", message: msg});
                    }
                }
            })
            .catch((error) => {
                var msg = "Error: " + error;
                Notification.error({title: "Error", message: msg});
            });
        }
    },
    addProspect(){
        const _table = this.$refs.prospects_data_table;
        this.$modal.show(ProspectEdit, {
            prospectObj: {},
            modalTitle: "Add lead manually",
            action: 'create',
            api_url : PROSPECTS_API_CREATE,
            valueUpdated:(newValue) => {
                Notification.success({title: "Success", message: "Lead added"});
                this.load_prospects();   
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
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
                Notification.success({title: "Success", message: "Updated"});
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    handleSelectionChange(val) {
        this.multipleSelection = val;
    },
    listAddProspects(){
        var prospects = this.multipleSelection;
        this.$modal.show(ProspectListAdd, {
            lists: this.list_data.lists,
            valueUpdated: (list_id) => {
                    const path = PROSPECTS_API_LIST_ADD;

                    var assignData = new FormData();
                    assignData.append('_prospects', JSON.stringify(prospects));
                    assignData.append('_list_id', list_id);


                    axios.post(path, assignData)
                    .then((res) => {
                        var r = res.data;
                        if (r.code <= 0){
                            var msg = "Error " + r.msg;
                            Notification.error({title: "Error", message: msg});
                        }else{
                            Notification.success({title: "Success", message: "Added to list"});
                            this.load_prospects();            
                        }
                    })
                    .catch((error) => {
                        var msg = "Error " + error;
                        Notification.error({title: "Error", message: msg});
                    });

                //End here
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    listRemoveProspects(){
        if (confirm("Are you sure? This action CAN'T be undone")){

            var prospects = this.multipleSelection;
            const path = PROSPECTS_API_LIST_REMOVE;

            var data = new FormData();
            data.append('_prospects', JSON.stringify(prospects));


            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code <= 0){
                    var msg = "Error code: " + r.msg;
                    Notification.error({title: "Error", message: msg});
                }else{
                    Notification.success({title: "Success", message: "Removed"});
                    this.load_prospects();
                }
            })
            .catch((error) => {
                var msg = "Catch Error: " + error;
                Notification.error({title: "Error", message: msg});
            });
        }
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
                        Notification.error({title: "Error", message: msg});
                        }else{
                            Notification.success({title: "Success", message: "Assigned"});
                            this.load_prospects();
                        }
                    })
                    .catch((error) => {
                        var msg = "Error " + error;
                        Notification.error({title: "Error", message: msg});
                    });

                //End here
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    unassignProspects(){
    if (confirm("Are you sure? This will stop all campaigns for leads.")){
        const path = PROSPECTS_API_UNASSIGN;

        var unassignData = new FormData();
        unassignData.append('_unassign', JSON.stringify(this.multipleSelection));

        axios.post(path, unassignData)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
            var msg = "Error " + r.msg;
            Notification.error({title: "Error", message: msg});
            }else{
                Notification.success({title: "Success", message: "Unassigned"});
                this.load_prospects();
            }
        })
        .catch((error) => {
            var msg = "Error " + error;
            Notification.error({title: "Error", message: msg});
        });

    }
    },
    stopSequenceProspects() {
        if (confirm("Stop actions for this leads?")) {

            const path = PROSPECTS_SEQUENCE_STOP_API;

            var data = new FormData();
            data.append('_prospects', JSON.stringify(this.multipleSelection));

            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code <= 0){
                var msg = "Error stopping actions for leads: " + r.msg;
                Notification.error({title: "Error", message: msg});
                } else {
                    Notification.success({title: "Success", message: "Actions stopped"});
                    this.load_prospects();
                }
            })
            .catch((error) => {
                var msg = "Error stopping actions for leads: " + error;
                Notification.error({title: "Error", message: msg});
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
            var msg = "Error deleting leads: " + r.msg;
            Notification.error({title: "Error", message: msg});
            }else{
                Notification.success({title: "Success", message: "Deleteed"});
                this.load_prospects();
            }
        })
        .catch((error) => {
            var msg = "Error loading leads: " + error;
            Notification.error({title: "Error", message: msg});
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
