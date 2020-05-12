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
              <form @submit.prevent="submitFilter">
              <div class="row">
                <div class="col-3">
                    <el-select
                    class="select-default mb-3"
                    v-model="filters.column"
                    placeholder="Filter by column">
                    <el-option
                      class="select-default"
                      v-for="column in prospects_data.columns"
                      :key="column.label"
                      :label="column.label"
                      :value="column.label">
                    </el-option>
                  </el-select>      
        
                </div>
                <div class="col-5">
                 <fg-input name="filterInput"
                    class="mb-3"
                    :disabled="filters.column === '' ? true : false"
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
                      v-for="campaign in prospects_data.campaigns"
                      :key="campaign._id.$oid"
                      :label="campaign.title"
                      :value="campaign.title">
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
                      v-for="list in prospects_data.lists"
                      :key="list._id.$oid"
                      :label="list.title"
                      :value="list.title">
                    </el-option>
                  </el-select>
      
                </div>
              </div>
              <div class="row">
                  <div class="col-6 d-flex">
                      <p class="text-danger" v-if="this.filters.error != ''">
                        {{ this.filters.error }}
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
                      v-if="prospects_data.columns"
                      fixed>
              </el-table-column>
              <el-table-column v-for="column in prospects_data.columns"
                        :key="column.label"
                        :prop="column.prop"
                        :label="column.label"
                        :fixed="column.label === 'Email' ? true : false"
                        show-overflow-tooltip>
                        <template slot-scope="scope">
                          <a @click.prevent="editProspect(scope.row, scope.$index)" href="#"  v-if="column.label === 'email'">{{ scope.row.data[column.prop] }}</a>
                          <template v-else> {{ mapTo(scope.row, column.prop) }} </template>
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
                        v-model="prospects_data.pagination.currentPage"
                        :per-page="prospects_data.pagination.perPage"
                        :total="prospects_data.pagination.total"
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
  import { Notification, Table, TableColumn, Select, Option } from 'element-ui'
  import ProspectPagination from './prospectPagination.vue'
  import NotificationMessage from './notification.vue';

  import ProspectEdit from './prospectEdit.vue'
  import ProspectAssign from './prospectAssign.vue'
  import CsvUpload from './upload_csv/upload.vue'

  import users from './dummy.js'
  import Fuse from 'fuse.js'
  import axios from '@/api/axios-auth'

  const PROSPECTS_API_LIST = 'http://127.0.0.1:5000/prospects';
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

        mapped_ids : {},

        prospects_data: {
          columns : null,
          lists : null,
          campaigns: null,

          prospects : [],

          pagination : {
            perPage : 0,
            currentPage : 1,
            total : 0
          }
        },
        multipleSelection: [],

        filters: {
          assign_to : '',
          assign_to_list : '',
          column : '',
          contains: '',
          error: '',
          message: ''
        }
      }
    },
    methods: {
      switchPage(page){
        this.submitFilter(event=null, page=page);
      },
      update_prospects_data(newData, init=0){
        if (init == 1){
          this.prospects_data.campaigns = JSON.parse(newData.campaigns);
          this.prospects_data.lists = JSON.parse(newData.lists);
          this.prospects_data.columns = JSON.parse(newData.columns);
          
          var _this = this;
          this.prospects_data.lists.forEach(function(list){
            _this.mapped_ids[list['_id']['$oid']] = list['title'];
          })

          this.prospects_data.campaigns.forEach(function(campaign){
            _this.mapped_ids[campaign['_id']['$oid']] = campaign['title'];
          })
        }

        if (newData.prospects){
          this.prospects_data.prospects = JSON.parse(newData.prospects);
        }
        this.prospects_data.pagination = JSON.parse(newData.pagination);
      },
      filterClear(){
        this.filters.column = '';
        this.filters.assign_to = '';
        this.filters.assign_to_list = '';
        this.filters.contains = '';
        this.filters.error = '';

        this.submitFilter(event=null);
      },
      submitFilter(event, page=1) {
        if ((this.filters.column != '') & (this.filters.contains == '')){
          this.filters.error = 'Input value for column filter...';
          return false;
        }
        this.filters.error = '';

        var filterFormData = new FormData();
        filterFormData.append('_filters', JSON.stringify(this.filters));
        filterFormData.append('_page', page);

        const path = PROSPECTS_API_LIST;
        
        axios.post(path, filterFormData)
        .then((res) => {
            var r = res.data;
            if (r.code > 0){
              this.prospects_data.prospects = [];
              this.update_prospects_data(r);
            }else{
                var msg = 'Server Error loading prospects ' + r.msg;
                Notification.error({title: "Error", message: msg});
            }
        })
        .catch((error) => {
            var msg = 'Error loading prospects ' + error;
            Notification.error({title: "Error", message: msg});
        });

      },
      initProspects() {
        this.filterClear();

        const path = PROSPECTS_API_LIST;
        
        var initData = new FormData();
        initData.append('_init', 1);

        axios.post(path, initData)
          .then((res) => {
            var r = res.data;
            if (r.code <= 0){
              var msg = "Error loading prospects " + r.msg;
              Notification.error({title: "Error", message: msg});
            }else{
              this.update_prospects_data(r, 1);
            }
          })
          .catch((error) => {
            var msg = "Error loading prospects " + error;
            Notification.error({title: "Error", message: msg});
          });
      },
      uploadProspect(){
        this.$modal.show(CsvUpload, {
            api_url : PROSPECTS_API_UPLOAD,
            lists: this.prospects_data.lists,
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
                this.initProspects();   
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
            campaigns: this.prospects_data.campaigns,
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
                      Notification.error({title: "Error", message: msg});
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
                Notification.error({title: "Error", message: msg});
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
                var msg = "Error deleting prospects " + r.msg;
                Notification.error({title: "Error", message: msg});
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
              Notification.error({title: "Error", message: msg});
            });

        }
      },
      mapTo(data, prop){
        if (prop == 'assign_to_list'){
           return this.mapped_ids[data[prop]['$oid']];
        }else if (prop == 'assign_to'){
          return this.mapped_ids[data[prop]['$oid']];
        }else{
          return data['data'][prop];
        }
        return ''
      }
    },
    mounted () {
      this.initProspects();
    },
    created() {
    },
  }
</script>
<style>
</style>
