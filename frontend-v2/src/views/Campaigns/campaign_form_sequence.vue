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
          <h4 class="ml-3">Create Sequence</h4>
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
          <b-progress :value="2" :max="4"></b-progress>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row align-h="center" v-for="(template, index) in campaign_data.templates.email" :key="index">
        <b-col cols="10">

          <b-card class="shadow p-3 mb-5 bg-white rounded">
            <b-row class="no-gutters">
              <b-col cols="1" md="auto">
                <b-icon icon="envelope" class="mr-2 mt-1"></b-icon>
              </b-col>
              <b-col cols="2" md="auto" class="mr-2">
                <p>Send email</p>
              </b-col>
              <b-col cols="1" v-if="index !== 0" class="mr-2">
                <b-form-input size="sm" type="number" v-model="template.interval"></b-form-input>
              </b-col>
              <b-col cols="2" md="auto">
                <p v-if="index !== 0">days from previous step.</p>
              </b-col>
              <b-col cols="1" md="auto" class="ml-auto">
                <b-icon v-if="index !== 0" icon="x" class="mt-1" @click="remove_template(index)"></b-icon>
              </b-col>
            </b-row>

            <hr class="my-1">

            <b-row class="my-4">
              <b-col>
                <label>Subject</label>
                <b-form-input v-model="template.subject" type="text" placeholder="Enter your name"></b-form-input>
              </b-col>
            </b-row>
            
            <b-row>
              <b-col>
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
              </b-col>
            </b-row>

          </b-card>
        </b-col>
      </b-row>
    </b-container>

    <b-container class="mb-5">
      <b-row align-h="center">
        <b-col md="auto" cols="4">
          <p>Add New Touch:</p>
        </b-col>
      </b-row>
      <b-row align-h="center">
        <b-col md="auto" cols="3">
          <b-button @click="add_template">Email</b-button>
        </b-col>
      </b-row>
    </b-container>

  </div>
</template>
<script>
import utils from "./CampaignController";

import Editor from "@tinymce/tinymce-vue";

const CURRENT_PATH = "/campaign_form_sequence";

const CAMPAIGNS_API_ADD = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
    editor: Editor,
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
