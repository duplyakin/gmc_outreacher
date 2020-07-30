<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="$router.push('/campaign_data_form_sn_leads')" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Add Leads from LinkedIn URL</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="$router.push('/campaign_data_form_sn_settings')" type="primary" style="font-size: 26px; border: none;">Next</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="60" :format="progress_format"></el-progress>
    </div>

    <div class="row justify-content-md-center mb-3">
      <div class="col-8">
        <label class="o24_text">Paste here your LinkedIn URL</label>
        <el-input
          placeholder="LinkedIn Sales Navigator search URL"
          v-model="campaign_data.title"
        ></el-input>
      </div>
    </div>

    <div class="row justify-content-md-center mb-3">
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
    [TimeSelect.name]: TimeSelect,
    [Slider.name]: Slider
  },
  data() {
    return {
      action_type: "",
      campaign_id: "",
      
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
    progress_format(percentage) {
      return '2 / 3';
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
