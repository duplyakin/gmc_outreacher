<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="goto_previous_step" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Settings</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="goto_next_step" type="primary" style="font-size: 26px; border: none;">{{action}}</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="90" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-5">
      <div class="col-8">
        <label class="o24_text">Name your campaign</label>
        <el-input
          placeholder="Сampaign name"
          v-model="campaign_data.title"
        ></el-input>
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
            v-model="campaign_data.time_zone"
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
        <el-checkbox-group v-model="campaign_data.sending_days">
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

import utils from "@/utils/campaign_utils";

const CURRENT_PATH = "/campaign_form_leads";

const CAMPAIGNS_API_ADD = "/campaigns/parsing/create";
const CAMPAIGNS_API_EDIT = "/campaigns/parsing/edit";

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
      action_type: 'create',
      path: CAMPAIGNS_API_ADD + CURRENT_PATH,
      action: 'Save draft',

      next_step: '/campaigns', // expected default value
      previous_step: '/campaign_data_form_accounts', // expected default value

      /* All defaults that you store on client */
      timezones_selects: timezones,
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],

      /* All lists that we need to select */
      list_data: {
        credentials: [],
      },

      /* Object data */
      campaign_data: {
        title: "",
        credentials: [],

        from_hour: "",
        to_hour: "",
        time_zone: "",
        sending_days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
      }
    };
  },
  methods: {
    progress_format(percentage) {
      return '4 / 4'
    },

    async goto_next_step() {
      let next_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!next_step.hasOwnProperty('path') || !next_step.path) {
        next_step.path = this.next_step
      }
      if(next_step.hasOwnProperty('error') && next_step.error) {
        Notification.error({ title: "Error", message: next_step.error })
      }
      this.$router.push({ path: next_step.path, query: { action_type: this.action_type } })
    },

    async goto_previous_step() {
      let previous_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!previous_step.hasOwnProperty('path') || !previous_step.path) {
        previous_step.path = this.previous_step
      }
      if(previous_step.hasOwnProperty('error') && previous_step.error) {
        Notification.error({ title: "Error", message: previous_step.error })
      }
      this.$router.push({ path: previous_step.path, query: { action_type: this.action_type } })
    }
  },
  async mounted() {
    let action_type = this.$route.query.action_type || ''
    if (action_type != '' && action_type.includes('edit')) {
      this.$set(this, 'action_type', 'edit')
      this.$set(this, 'path', CAMPAIGNS_API_EDIT + CURRENT_PATH)
    }

    let result = await utils.load_data(this.path, this.campaign_data, this.list_data)

    if(result.hasOwnProperty('list_data') && result.list_data) {
      this.$set(this, 'list_data', result.list_data)
    }
    if(result.hasOwnProperty('campaign_data') && result.campaign_data) {
      this.$set(this, 'campaign_data', result.campaign_data)
    }
    if(result.hasOwnProperty('action') && result.action) {
      this.$set(this, 'action', result.action)
    }
    if(result.hasOwnProperty('error') && result.error) {
      Notification.error({ title: "Error", message: result.error })
    }
  }
};
</script>
<style lang="scss">
.o24_text {
    color: #262a79;
    font-size: 20px;
}
</style>
