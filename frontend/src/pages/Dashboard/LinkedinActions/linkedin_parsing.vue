<template>
  <div>
    <card>
      <card>
        <p>Campaign title (required)</p>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="Input campaign title"
          v-model="campaign_data.title"
        ></el-input>
      </card>

      <card v-if="modified_fields['credentials']">
        <div class="col-6">
          <p>Select Linkedin account</p>
          <el-select
            class="select-default mb-3"
            style="width: 100%;"
            placeholder="Select linkedin account"
            v-on:change="onChangeLinkedinCredentials"
            v-model="linkedin_account_selected"
            value-key="data.account"
            :disabled="!modified_fields['credentials']"
          >
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

      <card v-if="modified_fields['lists']">
        <p>Prospects list title</p>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="Input prospects list title"
          v-model="campaign_data.list_title"
        ></el-input>
      </card>

      <card>
        <p>Search url</p>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="ex: https://www.linkedin.com/search/results/all/?keywords=company&origin=GLOBAL_SEARCH_HEADER&page=97"
          v-model="campaign_data.data.search_url"
        ></el-input>
      </card>

      <card>
      <p>LinkedIn pages settings</p>
      <div class="container">
            <p class="interval_text">Total pages required</p>
            <div class="col-3">
              <fg-input label>
                <el-input-number v-model="campaign_data.data.total_pages" placeholder="ex: 1.00" :min="1" :max="8000000000"></el-input-number>
              </fg-input>
            </div>
            <p class="interval_text">Number of pages for iteration (10 recommended)</p>

            <div class="col-3">
              <fg-input label>
                <el-input-number v-model="campaign_data.data.interval_pages" placeholder="ex: 10.00" :min="1" :max="1000"></el-input-number>
              </fg-input>
            </div>
          </div>
      </card>

      <card v-if="modified_fields['time_table']">
        <h5 class="text-center">Search time with respect to prospect's timezone</h5>
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
                  value-key="label"
                >
                  <el-option
                    v-for="option in timezones_selects"
                    class="select-primary"
                    :value="option"
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

    <div v-if="test" class="row">
      <div class="col-12">{{ this.campaign_data.credentials }}</div>
      <div class="col-12">
        <pre>modified_fields: {{ this.modified_fields}}</pre>
      </div>
      <div class="col-12">
        <pre>campaign_data: {{ this.campaign_data}}</pre>
      </div>
      <div class="col-12">
        <pre>list_data: {{ this.list_data}}</pre>
      </div>
    </div>
    
  </div>
</template>
<script>
import {
  drop,
  every,
  forEach,
  some,
  get,
  isArray,
  map,
  set,
  findIndex
} from "lodash";

import {
  Notification,
  Table,
  TimeSelect,
  TableColumn,
  Select,
  Option,
  Input
} from "element-ui";

import timezones from "../CampaignsList/defaults/timezones";
import axios from '@/api/axios-auth';

const CAMPAIGNS_API_GET = "/campaign/linkedin/get";
const CAMPAIGNS_API_DATA = "/campaign/linkedin/data";

const CAMPAIGNS_API_ADD = "/campaign/linkedin/parsing/create";
const CAMPAIGNS_API_EDIT = "/campaign/linkedin/edit";

export default {
  components: {
    [Input.name]: Input,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect
  },
  data() {
    return {
      test: true,

      action_type: "",
      campaign_id: "",

      linkedin_account_selected: "",
      timezones_selected: "",

      /*All defaults that you store on client*/
      timezones_selects: timezones,
      modified_fields: {},

      /* All lists that we need to select */
      list_data: {
        credentials: [],
        lists: [],
        columns: []
      },

      /*Object data*/
      campaign_data: {
        list_title: '',
        data: {
            search_url: '',
            total_pages: 100,
            interval_pages: 10,
        },
        title: "",
        credentials: [],

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
    };
  },
  methods: {
    toggleDay(ref) {
      var btn = this.$refs[ref];
      if (!btn) {
        return false;
      }

      var index = ref.split("_")[1];

      this.campaign_data.sending_days[index] = !this.campaign_data.sending_days[
        index
      ];
      return true;
    },
    onChangeEmailCredentials(new_credentials) {
      return this.onChangeCredentials("email", new_credentials);
    },
    onChangeLinkedinCredentials(new_credentials) {
      return this.onChangeCredentials("linkedin", new_credentials);
    },
    onChangeCredentials(medium, new_credentials) {
      if (this.campaign_data.credentials.length <= 0) {
        this.campaign_data.credentials.push(new_credentials);
        return;
      } else {
        let _medium = medium;
        var index = findIndex(this.campaign_data.credentials, function(el) {
          return el.medium == _medium;
        });
        if (index >= 0) {
          this.campaign_data.credentials.splice(index, 1, new_credentials);
        } else {
          /*Should never happened*/
          this.campaign_data.credentials.push(new_credentials);
        }
        return;
      }
    },
    deserialize_data(from_data) {
      console.log('from_data: ', from_data);
      for (var key in from_data) {
        if (this.list_data.hasOwnProperty(key) && from_data[key]) {
          var parsed_data = JSON.parse(from_data[key]);
          this.$set(this.list_data, key, parsed_data);
        }
      }
      /*Not sure that we need it - but don't want to deal with concurency*/
      if (from_data.modified_fields && this.action_type != "edit") {
        var modified_fields = JSON.parse(from_data.modified_fields);
        this.$set(this, "modified_fields", modified_fields);
      }
    },
    deserialize_campaign(campaign_json) {
      var campaign_dict = JSON.parse(campaign_json.campaign);

      for (var key in campaign_dict) {
        if (this.campaign_data.hasOwnProperty(key) && campaign_dict[key]) {
            this.$set(this.campaign_data, key, campaign_dict[key]);
        }
      }

      var updated_from_hour = campaign_dict.from_hour + ":" + campaign_dict.from_minutes;
      var updated_to_hour = campaign_dict.to_hour + ":" + campaign_dict.to_minutes;

      this.$set(this.campaign_data, 'from_hour', updated_from_hour);
      this.$set(this.campaign_data, 'to_hour', updated_to_hour);
      this.timezones_selected = this.campaign_data.time_zone;

      console.log("campaign_data: ", this.campaign_data);

      /*Not sure that we need it - but don't want to deal with concurency*/
      if (campaign_json.modified_fields) {
        var modified_fields = JSON.parse(campaign_json.modified_fields);
        this.$set(this, "modified_fields", modified_fields);
      }
    },

    serialize_campaign() {
      /*If need any modifications then do it here*/

      return JSON.stringify(this.campaign_data);
    },
    save_changes() {
      /*Simple validation */
      if (this.campaign_data.title == "") {
        Notification.error({ title: "Error", message: "Title can't be empty" });
        return false;
      }

      if (this.campaign_data.list_title == "" && this.modified_fields['lists']) {
        Notification.error({
          title: "Error",
          message: "You need to enter prospects list title"
        });
        return false;
      }

      if (this.campaign_data.data.search_url == "") {
        Notification.error({
          title: "Error",
          message: "You need to enter search url"
        });
        return false;
      }

      var credentials = this.campaign_data.credentials;
      if (credentials.length == 0) {
        Notification.error({
          title: "Error",
          message: "You need to select account"
        });
        return false;
      }

      if (this.campaign_data.from_hour == "" || this.campaign_data.to_hour == "" || this.timezones_selected == "") {
          Notification.error({title: "Error", message: "Please select Delivery time"});
          return false;
      } else {
        this.campaign_data.time_zone = this.timezones_selected;
      }

      var days_selected = false;
      for (var key in this.campaign_data.sending_days) {
        if (this.campaign_data.sending_days[key] == true) {
          days_selected = true;
          break;
        }
      }

      if (!days_selected) {
        Notification.error({
          title: "Error",
          message: "Sending days can't be emtpy"
        });
        return false;
      }

      this.send_campaign_data();
    },
    send_campaign_data() {
      /* Add validation here*/

      if (confirm("Are you sure?")) {
        var path = CAMPAIGNS_API_ADD;
        var data = new FormData();

        var serialized_campaign_data = this.serialize_campaign();
        data.append("_add_campaign", serialized_campaign_data);

        if (this.action_type == "edit") {
          path = CAMPAIGNS_API_EDIT;
          data.append("_campaign_id", this.campaign_id);
          data.append("_modified_fields", JSON.stringify(this.modified_fields));
        }

        axios
          .post(path, data)
          .then(res => {
            var r = res.data;
            if (r.code <= 0) {
              var msg = "Save campaign error: " + r.msg + " code:" + r.code;
              Notification.error({ title: "Error", message: msg });
            } else {
              Notification.success({ title: "Success", message: "Action created" });
              console.log("campaign_data: ", this.campaign_data);
              this.$router.push({ path: "linkedin_actions" });
            }
          })
          .catch(error => {
            var msg = "Save campaign ERROR: " + error;
            Notification.error({ title: "Error", message: msg });
          });
      }
    },
    async load_data() {
      var path = CAMPAIGNS_API_DATA;
      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading data " + r.msg + " code:" + r.code;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.deserialize_data(r);
          }
        })
        .catch(error => {
          var msg = "Error loading data. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    async load_campaign(campaign_id = "") {
      console.log("load_campaign id:" + campaign_id);

      if (campaign_id === "") {
        Notification.error({
          title: "Error",
          message: "ERROR loading campaign: ID can't be empty"
        });
        return;
      }

      var path = CAMPAIGNS_API_GET;
      var data = new FormData();
      data.append("_campaign_id", campaign_id);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading campaign " + r.msg + " code:" + r.code;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.deserialize_campaign(r);
          }
        })
        .catch(error => {
          var msg = "Error loading campaign. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    }
  },
  async mounted() {
    this.action_type = this.$route.query.action_type;
    this.campaign_id = this.$route.query.campaign_id || "";

    console.log("mounted with action_type:" + this.action_type + " campaign_id:" + this.campaign_id);

    await this.load_data();

    if (this.action_type == "edit") {
      await this.load_campaign(this.campaign_id);
    }
  }
};
</script>
<style lang="scss">

</style>
