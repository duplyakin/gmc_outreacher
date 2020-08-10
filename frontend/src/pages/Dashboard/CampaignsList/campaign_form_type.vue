<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="$router.push('/campaign_form_start')" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Choose Campaign type</p>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="5" :format="progress_format"></el-progress>
    </div>

    <p class="text-center" style="font-size: 32px; line-height: 65px; font-weight: bold; color: #262a79;">What type of campaign do you want to create?</p>

    <div class="card-deck justify-content-md-center">
      <a @click="goto_next_step('outreach_email')">
        <div class="card mr-3 mb-3" style="width: 18rem; height: 11rem;">
          <div class="card-body text-center mx-4 my-4">
            <p class="card-text o24_card_title">Email outreach</p>
            <p class="card-text o24_card_text">Create sequence of emails to contact prospects</p>
          </div>
        </div>
      </a>

      <a @click="goto_next_step('outreach_email_linkedin')">
        <div class="card mr-3 mb-3" style="width: 18rem; height: 11rem;">
          <div class="card-body text-center mx-4 my-4">
            <p class="card-text o24_card_title">Email + LinkedIn outreach</p>
            <p class="card-text o24_card_text" style="color: red;">Comming soom</p>
          </div>
        </div>
      </a>
    </div>

  </div>
</template>
<script>
import {
  Notification,
  Select,
  Option,
  Input,
  Button,
  Progress,
} from "element-ui";

import axios from "@/api/axios-auth";

const CAMPAIGNS_API_ADD = "/campaigns/create";

export default {
  components: {
    [Progress.name]: Progress,
    [Button.name]: Button,
    [Input.name]: Input,
    [Select.name]: Select,
    [Option.name]: Option,
  },
  data() {
    return {
      action_type: 'create',
      next_step: '/campaign_form_leads', // expected default value
    };
  },
  methods: {
    progress_format(percentage) {
      return '0 / 4'
    },
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
          if (r.hasOwnProperty('error') && r.error !== 0) {
            var msg = "Error loading data " + r.msg + " Error:" + r.error
            Notification.error({ title: "Error", message: msg })
          } else {
            if (r.hasOwnProperty('next_step')) {
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
.o24_text {
    color: #262a79;
    font-size: 20px;
}
.o24_card_text {
    color: #262a79;
    font-size: 14px;
}
.o24_card_title {
    color: #262a79;
    font-size: 20px;
    font-weight: bold;
}
</style>
