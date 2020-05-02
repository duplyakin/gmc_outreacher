<template>
<div>
<card>
    <card>
        <p>Campaign title (required)</p>
        <el-input
            :disabled="!modified_fields['title']"
            placeholder="Input campaign title" 
            v-model="campaign_data.title">
        </el-input>
    </card>
    <card>
        <p>Select prospects list to send data to (required)</p>
        <el-select
        class="select-default mb-3"
        style="width: 100%;"
        placeholder="Select prospects list"
        v-model="campaign_data.prospects_list"
        value-key="title"
        :disabled="!modified_fields['prospects_list']">
        <el-option
            class="select-default"
            v-for="(list,index) in list_data.prospects_list"
            :key="list._id.$oid"
            :label="list.title"
            :value="list"
        ></el-option>
        </el-select>
    </card>
    
    <card>
        <p>Funnel to use for communication (required)</p>
        <el-select
            class="select-default mb-3"
            name="Campaign funnel"
            v-on:change="onChangeFunnel"
            style="width: 100%;"
            placeholder="Select funnel"
            v-model="campaign_data.funnel"
            value-key="title">
        <el-option
          class="select-default"
          v-for="(funnel,index) in list_data.funnels"
          :key="funnel._id.$oid"
          :label="funnel.title"
          :value="funnel"
        ></el-option>
      </el-select>
    </card>

    <card v-if="hasMedium('any')">
        <div v-if="hasMedium('email')" class="col-6">
            <p>Select Email account</p>
            <el-select
                class="select-default mb-3"
                style="width: 100%;"
                placeholder="Select email account"
                v-on:change="onChangeEmailCredentials"
                v-model="email_account_selected"
                value-key="data.account"
                :disabled="!modified_fields['credentials']">
                <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'email'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account"
                ></el-option>
            </el-select>
        </div>

        <div v-if="hasMedium('linkedin')" class="col-6">
            <p>Select Linkedin account</p>
            <el-select
                class="select-default mb-3"
                style="width: 100%;"
                placeholder="Select linkedin account"
                v-on:change="onChangeLinkedinCredentials"
                v-model="linkedin_account_selected"
                value-key="data.account"
                :disabled="!modified_fields['credentials']">
                <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'linkedin'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account"
                ></el-option>
            </el-select>
        </div>    
    </card>


    <card v-if="modified_fields['templates'] && campaign_data.templates.email.length != 0">
        <p>Fill Email templates</p>
        <el-table
        stripe
        ref="email_templates_data_table"
        style="width: 100%;"
        :data="campaign_data.templates.email"
        max-height="500"
        border
        >
        <el-table-column
            v-for="(column, index) in email_table_columns"
            :key="index"
            :label="column.label"
            :prop="column.prop"
            show-overflow-tooltip>
            <template slot-scope="scope">
            <a
                @click.prevent="editEmailTemplate(scope.row, scope.$index)"
                href="#"
                v-if="column.prop === 'title'"
            >{{ scope.row[column.prop] }}</a>
            <template v-else>{{ scope.row[column.prop] }}</template>
            </template>
        </el-table-column>
        </el-table>
    </card>
    
    <card v-if="modified_fields['templates'] && campaign_data.templates.linkedin.length != 0">
        <p>Fill Linkedin templates</p>
        <el-table
        stripe
        ref="linkedin_templates_data_table"
        style="width: 100%;"
        :data="campaign_data.templates.linkedin"
        max-height="500"
        border
        >
        <el-table-column
            v-for="(column, index) in linkedin_table_columns"
            :key="index"
            :label="column.label"
            :prop="column.prop"
            show-overflow-tooltip
        >
            <template slot-scope="scope">
            <a
                @click.prevent="editLinkedinTemplate(scope.row, scope.$index)"
                href="#"
                v-if="column.prop === 'title'"
            >{{ scope.row[column.prop] }}</a>
            <template v-else>{{ scope.row[column.prop] }}</template>
            </template>
        </el-table-column>
        </el-table>
    </card>
    
    <card v-if="modified_fields['time_table']">
    <h5 class="text-center">Delivery time with respect to prospect's timezone</h5>
    <div class="extended-forms">
        <card>
        <div class="col-12">
            <div class="row">
            <div class="col-lg-6">
                <h4 class="title">From</h4>
                <el-time-select
                    name="From time"
                    v-model="campaign_data.from_hour"
                    :picker-options="{
                        start: '00:00',
                        step: '00:15',
                        end: '23:59'
                    }"
                    placeholder="Select time"
                ></el-time-select>
            </div>
            <div class="col-lg-6">
                <h4 class="title">Till</h4>
                <el-time-select
                    name="Till time has to be after FROM time"
                    v-model="campaign_data.to_hour"
                    :picker-options="{
                        start: '00:00',
                        step: '00:15',
                        end: '23:59'
                    }"
                    placeholder="Select time"
                ></el-time-select>
            </div>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
            <h4 class="title">Fallback Time Zone</h4>
                <el-select
                class="select-primary"
                name="Fallback Time Zone"
                size="large"
                placeholder="Fallback Time Zone"
                v-model="timezones_selected"
                >
                <el-option
                    v-for="option in timezones_selects"
                    class="select-primary"
                    :value="option.value"
                    :label="option.label"
                    :key="option.label"
                ></el-option>
                </el-select>
            </div>
        </div>
        </card>
    </div>
    <h4 class="title">Days Preference</h4>
    <div class="row">
        <div class="col-12">
        <card title="Select sending days">
            <div class="btn-group">
            <button
                type="button"
                ref="day_0"
                @click="toggleDay('day_0')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['0'] }"
            >Mon</button>
            <button
                type="button"
                ref="day_1"
                @click="toggleDay('day_1')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['1'] }"
            >Tue</button>
            <button
                type="button"
                ref="day_2"
                @click="toggleDay('day_2')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['2'] }"
            >Wed</button>
            <button
                type="button"
                ref="day_3"
                @click="toggleDay('day_3')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['3'] }"
            >Thu</button>
            <button
                type="button"
                ref="day_4"
                @click="toggleDay('day_4')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['4'] }"
            >Fri</button>
            <button
                type="button"
                ref="day_5"
                @click="toggleDay('day_5')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['5'] }"
            >Sat</button>
            <button
                type="button"
                ref="day_6"
                @click="toggleDay('day_6')"
                v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['6'] }"
            >Sun</button>
            </div>
        </card>
        </div>
    </div>
</card>

<card>
    <div class="row">
        <div class="col-12 d-flex flex-row-reverse">
                <button
                type="button"
                class="btn btn-default btn-success mx-1"
                >Save Campaign</button>
            <button type="button" class="btn btn-outline btn-wd btn-danger">Discard</button>
        </div>
    </div>
</card>


</card>
    <div v-if="test" class="row">
        <div class="col-12">
            {{ this.campaign_data.credentials }}
        </div>
        <div class="col-12">
        <pre>{{ this.modified_fields}}</pre>
        </div>
        <div class="col-12">
        <pre>{{ this.campaign_data}}</pre>
        </div>
        <div class="col-12">
        <pre>{{ this.list_data}}</pre>
        </div>
    </div>
</div>
</template>
<script>
import { drop, every, forEach, some, get, isArray, map, set, findIndex } from 'lodash';

import { Table, TimeSelect, TableColumn, Select, Option, Input } from "element-ui";

import timezones from "./defaults/timezones";
import axios from "axios";
import MessageEdit from "./messageEdit.vue";

const CAMPAIGNS_API_GET = 'http://127.0.0.1:5000/campaigns/get';
const CAMPAIGNS_API_DATA = 'http://127.0.0.1:5000/campaigns/data';

const CAMPAIGNS_API_ADD = 'http://127.0.0.1:5000/campaigns/create';
const CAMPAIGNS_API_EDIT = 'http://127.0.0.1:5000/campaigns/edit';

export default {
    components: {
        [Input.name]: Input,
        [Select.name]: Select,
        [Option.name]: Option,
        [Table.name]: Table,
        [TableColumn.name]: TableColumn,
        [TimeSelect.name] : TimeSelect
    },
    data() {
        return {
            test : false,

            action_type : '',
            campaign_id : '',

            email_account_selected : '',
            linkedin_account_selected : '',
            timezones_selected: "",

            /*All defaults that you store on client*/
            timezones_selects: timezones,
            modified_fields : {},

            email_table_columns : [
                {
                    prop: "title",
                    label: "Template title",
                    minWidth: 300
                },
                {
                    prop: "subject",
                    label: "Subject",
                    minWidth: 300
                },
                {
                    prop: "interval",
                    label: "Interval",
                    minWidth: 100
                }
            ],

            linkedin_table_columns : [
                {
                    prop: "title",
                    label: "Template title",
                    minWidth: 300
                },
                {
                    prop: "interval",
                    label: "Interval",
                    minWidth: 100
                }
            ],
        
            /* All lists that we need to select */
            list_data : {
                credentials: [],
                prospects_list: [],
                funnels: [],
                columns: []
            },

            /*Object data*/
            campaign_data : {
                title: "",
                funnel: {},
                credentials: [],
                prospects_list: {},
                templates: {
                    email: [],
                    linkedin: []
                },
                
                from_hour: "",
                to_hour: "",
                time_zone: "",
                sending_days: {
                    "0": true,
                    "1": true,
                    "2": true,
                    "3": true,
                    "4": true,
                    "5": false,
                    "6": false
                }
            }
        }
    },
    methods: {
        toggleDay(ref) {
            var btn = this.$refs[ref];
            if (!btn) {
                return false;
            }

            var index = ref.split("_")[1];

            this.campaign_data.sending_days[index] = !this.campaign_data.sending_days[index];
            return true;
        },
        editLinkedinTemplate(teamplateObj, row_index) {
            var table = this.$refs["linkedin_templates_data_table"];
            this.editTemplate("linkedin", teamplateObj, row_index, table);
        },
        editEmailTemplate(teamplateObj, row_index) {
            var table = this.$refs["email_templates_data_table"];
            this.editTemplate("email", teamplateObj, row_index, table);
        },
        editTemplate(template_type, templateObj, _row_index, _table) {
            const current_index = _row_index;
            const cuurent_table = _table;

            this.$modal.show(
                MessageEdit,
                {
                templateObj: templateObj,
                template_type: template_type,
                valueUpdated: newValue => {
                    if (template_type === "email") {
                        this.$set(this.campaign_data.templates.email, current_index, newValue);
                    } else if (template_type === "linkedin") {
                        this.$set(this.campaign_data.templates.linkedin, current_index, newValue);
                    } else {
                        alert("Unsupported template_type");
                    }

                    cuurent_table.$forceUpdate();
                }
                },
                {
                width: "720",
                height: "auto"
                }
            );
        },


        hasMedium(medium) {
            var templates_required = this.campaign_data.funnel.templates_required || null;
            if (templates_required) {
                var email = templates_required.email || null;
                var linkedin = templates_required.linkedin || null;
                if (medium == 'any'){
                    if (email || linkedin){
                        return true;
                    }else{
                        return false;
                    }
                }

                if (medium == "email") {
                    if (email) {
                        return true;
                    } else {
                        return false;
                    }
                }

                if (medium == "linkedin") {
                    if (linkedin) {
                        return true;
                    } else {
                        return false;
                    }
                }
            }

            return false;
        },
        onChangeEmailCredentials(new_credentials){
            return this.onChangeCredentials('email', new_credentials)
        },
        onChangeLinkedinCredentials(new_credentials){
            return this.onChangeCredentials('linkedin', new_credentials)
        },
        onChangeCredentials(medium, new_credentials){
            if (this.campaign_data.credentials.length <= 0){
                this.campaign_data.credentials.push(new_credentials);
                return;
            }else{
                let _medium = medium;
                var index = findIndex(this.campaign_data.credentials, function(el) { return el.medium == _medium; });
                if (index >= 0){
                    this.campaign_data.credentials.splice(index, 1, new_credentials);
                }else{
                    /*Should never happened*/
                    this.campaign_data.credentials.push(new_credentials);
                }
                return;
            }

        },
        _clear_funnel_dependent_data(){
            this.$set(this.campaign_data, 'templates', {
                email : [],
                linkedin : []
            });
            this.$set(this.campaign_data, 'credentials', []);
            this.email_account_selected = '';
            this.linkedin_account_selected = '';

        },
        onChangeFunnel() {
            this._clear_funnel_dependent_data()

            var templates_required = this.campaign_data.funnel.templates_required || null;
            if (templates_required) {
                var email = templates_required.email || null;
                if (email) {
                    var email_templates = Object.values(email);
                    /*sort by order field*/
                    email_templates.sort(function(first, second) {
                        return first["order"] - second["order"];
                    });

                    this.$set(this.campaign_data.templates, 'email', email_templates);
                }

                var linkedin = templates_required.linkedin || null;
                if (linkedin) {
                    var linkedin_templates = Object.values(linkedin);

                    /*sort by order field*/
                    linkedin_templates.sort(function(first, second) {
                        return first["order"] - second["order"];
                    });

                    this.$set(this.campaign_data.templates, 'linkedin', linkedin_templates);
                }
            }
        },
        deserialize_data(from_data){            
            for (var key in from_data){
                if (this.list_data.hasOwnProperty(key) && from_data[key]){
                    var parsed_data = JSON.parse(from_data[key])
                    this.$set(this.list_data, key, parsed_data);
                }
            }

            /*Not sure that we need it - but don't want to deal with concurency*/
            if (from_data.modified_fields  && this.action_type != 'edit'){
                var modified_fields = JSON.parse(from_data.modified_fields);
                this.$set(this, 'modified_fields', modified_fields);
            }
        },
        deserialize_campaign(campaign_json){
            var campaign_dict = JSON.parse(campaign_json.campaign);
           
            for (var key in campaign_dict){
                if (this.campaign_data.hasOwnProperty(key) && campaign_dict[key]){
                    /*Check or validate for custom keys here*/
                    if (key == 'templates'){
                        var email_templates = campaign_dict[key].email || null;
                        if (email_templates){
                            this.$set(this.campaign_data[key], 'email', email_templates);
                        }

                        var linkedin_templates = campaign_dict[key].linkedin || null;
                        if (linkedin_templates){
                            this.$set(this.campaign_data[key], 'linkedin', linkedin_templates);
                        }
                    }else{
                        this.$set(this.campaign_data, key, campaign_dict[key]);
                    }
                }
            }

                        /*Not sure that we need it - but don't want to deal with concurency*/
            if (campaign_json.modified_fields){
                var modified_fields = JSON.parse(campaign_json.modified_fields);
                this.$set(this, 'modified_fields', modified_fields);
            }

        },
        
        
        serialize_campaign(){

            /*If need any modifications then do it here*/
            return JSON.stringify(this.campaign_data);
        },
        send_campaign_data(){
            /* Add validation here*/

            if (confirm("Are you sure?")) {
                var path = CAMPAIGNS_API_ADD;
                var data = new FormData();

                var serialized_campaign_data = this.serialize_campaign();

                if (this.action_type == 'edit'){
                    path = CAMPAIGNS_API_EDIT;
                    data.append('_campaign_id', this.campaign_id)
                    data.append('_modified_fields', JSON.stringify(this.modified_fields))
                    data.append('_edit_campaign_data', serialized_campaign_data);
                }else{
                    data.append('_add_campaign', serialized_campaign_data);
                }

                axios
                .post(path, data)
                .then(res => {
                    var r = res.data;
                    if (r.code <= 0) {
                        var msg = "Save campaign error: " + r.msg + " code:" + r.code;
                        alert(msg);
                    } else {
                        /*update here*/
                    }
                })
                .catch(error => {
                    var msg = "Save campaign ERROR: " + error;
                    alert(msg);
                });

            
            }
        },
        async load_data(){
            console.log("load_data");

            var path = CAMPAIGNS_API_DATA
            var data = new FormData();

            axios
            .post(path, data)
            .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error loading data " + r.msg + " code:" + r.code;
                    alert(msg);
                } else {
                    this.deserialize_data(r);
                }
            })
            .catch(error => {
                var msg = "Error loading data. ERROR: " + error;
                alert(msg);
            });

        },
        async load_campaign(campaign_id=''){
            console.log("load_campaign id:" + campaign_id);

            if (campaign_id === ''){
                alert("ERROR loading campaign: ID can't be empty");
                return;
            }

            var path = CAMPAIGNS_API_GET;
            var data = new FormData();
            data.append('_campaign_id', campaign_id);
            
            axios
            .post(path, data)
            .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error loading campaign " + r.msg + " code:" + r.code;
                    alert(msg);
                } else {
                    this.deserialize_campaign(r);
                }
            })
            .catch(error => {
                var msg = "Error loading campaign. ERROR: " + error;
                alert(msg);
            });

        }
    },
    async mounted() {
        this.action_type = this.$route.query.action_type;
        this.campaign_id = this.$route.query.campaign_id || '';
        console.log("mounted with action_type:" + this.action_type + " campaign_id:" + this.campaign_id);


        await this.load_data();

        if (this.action_type == 'edit'){
            await this.load_campaign(this.campaign_id);
        }
    }
};
</script>
<style lang="scss">
</style>
