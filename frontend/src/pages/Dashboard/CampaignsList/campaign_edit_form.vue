<template>
<div>
        <card>
                <card>
                    <p>Campaign title (required)</p>
                    <el-input
                        placeholder="Input campaign title" 
                        v-model="campaign_data.title">
                    </el-input>
                </card>                        
            
                <card v-if="campaign_data.templates.email && campaign_data.templates.email.length != 0">
                    <p>Edit Email templates</p>
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
                
                <card v-if="campaign_data.templates.linkedin && campaign_data.templates.linkedin.length != 0">
                    <p>Edit Linkedin templates</p>
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
                
                <card>
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
                            @click.prevent="save_changes"
                            type="button"
                            class="btn btn-default btn-success mx-1"
                            >Save Changes</button>
                      <!--  <button type="button" class="btn btn-outline btn-wd btn-danger">Discard</button> -->
                    </div>
                </div>
            </card>
            
</card>
    <div v-if="test" class="row">
        <div class="col-12">
            <p>TEST RESPONSE</p>
            {{ this.test_response }}
        </div>
        
        <div class="col-12">
            <p>CAMPAIGN_DATA</p>
            {{ this.campaign_data }}
        </div>
        <div class="col-12">
        <p>MODIFIED_FIELDS</p>
        <pre>{{ this.modified_fields}}</pre>
        </div>
        <div class="col-12">
        <p>LIST_DATA</p>

        <pre>{{ this.list_data}}</pre>
        </div>
    </div>
</div>
</template>
<script>
import { drop, every, forEach, some, get, isArray, map, set, findIndex } from 'lodash';

import { Notification, Table, TimeSelect, TableColumn, Select, Option, Input } from "element-ui";

import timezones from "./defaults/timezones";
import axios from '@/api/axios-auth';;

const MessageEdit = () => import('./messageEdit.vue')

const CAMPAIGNS_API_GET = '/campaigns/get';
const CAMPAIGNS_API_DATA = '/campaigns/data';
const CAMPAIGNS_API_EDIT = '/campaigns/edit';

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
            campaign_id : '',
            
            test_response : '',

            /*All defaults that you store on client*/
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
                lists: [],
                funnels: [],
                columns: []
            },

            /*Object data*/
            campaign_data : {
                title: "",
                templates: {
                    email: [],
                    linkedin: []
                },
                
                from_hour: "",
                to_hour: "",
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
                        Notification.error({title: "Error", message: "Unsupported template_type"});
                    }

                    cuurent_table.$forceUpdate();
                }
                },
                {
                width: "1100",
                height: "auto",
                scrollable: true
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
        deserialize_data(from_data){
            for (var key in from_data){
                if (this.list_data.hasOwnProperty(key) && from_data[key]){
                    var parsed_data = JSON.parse(from_data[key])
                    this.$set(this.list_data, key, parsed_data);
                }
            }
        },
        deserialize_campaign(campaign_json){
            var campaign_dict = JSON.parse(campaign_json.campaign);
            this.test_response = campaign_dict;
            
            for (var key in this.campaign_data){
                if (this.campaign_data.hasOwnProperty(key) && campaign_dict.hasOwnProperty(key) && campaign_dict[key]) {
                    if (key == 'templates'){
                        var email_templates = campaign_dict[key].email || null;
                        if (email_templates){
                            var emails = [];
                            for (var k in email_templates){
                                emails.push(email_templates[k])
                            }
                            this.$set(this.campaign_data[key], 'email', emails);
                        }

                        var linkedin_templates = campaign_dict[key].linkedin || null;
                        if (linkedin_templates){
                            var messages = [];
                            for (var k in linkedin_templates){
                                messages.push(linkedin_templates[k])
                            }
                            this.$set(this.campaign_data[key], 'linkedin', messages);
                        }
                    }else{
                        this.$set(this.campaign_data, key, campaign_dict[key]);
                    }

                }
            }
            
            var updated_from_hour = campaign_dict.from_hour + ":" + campaign_dict.from_minutes;
            var updated_to_hour = campaign_dict.to_hour + ":" + campaign_dict.to_minutes;

            this.$set(this.campaign_data, 'from_hour', updated_from_hour);
            this.$set(this.campaign_data, 'to_hour', updated_to_hour);


                        /*Not sure that we need it - but don't want to deal with concurency*/
            if (campaign_json.modified_fields){
                var modified_fields = JSON.parse(campaign_json.modified_fields);
                this.$set(this, 'modified_fields', modified_fields);
            }
            console.log(this.campaign_data);
        },
        
        
        serialize_campaign(){
            /*If need any modifications then do it here*/
            console.log(this.campaign_data);
            return JSON.stringify(this.campaign_data);
        },
        save_changes(){
            /*Simple validation */
            if (this.campaign_data.title == ''){
                Notification.error({title: "Error", message: "Title can't be empty"});
                return false;
            }


            if (this.campaign_data.from_hour == '' ||
                this.campaign_data.to_hour == ''){
                    Notification.error({title: "Error", message: "Please select Delivery time"});
                    return false;
                }
            
            var days_selected = false;
            for (var key in this.campaign_data.sending_days){
                if (this.campaign_data.sending_days[key] == true){
                    days_selected = true;
                    break;
                }
            }

            if (!days_selected){
                Notification.error({title: "Error", message: "Sending days can't be emtpy"});
                return false;
            }

            this.send_campaign_data();
        },
        send_campaign_data(){
            /* Add validation here*/

            if (confirm("Are you sure?")) {
                var path = CAMPAIGNS_API_EDIT;
                var data = new FormData();

                var serialized_campaign_data = this.serialize_campaign();
                data.append('_add_campaign', serialized_campaign_data);
                data.append('_campaign_id', this.campaign_id);
                data.append('_modified_fields', JSON.stringify(this.modified_fields));
                

                axios
                .post(path, data)
                .then(res => {
                    var r = res.data;
                    if (r.code <= 0) {
                        var msg = "Save campaign error: " + r.msg + " code:" + r.code;
                        Notification.error({title: "Error", message: msg});
                    } else {
                        this.$router.push({ path: "campaigns_new"});
                    }
                })
                .catch(error => {
                    var msg = "Save campaign ERROR: " + error;
                    Notification.error({title: "Error", message: msg});
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
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.deserialize_data(r);
                }
            })
            .catch(error => {
                var msg = "Error loading data. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });

        },
        async load_campaign(campaign_id=''){
            console.log("load_campaign id:" + campaign_id);

            if (campaign_id === ''){
                Notification.error({title: "Error", message: "ERROR loading campaign: ID can't be empty"});
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
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.deserialize_campaign(r);
                }
            })
            .catch(error => {
                var msg = "Error loading campaign. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });

        }
    },
    async mounted() {
        this.campaign_id = this.$route.query.campaign_id || '';

        await this.load_data();
        await this.load_campaign(this.campaign_id);
    }
};
</script>
<style lang="scss">
</style>
