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
      <el-progress :percentage="90" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-5">
      <div class="col-8">
        <label class="o24_text">Name your campaign</label>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="Сampaign name"
          v-model="campaign_data.title"
        ></el-input>
      </div>
    </div>

    <div class="row justify-content-md-center mb-5">
      <div class="col-8">
        <label class="o24_text">
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
      <div class="row justify-content-md-center mb-3">
        <label class="o24_text">Shedule</label>
      </div>
      <div class="row justify-content-md-center mb-5 ml-1">
        <div class="col-3">
          <label class="o24_text">Start</label>
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
        <div class="col-3">
          <label class="o24_text">End</label>
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
        <div class="col-3">
          <label class="o24_text">Time Zone</label>
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

    <div class="row justify-content-md-center mb-5 ml-5">
      <div class="col-6">
        <label class="o24_text">Sending days</label>
        <el-checkbox-group v-model="sending_days">
          <el-checkbox-button v-for="day in days" :label="day" :key="day">{{day}}</el-checkbox-button>
        </el-checkbox-group>
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
  Switch,
  CheckboxGroup,
  CheckboxButton,
} from "element-ui";

import timezones from "../../CampaignsList/defaults/timezones";
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
    [TimeSelect.name]: TimeSelect,
    [CheckboxGroup.name]: CheckboxGroup,
    [CheckboxButton.name]: CheckboxButton,
  },
  data() {
    return {
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      sending_days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],

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
  methods: {
    progress_format(percentage) {
      return '3 / 3';
    }
  },
  async mounted() {}
};
</script>
<style lang="scss">
.o24_text {
    color: #262a79;
    font-size: 20px;
}
</style>
