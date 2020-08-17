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
          <h4 class="ml-3">Settings</h4>
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
          <b-progress :value="4" :max="4"></b-progress>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row align-h="center">
        <b-col cols="9">
          <label>Name your campaign</label>
          <b-form-input v-model="campaign_data.title" type="text" placeholder="Сampaign name"></b-form-input>
        </b-col>
      </b-row>

      <b-row align-h="center" class="mt-3">
        <b-col cols="3" md="auto">
          <p>Shedule</p>
        </b-col>
      </b-row>

      <b-row align-h="center">
        <b-col cols="3">
          <label>Start</label>
          <b-form-timepicker v-model="campaign_data.from_hour" placeholder="Start" locale="en"></b-form-timepicker>
        </b-col>
        <b-col cols="3">
          <label>End</label>
          <b-form-timepicker v-model="campaign_data.to_hour" placeholder="End" locale="en"></b-form-timepicker>
        </b-col>
        <b-col cols="3">
          <label>Time Zone</label>
          <b-form-select v-model="campaign_data.time_zone" :options="timezones_selects" placeholder="Select Time Zone"></b-form-select>
        </b-col>
      </b-row>

      <b-row align-h="center" class="mt-3">
        <b-col cols="7" md="auto">
          <b-form-group label="Sending days">
            <b-form-checkbox-group
              v-model="campaign_data.sending_days"
              :options="days"
              buttons
            ></b-form-checkbox-group>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>

  </div>
</template>
<script>
import utils from "./CampaignController";
import timezones from "./defaults/timezones";

const CURRENT_PATH = "/campaign_form_settings";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
  },
 data() {
    return {
      action_type: 'create',
      path: CAMPAIGNS_API_ADD + CURRENT_PATH,
      action: 'Save draft',

      next_step: '/campaigns', // expected default value
      previous_step: '/campaign_form_accounts', // expected default value

      /* All defaults that you store on client */
      timezones_selects: timezones,
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],

      /* All lists that we need to select */
      list_data: {
      },

      /* Object data */
      campaign_data: {
        title: "",

        from_hour: "",
        to_hour: "",
        time_zone: "",
        sending_days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
      }
    };
  },
  methods: {
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
