<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Choose leads</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="$router.push('/campaign_form_sequence')" type="primary" style="font-size: 26px; border: none;">Next</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="30"></el-progress>
    </div>

    <div class="row justify-content-md-center">
      <div class="col-8">
        <label style="color: #262a79; font-size: 20px;">Select leads list or <a href="/campaign_data_form_leads" style="color: #409EFF;">create new</a></label>
        <el-select
          class="select-default mb-3"
          style="width: 100%;"
          placeholder="Select leads list"
          v-model="campaign_data.list_selected"
          value-key="title"
          :disabled="!modified_fields['lists']"
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
  drop,
  every,
  forEach,
  some,
  get,
  isArray,
  map,
  set,
  findIndex
} from "lodash";

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

import Editor from "@tinymce/tinymce-vue";
import timezones from "./defaults/timezones";
import axios from "@/api/axios-auth";

const MessageEdit = () => import("./messageEdit.vue");

const CAMPAIGNS_API_GET = "/campaigns/get";
const CAMPAIGNS_API_DATA = "/campaigns/data";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
    editor: Editor,
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
      test: false,

      interval: 1,
      subject: '',

      template: {
        body: ''
      },
      editorSettings: {
        height: 200,
        menubar: false,
        plugins: [
          "advlist autolink lists link image charmap print preview anchor",
          "searchreplace visualblocks code fullscreen",
          "insertdatetime media table paste code help wordcount autoresize emoticons"
        ],
        toolbar:
          "undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help \
           image | link | autolink | emoticons",
      },


      action_type: "",
      campaign_id: "",

      email_account_selected: "",
      linkedin_account_selected: "",
      timezones_selected: "",

      /*All defaults that you store on client*/
      timezones_selects: timezones,
      modified_fields: {},

      email_table_columns: [
        {
          prop: "title",
          label: "Template name",
          minWidth: 300
        },
        {
          prop: "subject",
          label: "Subject",
          minWidth: 300
        },
        {
          prop: "interval",
          label: "Delay (days)",
          minWidth: 100
        }
      ],

      linkedin_table_columns: [
        {
          prop: "title",
          label: "Template name",
          minWidth: 300
        },
        {
          prop: "interval",
          label: "Delay (days)",
          minWidth: 100
        }
      ],

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
