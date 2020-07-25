<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="$router.push('/campaign_form_sequence')" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Settings</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button type="primary" style="font-size: 26px; border: none;">Save draft</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="90"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label style="color: #262a79; font-size: 20px;">Name your campaign</label>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="Сampaign name"
          v-model="campaign_data.title"
        ></el-input>
      </div>
    </div>

    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label style="color: #262a79; font-size: 20px;">Choose Email account or <a href="/accounts" style="color: #409EFF;">add new</a></label>
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
    </div>

    <div class="container">
      <div class="row justify-content-md-center mb-5">
        <div class="col-lg-3">
          <label style="color: #262a79; font-size: 20px;">Start</label>
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
        <div class="col-lg-3">
          <label style="color: #262a79; font-size: 20px;">End</label>
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
        <div class="col-lg-3">
          <label style="color: #262a79; font-size: 20px;">Time Zone</label>
          <el-select
            class="select-primary"
            name="Time Zone"
            size="large"
            placeholder="Select Time Zone"
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
    </div>

    <div class="row justify-content-md-center">
        <div class="col-8">
          <div class="btn-group">
              <button
                type="button"
                ref="day_0"
                style="background-color: #409EFF;"
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
          </div>
      </div>

    <modals-container />
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
  Input,
  Button,
  Progress,
} from "element-ui";

import Editor from "@tinymce/tinymce-vue";
import timezones from "./defaults/timezones";
import axios from "@/api/axios-auth";

const MessageEdit = () => import("./messageEdit.vue");

const CAMPAIGNS_API_GET = "/campaigns/get";
const CAMPAIGNS_API_DATA = "/campaigns/data";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
    editor: Editor,
    [Progress.name]: Progress,
    [Button.name]: Button,
    [Input.name]: Input,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect
  },
  data() {
    return {
      test: false,

      interval: 1,
      subject: '',

      template: {
        body: ''
      },
      editorSettings: {
        height: 200,
        menubar: false,
        plugins: [
          "advlist autolink lists link image charmap print preview anchor",
          "searchreplace visualblocks code fullscreen",
          "insertdatetime media table paste code help wordcount autoresize emoticons"
        ],
        toolbar:
          "undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help \
           image | link | autolink | emoticons",
      },


      action_type: "",
      campaign_id: "",

      email_account_selected: "",
      linkedin_account_selected: "",
      timezones_selected: "",

      /*All defaults that you store on client*/
      timezones_selects: timezones,
      modified_fields: {},

      email_table_columns: [
        {
          prop: "title",
          label: "Template name",
          minWidth: 300
        },
        {
          prop: "subject",
          label: "Subject",
          minWidth: 300
        },
        {
          prop: "interval",
          label: "Delay (days)",
          minWidth: 100
        }
      ],

      linkedin_table_columns: [
        {
          prop: "title",
          label: "Template name",
          minWidth: 300
        },
        {
          prop: "interval",
          label: "Delay (days)",
          minWidth: 100
        }
      ],

      /* All lists that we need to select */
      list_data: {
        credentials: [],
        lists: [],
        funnels: [],
        columns: []
      },

      /*Object data*/
      campaign_data: {
        campaign_type: 0,
        list_selected: "",
        title: "",
        funnel: {},
        credentials: [],
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
    };
  },
  methods: {
  },
  async mounted() {
  }
};
</script>
<style lang="scss">
.action_text {
    color: #262a79;
    //font-family: NeurialGrotesk-Medium;
    font-size: 20px;
}
.new_step {
    color: #dcdce6;
    letter-spacing: 1px;
    //font-family: NeurialGrotesk-Medium;
    font-size: 26px;
    line-height: 80px;
}
</style>
