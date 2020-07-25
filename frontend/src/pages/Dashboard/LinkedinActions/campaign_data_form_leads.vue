<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Create leads list</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="$router.push('/campaign_data_form_sequence')" type="primary" style="font-size: 26px; border: none;">Next</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="30"></el-progress>
    </div>

    <div class="row justify-content-md-center">
      <div class="col-8">
        <label style="color: #262a79; font-size: 20px;">Create new leads list name</label>
        <el-input
          :disabled="!modified_fields['title']"
          placeholder="New leads list"
          v-model="campaign_data.title"
        ></el-input>
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
} from "element-ui";

import timezones from "../CampaignsList/defaults/timezones";
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
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [TimeSelect.name]: TimeSelect
  },
  data() {
    return {
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
        list_title: '',
        data: {
            search_url: '',
            total_pages: 100,
            interval_pages: 20,
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
  },
  async mounted() {
  }
};
</script>
<style lang="scss">
.action_text {
    color: #262a79;
    //font-family: NeurialGrotesk-Medium;
    font-size: 20px;
}
.new_step {
    color: #dcdce6;
    letter-spacing: 1px;
    //font-family: NeurialGrotesk-Medium;
    font-size: 26px;
    line-height: 80px;
}
</style>
