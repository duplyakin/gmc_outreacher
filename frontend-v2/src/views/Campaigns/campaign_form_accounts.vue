<template>
  <div>
    <b-container fluid class="mb-5">
      <b-row class="no-gutters">
        <b-col cols="3" md="auto">
          <b-button @click="goto_previous_step">
            <b-icon icon="arrow-left"></b-icon>
          </b-button>
        </b-col>
        <b-col cols="6" md="auto">
          <h4 class="ml-3">Choose account</h4>
        </b-col>
        <b-col cols="3" class="ml-auto" md="auto">
          <b-button @click="goto_next_step">
            {{action}}
          </b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-container fluid class="mb-5">
      <b-row>
        <b-col cols="12">
          <b-progress :value="3" :max="4"></b-progress>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row align-h="center">
        <b-col cols="9">
          <label>Choose Email account or <a href="/accounts">add new</a></label>
          <b-form-select v-model="email_account_selected" :options="list_data.credentials" @change="onChangeEmailCredentials"></b-form-select>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import utils from "./CampaignController";

const CURRENT_PATH = "/campaign_form_accounts";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
  },
 data() {
    return {
      action_type: 'create',
      path: CAMPAIGNS_API_ADD + CURRENT_PATH,

      action: 'Next',

      next_step: '/campaign_form_settings', // expected default value
      previous_step: '/campaign_form_sequence', // expected default value

     /* All defaults that you store on client */
      email_account_selected: "",

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
    onChangeEmailCredentials(new_credentials) {
      return this.onChangeCredentials("email", new_credentials)
    },
    onChangeCredentials(medium, new_credentials) {
       if (this.campaign_data.credentials.length <= 0) {
        this.campaign_data.credentials.push(new_credentials)
        return
      } else {
        let _medium = medium
        var index = this.findIndex(this.campaign_data.credentials, function(el) {
          return el.medium == _medium
        })
        if (index >= 0) {
          this.campaign_data.credentials.splice(index, 1, new_credentials)
        } else {
          // Should never happened
          this.campaign_data.credentials.push(new_credentials)
        }
        return
      } 
    },
    findIndex(credentials, medium){
      // remove it ! (use lodash ?)
      return {credentials, medium}
    },

    async goto_next_step() {
      let next_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!Object.prototype.hasOwnProperty.call(next_step, 'path') || !next_step.path) {
        next_step.path = this.next_step
      }
      if(Object.prototype.hasOwnProperty.call(next_step, 'error') && next_step.error) {
        //Notification.error({ title: "Error", message: next_step.error })
      }
      this.$router.push({ path: next_step.path, query: { action_type: this.action_type } })
    },

    async goto_previous_step() {
      let previous_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!Object.prototype.hasOwnProperty.call(previous_step, 'path') || !previous_step.path) {
        previous_step.path = this.previous_step
      }
      if(Object.prototype.hasOwnProperty.call(previous_step, 'error') && previous_step.error) {
        //Notification.error({ title: "Error", message: previous_step.error })
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

    if(Object.prototype.hasOwnProperty.call(result, 'list_data') && result.list_data) {
      this.$set(this, 'list_data', result.list_data)
    }
    if(Object.prototype.hasOwnProperty.call(result, 'campaign_data') && result.campaign_data) {
      this.$set(this, 'campaign_data', result.campaign_data)
    }
    if(Object.prototype.hasOwnProperty.call(result, 'action') && result.action) {
      this.$set(this, 'action', result.action)
    }
    if(Object.prototype.hasOwnProperty.call(result, 'error') && result.error) {
      //Notification.error({ title: "Error", message: result.error })
    }
  }
};
</script>
<style lang="scss">

</style>
