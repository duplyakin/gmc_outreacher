<template>
  <div>
    <div class="form-inline align-items-start">
      <div class="align-self-start">
        <el-button @click="goto_previous_step" type="info" plain icon="el-icon-back" style="font-size: 40px; border: none;"></el-button>
      </div>
      <div class="align-self-center ml-3">
        <p style="font-size: 26px; line-height: 65px; font-weight: bold; color: #262a79;">Create Sequence</p>
      </div>
      <div class="align-self-start ml-auto">
        <el-button @click="goto_next_step" type="primary" style="font-size: 26px; border: none;">{{action}}</el-button>
      </div>
    </div>

    <div class="mb-5">
      <el-progress :percentage="50" :format="progress_format"></el-progress>
    </div>

    <div v-for="(template, index) in campaign_data.templates.email" :key="index" class="row justify-content-md-center">
      <card class="shadow p-3 mb-5 bg-white rounded col-10">
        <div class="form-inline align-items-start">
          <div class="mr-2">
            <i class="el-icon-message" style="font-size: 28px; color: #262a79;"></i>
          </div>
          <div class="mr-3">
            <p class="o24_text">Send email</p>
          </div>
          <div class="mr-3" v-if="index !== 0">
              <el-input-number v-model="template.interval" controls-position="right" size="mini" :min="1" :max="366"></el-input-number>
          </div>
          <div class="mr-auto" v-if="index !== 0">
            <p class="o24_text">days from previous step.</p>
          </div>
          <div class="ml-auto" v-if="index !== 0">
            <el-button size="small" icon="el-icon-close" style="border: none;" @click="remove_template(index)"></el-button>
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
                v-model="template.subject">
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
    </div>
    

    <div class="row justify-content-md-center">
      <p class="o24_new_step">Add New Touch:</p>
    </div>
    <div class="row justify-content-md-center mb-5" style="height: 80px;" @click="add_template">
      <el-button class="w-25 p-3 mh-100" type="info" style="font-size: 20px;" plain>Email</el-button>
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

import utils from "@/utils/campaign_utils";

import Editor from "@tinymce/tinymce-vue";

const CURRENT_PATH = "/campaign_form_sequence";

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
      action_type: 'create',
      path: CAMPAIGNS_API_ADD + CURRENT_PATH,

      action: 'Next',

      next_step: '/campaign_form_accounts', // expected default value
      previous_step: '/campaign_form_leads', // expected default value

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

      /* All lists that we need to select */
      list_data: {
      },

      /*Object data*/
      campaign_data: {
        templates: {
          email: [],
          linkedin: []
        },
      },
    };
  },
  methods: {
    progress_format(percentage) {
      return '2 / 4'
    },
    add_template() {
      let new_template = {
        interval: 1,
        subject: '',
        body: ''
      }
      this.$set(this.campaign_data.templates.email, this.campaign_data.templates.email.length, new_template)
    },
    remove_template(index) {
      if(index !== 0) {
        this.campaign_data.templates.email.splice(index, 1)
      }
    },

    async goto_next_step() {
      let next_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!next_step.hasOwnProperty('path') || !next_step.path) {
        next_step.path = this.next_step
      }
      if(next_step.hasOwnProperty('error') && next_step.error) {
        Notification.error({ title: "Error", message: next_step.error })
      }
      this.$router.push({ path: next_step.path, query: { action_type: this.action_type } })
    },

    async goto_previous_step() {
      let previous_step = await utils.load_previous_step(this.path, this.campaign_data)
      if(!previous_step.hasOwnProperty('path') || !previous_step.path) {
        previous_step.path = this.previous_step
      }
      if(previous_step.hasOwnProperty('error') && previous_step.error) {
        Notification.error({ title: "Error", message: previous_step.error })
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

    if(result.hasOwnProperty('list_data') && result.list_data) {
      this.$set(this, 'list_data', result.list_data)
    }
    if(result.hasOwnProperty('campaign_data') && result.campaign_data) {
      this.$set(this, 'campaign_data', result.campaign_data)
    }
    if(result.hasOwnProperty('action') && result.action) {
      this.$set(this, 'action', result.action)
    }
    if(result.hasOwnProperty('error') && result.error) {
      Notification.error({ title: "Error", message: result.error })
    }
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
