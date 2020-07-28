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
      <a href="/campaign_form_leads">
        <div class="card mr-3 mb-3" >
          <div class="card-body text-center mx-4 my-4">
            <p class="card-text o24_card_title">Email outreach</p>
            <p class="card-text o24_card_text">Create sequence of emails to contact prospects</p>
          </div>
        </div>
      </a>

      <a href="">
        <div class="card mr-3 mb-3" >
          <div class="card-body text-center mx-4 my-4">
            <p class="card-text o24_card_title">Email + LinkedIn outreach</p>
            <p class="card-text o24_card_text" style="color: red;">Comming soom</p>
          </div>
        </div>
      </a>
    </div>


    <modals-container />
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

const CAMPAIGNS_API_GET = "/campaigns/get";
const CAMPAIGNS_API_DATA = "/campaigns/data";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

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

    };
  },
  methods: {
    progress_format(percentage) {
      return '0 / 3';
    }
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
