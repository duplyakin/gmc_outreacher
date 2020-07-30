<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="$router.push('/campaign_form_type')" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Choose leads</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="$router.push('/campaign_form_sequence')" type="primary" style="font-size: 26px; border: none;">Next</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="30" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center">
      <div class="col-8">
        <label class="o24_text">Select leads list or <a href="/campaign_data_form_type" style="color: #409EFF;">create new</a></label>
        <el-select
          class="select-default mb-3"
          style="width: 100%;"
          placeholder="Select leads list"
          v-model="campaign_data.list_selected"
          value-key="title"
        >
          <el-option
            class="select-default"
            v-for="(list,index) in list_data.lists"
            :key="list._id.$oid"
            :label="list.title"
            :value="list"
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
      action_type: "",
      campaign_id: "",

      /* All lists that we need to select */
      list_data: {
        credentials: [],
        lists: [],
        funnels: [],
        columns: []
      },

      /*Object data*/
      campaign_data: {
        campaign_type: 0,
        list_selected: "",
        title: "",
        funnel: {},
        credentials: [],
        templates: {
          email: [],
          linkedin: []
        },

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
      return '1 / 3';
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
</style>
