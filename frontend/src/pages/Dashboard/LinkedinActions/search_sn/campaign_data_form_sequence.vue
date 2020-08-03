<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="goto_previous_step" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Add Leads from LinkedIn URL</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="goto_next_step" type="primary" style="font-size: 26px; border: none;">{{action}}</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="50" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label class="o24_text">Paste here your LinkedIn URL</label>
        <el-input
          placeholder="LinkedIn search URL"
          v-model="campaign_data.search_url"
        ></el-input>
      </div>
    </div>

    <div class="row justify-content-md-center">
      <div class="ml-auto">
        <a href="https://www.linkedin.com/sales/search/people" target="_blank" style="color: #c4c6d5; font-size: 15px; letter-spacing: 1px; padding-bottom: 3px; border-bottom: 1px solid #d2dee0;">Go to LinkedIn Sales Navigator search</a>
      </div>
      <div class="col-2">
      </div>
    </div>
    
    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label>Number of pages per day</label>
        <el-slider v-model="campaign_data.data.interval_pages" max="100"></el-slider>
      </div>
    </div>

    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label>Total number of pages to search</label>
        <el-slider v-model="campaign_data.data.total_pages" max="1000"></el-slider>
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
  Slider,
} from "element-ui";

import utils from "@/utils/campaign_utils";

const CURRENT_PATH = "/campaign_data_form_sequence";

const CAMPAIGNS_API_ADD = "/campaigns/parsing/create";
const CAMPAIGNS_API_EDIT = "/campaigns/parsing/edit";

export default {
  components: {
    [Progress.name]: Progress,
    [Button.name]: Button,
    [Input.name]: Input,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect,
    [Slider.name]: Slider
  },
  data() {
    return {
      action_type: 'create',
      path: CAMPAIGNS_API_ADD + CURRENT_PATH,

      action: 'Next',

      next_step: '/campaign_data_form_accounts', // expected default value
      previous_step: '/campaign_data_form_leads', // expected default value

      /* All lists that we need to select */
      list_data: {
      },

      /* Object data */
      campaign_data: {
        data: {
            search_url: '',
            total_pages: 100,
            interval_pages: 20,
        },
      }
    };
  },
  methods: {
    progress_format(percentage) {
      return '2 / 4'
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
