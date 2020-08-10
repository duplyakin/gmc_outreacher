<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="goto_previous_step" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Choose account</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="goto_next_step" type="primary" style="font-size: 26px; border: none;">{{action}}</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="75" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-5">
      <div class="col-8">
        <label class="o24_text">Choose LinkedIn account or <a href="/accounts" style="color: #409EFF;">add new</a></label>
        <el-select
            class="select-default mb-3"
            style="width: 100%;"
            placeholder="Select email account"
            v-model="linkedin_account_selected"
            @change="onChangeLinkedinCredentials"
            value-key="data.account">
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

import utils from "@/utils/campaign_utils";

const CURRENT_PATH = "/campaign_data_form_post_accounts";

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
      action: 'Next',

      next_step: '/campaign_data_form_post_settings', // expected default value
      previous_step: '/campaign_data_form_post_sequence', // expected default value

      /* All defaults that you store on client */
      linkedin_account_selected: "",

      /* All lists that we need to select */
      list_data: {
        credentials: [],
      },

      /* Object data */
      campaign_data: {
        credentials: [],
      }
    };
  },
  methods: {
    progress_format(percentage) {
      return '3 / 4'
    },

    onChangeLinkedinCredentials(new_credentials) {
      return this.onChangeCredentials("linkedin", new_credentials)
    },
    onChangeCredentials(medium, new_credentials) {
      if (this.campaign_data.credentials.length <= 0) {
        this.campaign_data.credentials.push(new_credentials)
        return
      } else {
        let _medium = medium
        var index = findIndex(this.campaign_data.credentials, function(el) {
          return el.medium == _medium
        })
        if (index >= 0) {
          this.campaign_data.credentials.splice(index, 1, new_credentials)
        } else {
          /* Should never happened */
          this.campaign_data.credentials.push(new_credentials)
        }
        return
      }
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
      this.$set(this, 'path', CAMPAIGNS_API_ADD + CURRENT_PATH)
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
