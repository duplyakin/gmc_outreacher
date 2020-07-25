<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button
          @click="$router.push('/campaign_data_form_sequence')"
          type="info"
          plain
          icon="el-icon-back"
          style="font-size: 40px; border: none;"
        ></el-button>
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
        <label style="color: #262a79; font-size: 20px;">
          Choose LinkedIn account or
          <a href="/accounts" style="color: #409EFF;">add new</a>
        </label>
        <el-select
          class="select-default mb-3"
          style="width: 100%;"
          placeholder="Select linkedin account"
          v-on:change="onChangeEmailCredentials"
          v-model="email_account_selected"
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

    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['2']" active-text="Sun"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['0']" active-text="Mon"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['1']" active-text="Tues"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['2']" active-text="Wed"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['2']" active-text="Wed"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['2']" active-text="Wed"></el-switch>
      </div>
    </div>
    <div class="row justify-content-md-center mb-3">
      <div class="col-4">
        <el-switch v-model="campaign_data.sending_days['2']" active-text="Wed"></el-switch>
      </div>
    </div>

    <div class="row justify-content-md-center">
      <div class="col-4">
        <div class="btn-group">
          <button
            type="button"
            ref="day_0"
            style="background-color: #409EFF; border-color: #409EFF;"
            @click="toggleDay('day_0')"
            v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['0'] }"
          >Mon</button>
          <el-button
            ref="day_0"
            style="background-color: #409EFF; border-color: #409EFF;"
            @click="toggleDay('day_0')"
            v-bind:class="{ 'btn btn-default' : true, 'btn-success': campaign_data.sending_days['0'] }"
          >Mon</el-button>
        </div>
      </div>
    </div>

    <modals-container />
  </div>
</template>
<script>
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
  Switch
} from "element-ui";

import timezones from "../CampaignsList/defaults/timezones";
import axios from "@/api/axios-auth";

const CAMPAIGNS_API_GET = "/campaigns/get";
const CAMPAIGNS_API_DATA = "/campaigns/data";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
    [Switch.name]: Switch,
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
        list_title: "",
        data: {
          search_url: "",
          total_pages: 100,
          interval_pages: 20
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
  methods: {},
  async mounted() {}
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
