<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="$router.push('/campaign_form_leads')" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Create Sequence</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="$router.push('/campaign_form_settings')" type="primary" style="font-size: 26px; border: none;">Next</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="60" :format="progress_format"></el-progress>
    </div>

    <card class="shadow p-3 mb-5 bg-white rounded">
      <div class="form-inline align-items-start">
        <div class="mr-2">
          <i class="el-icon-message" style="font-size: 28px; color: #262a79;"></i>
        </div>
        <div class="mr-3">
          <p class="o24_text">Send email</p>
        </div>
        <div class="mr-3">
            <el-input-number v-model="interval" controls-position="right" size="mini" @change="handleChange" :min="1" :max="366"></el-input-number>
        </div>
        <div class="mr-auto">
          <p class="o24_text">days from previous step.</p>
        </div>
        <div class="ml-auto">
          <el-button size="small" icon="el-icon-close" style="border: none;"></el-button>
        </div>
      </div>

      <hr class="my-1">

      <div class="row mt-3">        
        <div class="col-12 mb-4"> 
          <label>Subject</label>
          <el-input label="Subject"
              class="o24_input"
              placeholder="Enter Subject"
              name="Subject"
              v-model="subject">
          </el-input>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <label>Message</label>
          <fg-input>
            <editor
              name="body text"
              output-format="html"
              v-model="template.body"
              api-key="o5wuoncsvrewlx7zeflsjb4wo2a252lvnrnlslv30ohh31ex"
              :init="editorSettings"
            />
          </fg-input>
        </div>
      </div>
    </card>
    

    <div class="row justify-content-md-center">
      <p class="o24_new_step">Add New Touch:</p>
    </div>
    <div class="row justify-content-md-center mb-5" style="height: 80px;">
      <el-button class="w-25 p-3 mh-100" type="info" style="font-size: 20px;" plain>Email</el-button>
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
          "insertdatetime media table paste code help wordcount autoresize emoticons template"
        ],
        toolbar:
          "undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help \
           image | link | autolink | emoticons | template",
        templates: [
          {title: 'first name', description: '', content: '{{first_name}}'},
          {title: 'last name', description: '', content: '{{last_name}}'},
        ]
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
.o24_new_step {
    color: #dcdce6;
    letter-spacing: 1px;
    font-size: 26px;
    line-height: 80px;
}

</style>
