<template>
  <div>
    <b-container fluid class="mb-5">
      <b-row class="no-gutters">
        <b-col cols="3" md="auto">
          <b-button @click="$router.push('/campaign_form_start')">
            <b-icon icon="arrow-left"></b-icon>
          </b-button>
        </b-col>
        <b-col cols="6" md="auto">
          <h4 class="ml-3">Choose Campaign type</h4>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row align-h="center" class="justify-content-md-center">

        <h2>What type of campaign do you want to create?</h2>

        <b-card-group class="mt-3">
          <a @click="goto_next_step('outreach_email')">
            <b-card class="mr-3 mb-3">
              <b-card-body class="text-center mx-4">
                <b-card-text>Email outreach</b-card-text>
                <b-card-text>Create sequence of emails to contact prospects</b-card-text>
              </b-card-body>
            </b-card>
          </a>

          <a @click="goto_next_step('outreach_email_linkedin')">
            <b-card class="mr-3 mb-3">
              <b-card-body class="text-center mx-4">
                <b-card-text>Email + LinkedIn outreach</b-card-text>
                <b-card-text style="color: red;">Comming soon</b-card-text>
              </b-card-body>
            </b-card>
          </a>
        </b-card-group>

      </b-row>
    </b-container>

  </div>
</template>
<script>
import axios from "@/api/axios-auth";

const CAMPAIGNS_API_ADD = "/campaigns/create";

export default {
  components: {

  },
  data() {
    return {
      action_type: 'create',
      next_step: '/campaign_form_leads', // expected default value
    };
  },
  methods: {
    async goto_next_step(campaign_type) {
      await this.load_next_step(campaign_type)
      this.$router.push({ path: this.next_step, query: { action_type: this.action_type } })
    },
    async load_next_step(campaign_type) {
      var path = CAMPAIGNS_API_ADD
      var data = new FormData()
      data.append("action", "create")
      data.append("campaign_type", campaign_type)

      axios
        .post(path, data)
        .then(res => {
          var r = res.data
          if (Object.prototype.hasOwnProperty.call(r, 'error') && r.error !== 0) {
            var msg = "Error loading data " + r.msg + " Error:" + r.error
            Notification.error({ title: "Error", message: msg })
          } else {
            if (Object.prototype.hasOwnProperty.call(r, 'next_step')) {
              this.next_step = r.next_step
            } else {
              Notification.error({ title: "Error", message: 'Server error: no next step' })
            }
          }
        })
        .catch(error => {
          var msg = "Error loading data. ERROR: " + error
          Notification.error({ title: "Error", message: msg })
        });
    },
  },
  async mounted() {
  }
};
</script>
<style lang="scss">

</style>
