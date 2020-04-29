<template>
<div>
    <card>
    <div class="row">
        <div class="col-12 d-flex flex-row-reverse align-self-center">
        <div>
            <input name="campaign_id"
            placeholder="Input campaign_id to test get"
            type="text"
            label="Campaign Id"
            class="mb-3"
            v-model="campaign_id_get"/>
        </div>
        <div>    
            <button @click.prevent="initCampaigns()" type="button" class="btn btn-default btn-success mx-1">Reload (INIT list campaigns)</button>
            <button @click.prevent="listCampaigns()" type="button" class="btn btn-default btn-success mx-1">List Campaigns page</button>
            <button @click.prevent="createCampaign()" type="button" class="btn btn-default btn-success mx-1">Create Campaign</button>
            <button @click.prevent="get_campaign_by_id()" type="button" class="btn btn-default btn-success mx-1">Get campaign by ID</button>
       
       </div>
        </div>
    </div>
    <div class="row">
        <div class="col-12 d-flex align-self-center">
            <p>Response from server</p>
        </div>
        <div class="col-12 d-flex align-self-center">
            <pre>{{ response_json }}</pre>
        </div>
    </div>
    <div class="row">
        <div class="col-12 d-flex align-self-center">
            <p>You sent to server</p>
        </div>
        <div class="col-12 d-flex align-self-center">
          <pre>{{ request_json }}</pre>
        </div>
    </div>

    <div class="row">
            <div class="col-12">
                <card title="Campaigns list">
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
                                    <a @click.prevent="editCampaign(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                                    <template v-else> {{ column.data ? scope.row.data[column.prop] : scope.row[column.prop] }} </template>
                                </template>     
                        </el-table-column>
                    </el-table>
                    </div>
                </div>    
                </card>
            </div>
      </div>
      
    <div class="row">
        <div class="col-12">
          <card title="Select sending days">
            <div class="btn-group">
              <button type="button" ref='day_0' @click="toggleDay('day_0')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['0'] }">Mon</button>
              <button type="button" ref='day_1' @click="toggleDay('day_1')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['1'] }">Tue</button>
              <button type="button" ref='day_2' @click="toggleDay('day_2')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['2'] }">Wed</button>
              <button type="button" ref='day_3' @click="toggleDay('day_3')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['3'] }">Thu</button>
              <button type="button" ref='day_4' @click="toggleDay('day_4')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['4'] }">Fri</button>
              <button type="button" ref='day_5' @click="toggleDay('day_5')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['5'] }">Sat</button>
              <button type="button" ref='day_6' @click="toggleDay('day_6')" v-bind:class="{ 'btn btn-default' : true, 'btn-success': days_selected['6'] }">Sun</button>
            </div>
          </card>
        </div>
    </div>

      <div class="row">
              <div class="col-12">
                  <card title="Select funnel">
                  <p>Select funnel</p>
                  <el-select
                    class="select-default mb-3"
                    v-on:change="onChangeFunnel"
                    style="width: 100%;"
                    placeholder="Select funnel"
                    v-model="funnel_selected"
                    value-key="title">
                      <el-option
                      class="select-default"
                      v-for="(funnel,index) in list_campaigns.funnels"
                      :key="funnel._id.$oid"
                      :label="funnel.title"
                      :value="funnel">
                      </el-option>
                  </el-select>  
                </card>

              </div>
      </div>
  
      <div class="row">
          <div class="col-12">
              <card title="Select prospects list">
              <p>Select prospects list</p>
              <el-select
                class="select-default mb-3"
                style="width: 100%;"
                placeholder="Select prospects list"
                v-model="prospect_list_selected">
                  <el-option
                  class="select-default"
                  v-for="(list,index) in list_campaigns.prospect_lists"
                  :key="list._id.$oid"
                  :label="list.title"
                  :value="list._id.$oid">
                  </el-option>
              </el-select>  
            </card>
          </div>
        </div>


      <div class="row">
        <div class="col-12">
          <card title="Select accounts based on medium (Linkedin or email)">
            <div v-if="hasMedium('email')" class="col-6">
                <p>Select email account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select email account"
                  v-model="email_data.email_account_selected">
                    <el-option
                    class="select-default"
                    v-for="(account,index) in list_campaigns.credentials"
                    v-if="account.medium == 'email'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account._id.$oid">
                    </el-option>
                </el-select>  
            </div>
            <div v-if="hasMedium('linkedin')" class="col-6">
                <p>Select linkedin account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select linkedin account"
                  v-model="linkedin_data.linkedin_account_selected">
                    <el-option
                    class="select-default"
                    v-for="(account,index) in list_campaigns.credentials"
                    v-if="account.medium == 'linkedin'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account._id.$oid">
                    </el-option>
                </el-select>  
            </div>
  
        </card>
      </div>
    </div>

    
    <div v-if="email_data.templates.length != 0" class="row">
            <div class="col-12">
                <card title="Email templates required">
                    <el-table stripe
                                ref="email_templates_data_table"
                                style="width: 100%;"
                                :data="email_data.templates"
                                max-height="500"
                                border>
                        <el-table-column v-for="(column, index) in email_data.table_columns"
                                :key="index"
                                :label="column.label"
                                :prop="column.prop"
                                show-overflow-tooltip>
                                <template slot-scope="scope">
                                    <a @click.prevent="editEmailTemplate(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                                    <template v-else> {{ scope.row[column.prop] }} </template>
                                </template>  
                        </el-table-column>
                    </el-table>
                  </card>
            </div>
    </div>

    <div v-if="linkedin_data.templates.length != 0" class="row">
        <div class="col-12">
            <card title="Linkedin templates required">
                <el-table stripe
                            ref="linkedin_templates_data_table"
                            style="width: 100%;"
                            :data="linkedin_data.templates"
                            max-height="500"
                            border>
                    <el-table-column v-for="(column, index) in linkedin_data.table_columns"
                            :key="index"
                            :label="column.label"
                            :prop="column.prop"
                            show-overflow-tooltip>
                            <template slot-scope="scope">
                                <a @click.prevent="editLinkedinTemplate(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                                <template v-else> {{ scope.row[column.prop] }} </template>
                            </template>  

                    </el-table-column>
                </el-table>
              </card>
        </div>
</div>
</card>
<modal
:width = "720"
name="major_modal">
</modal>

</div>
</template>
<script>
import axios from 'axios'
import { Table, TableColumn, Select, Option } from 'element-ui'
import TemplateEdit from './test_create_templates.vue'

const CAMPAIGNS_API_LIST = 'http://127.0.0.1:5000/campaigns';
const CAMPAIGNS_API_GET_BY_ID = 'http://127.0.0.1:5000/campaigns/get';
const CAMPAIGNS_API_CREATE = 'http://127.0.0.1:5000/campaigns/create';
const CAMPAIGNS_API_EDIT = 'http://127.0.0.1:5000/campaigns/edit';

export default {
components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
filters: {
    pretty: function(value) {
      try {
        return JSON.stringify(value, null, 2);
      }catch(error) {
        return error;
      }
    }
},
data() {
    return {
        response_json : '',
        request_json: '',
        funnel_selected: {},
        prospect_list_selected : '',
        campaign_id_get : '',
        
        email_data : {
          email_account_selected: '',
          templates: [],
          table_columns: [
              {
                prop: 'title',
                label: 'Template title',
                minWidth: 300
              },
              {
                prop: 'subject',
                label: 'Subject',
                minWidth: 300
              },
              {
                prop: 'interval',
                label: 'Interval',
                minWidth: 100
              }
          ]
        },

        linkedin_data : {
          linkedin_account_selected: '',
          templates: [],
          table_columns: [
             {
                prop: 'title',
                label: 'Template title',
                minWidth: 300
              },
              {
                prop: 'interval',
                label: 'Interval',
                minWidth: 100
              }
          ],
        },

        list_campaigns : {
            campaigns : [],
            credentials: [],
            prospect_lists : [],
            funnels : [],
            columns : [],

            pagination : {
                perPage : 0,
                currentPage : 1,
                total : 0
          }
        },

        days_selected : {
          '0' : true,
          '1' : true,
          '2' : true, 
          '3' : true,
          '4' : true,
          '5' : false,
          '6' : false
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
  hasMedium(medium){
    
    var templates_required = this.funnel_selected.templates_required || null;
    if (templates_required){
        var email = templates_required.email || null;
        var linkedin = templates_required.linkedin || null;

        if (medium == 'email'){
          if (email){
            return true;
          }else{
            return false;
          }
        }

        if (medium == 'linkedin'){
          if (linkedin){
            return true;
          }else{
            return false;
          }
        }
    }

    return false;
  },
  toggleDay(ref){
    var btn = this.$refs[ref];
    if (!btn){
      return false;
    }
    
    var index = ref.split('_')[1];
    
    this.days_selected[index] = !this.days_selected[index];    
    return true;
  },
  get_campaign_by_id(){
            /* SENDING TO SERVER HERE*/
        var campaign_id = this.campaign_id_get;

        var path = CAMPAIGNS_API_GET_BY_ID;
        var get_data = new FormData();
        get_data.append('_campaign_id', campaign_id);
        
        console.log(get_data);
        this.request_json = this._formdata_to_json(get_data);
        axios.post(path, get_data)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error getting campaign " + r.msg;
              alert(msg);
            }else{ 
              var updated = r.updated;
              console.log(updated);            
            }
          })
          .catch((error) => {
            var msg = "Error getting campaign " + error;
            alert(msg);
          });
  },
  editCampaign(campaign_obj, row_index){
    console.log(campaign_obj);

    var campaign_id = campaign_obj['_id']['$oid']
    console.log(campaign_id)

    var edit_data = {
            title: 'Test campaign - 22',
            templates : {
              'email' : this.email_data.templates,
              'linkedin' : this.linkedin_data.templates,
            },
            timeTable: {
              from_hour: '0',
              to_hour: '111',
              time_zone: 'time zone',
              sending_days: this.days_selected,
            },
        }
        
        /* SENDING TO SERVER HERE*/
        var path = CAMPAIGNS_API_EDIT;
        var edit_data = new FormData();
        edit_data.append('_campaign_id', campaign_id);
        edit_data.append('_edit_campaign_data', edit_data);
        
        console.log(edit_data);
        this.request_json = this._formdata_to_json(edit_data);
        axios.post(path, edit_data)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error creating campaign " + r.msg;
              alert(msg);
            }else{ 
              var updated = r.updated;
              console.log(updated);            
            }
          })
          .catch((error) => {
            var msg = "Error creating campaign " + error;
            alert(msg);
          });

  },
  editLinkedinTemplate(teamplateObj, row_index){
    var table = this.$refs['linkedin_templates_data_table'];
    this.editTemplate('linkedin', teamplateObj, row_index, table)
  },
  editEmailTemplate(teamplateObj, row_index){
    var table = this.$refs['email_templates_data_table'];
    this.editTemplate('email', teamplateObj, row_index, table)
  },
  editTemplate(template_type, teamplateObj, _row_index, _table) {
        const current_index = _row_index;
        const cuurent_table = _table;

        this.$modal.show(TemplateEdit, {
            templateObj: teamplateObj,
            template_type: template_type,
            valueUpdated:(newValue) => {
              if (template_type === 'email'){
                this.$set(this.email_data.templates, current_index, newValue);
              }else if(template_type === 'linkedin'){
                this.$set(this.linkedin_data.templates, current_index, newValue);
              }else{
                alert("Unsupported template_type")
              }

              cuurent_table.$forceUpdate();
            }
          },
          {
            width: '720',
            height: 'auto'
          })
  },
    onChangeFunnel(){
      /* update tempaltes based on selected funnel */

      /* clear all data first */
      this.email_data.templates = [];
      this.linkedin_data.templates = [];
            
      var templates_required = this.funnel_selected.templates_required || null;
      if (templates_required){
        var email = templates_required.email || null;
        if (email){
          this.email_data.templates = Object.values(email);

          /*sort by order field*/
          this.email_data.templates.sort(function(first, second) {
            return first['order'] - second['order'];
          });


        }
        var linkedin = templates_required.linkedin || null;
        if (linkedin){
          this.linkedin_data.templates = Object.values(linkedin);
          
          /*sort by order field*/
          this.linkedin_data.templates.sort(function(first, second) {
            return first['order'] - second['order'];
          });

        }
      }

      console.log("new onchangefunnel");
      console.log(this.funnel_selected);
      console.log(this.email_data.templates);
      console.log(this.linkedin_data.templates);

    },
    update_campaigns(newJson, init){
        if (init == 1){
          this.list_campaigns.prospect_lists = JSON.parse(newJson.prospect_lists);
          this.list_campaigns.columns = JSON.parse(newJson.columns);
          this.list_campaigns.funnels = JSON.parse(newJson.funnels);
          this.list_campaigns.credentials = JSON.parse(newJson.credentials);
        }

        /* This will help to prevent: JSON parse error in console */
        if (newJson.campaigns){
          this.list_campaigns.campaigns = JSON.parse(newJson.campaigns);

          /*FOR TEST ONLY - to show response in textarea. NO NEED in production */
          this.response_json = newJson;
        }
        this.list_campaigns.pagination = JSON.parse(newJson.pagination);
        console.log(this.list_campaigns);
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
        
        console.log(data);
        this.request_json = this._formdata_to_json(data);
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
        var credentials = [];

        if (this.email_data.email_account_selected.length != 0){
          console.log('email account');
          console.log(this.email_data.email_account_selected);

          credentials.push(this.email_data.email_account_selected);
        }

        if (this.linkedin_data.linkedin_account_selected.length != 0){
          console.log('linkedin account');
          console.log(this.linkedin_data.linkedin_account_selected);

          credentials.push(this.linkedin_data.linkedin_account_selected);
        }

        var campaign = {
            title: 'Test campaign - 1',
            funnel: this.funnel_selected._id.$oid,
            credentials: credentials,
            prospectsList: this.prospect_list_selected,
            templates : {
              'email' : this.email_data.templates,
              'linkedin' : this.linkedin_data.templates,
            },
            timeTable: {
              from_hour: '10',
              to_hour: '11',
              time_zone: 'time zone',
              sending_days: this.days_selected,
            },
        }
        
        var createData = new FormData();
        createData.append('_add_campaign', JSON.stringify(campaign));
        
        console.log(createData);
        this.request_json = this._formdata_to_json(createData);
        axios.post(path, createData)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error creating campaign " + r.msg;
              alert(msg);
            }else{                
            }
          })
          .catch((error) => {
            var msg = "Error creating campaign " + error;
            alert(msg);
          });
    },
    _formdata_to_json(form_data){
      var object = {};
      form_data.forEach(function(value, key){
        object[key] = value;
      });
      var json = JSON.stringify(object);
      return json;
    }

},
mounted() {
    //this.fuseSearch = new Fuse(this.tableData, {keys: ['name', 'email']});
}

};
</script>
<style>
</style>
