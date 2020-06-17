<template>
  <div class="test-modal">

    <card>
      <h4>{{template.title}}</h4>
      <form v-if="template" @submit.prevent="submitData">

        <card v-if="template_type === 'email'">

          <div class="row">
            <div class="col-12 mb-3">
              <el-input label="Subject"
                  placeholder="Enter Subject"
                  name="Subject"
                  maxlength="100"
                  show-word-limit
                  v-model="subject">
              </el-input>
            </div>
          </div>

          <div class="row">
            <div class="col-12 mb-3">
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

          <div class="container">
            <div class="row justify-content-start">
              <div class="col-8 o24_interval_text">If no reply is received for previous email, this email will be sent after (days)</div>
              <div class="col-2">
                <fg-input>
                  <el-input-number v-model="interval" placeholder="ex: 1.00" :min="1" :max="365"></el-input-number>
                </fg-input>
              </div>
            </div>
          </div>
        </card>


        <card v-if="template_type === 'linkedin'">
          <div class="row">
            <div class="col-12">
              <fg-input>
                <editor
                  name="body text"
                  output-format="html"
                  v-model="template.message"
                  api-key="o5wuoncsvrewlx7zeflsjb4wo2a252lvnrnlslv30ohh31ex"
                  :init="editorSettings"
                />
              </fg-input>
            </div>
          </div>

          <div class="container">
            <div class="row justify-content-start">
              <div class="col-8 o24_interval_text">If no reply is received for previous message, this message will be sent after (days)</div>
              <div class="col-2">
                <fg-input>
                  <el-input-number v-model="interval" placeholder="ex: 1.00" :min="1" :max="365"></el-input-number>
                </fg-input>
              </div>
            </div>
          </div>
        </card>

        <div class="row">
          <div class="col-12 d-flex flex-row-reverse">
            <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Save</button>
            <button
              v-on:click="discardEdit"
              type="button"
              class="btn btn-outline btn-wd btn-danger"
            >Discard</button>
          </div>
        </div>

      </form>
    </card>

  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";
import Editor from "@tinymce/tinymce-vue";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    editor: Editor,
  },
  props: {
    template_type: String,
    templateObj: Object,
    valueUpdated: Function
  },
  data() {
    return {
      subject: '', // element-ui feature
      interval: 1, // element-ui feature

      linkedin_max_msg_length: 1999,

      template: null,
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
      modelValidations: {
        message_data: {
          required: true
        },
        subject: {
          required: true
        }
      }
    };
  },
  methods: {
    convertToPlainText(htmlText) {
      let res = htmlText.replace(/<style([\s\S]*?)<\/style>/gi, "");
      res = res.replace(/<script([\s\S]*?)<\/script>/gi, "");
      res = res.replace(/<\/div>/gi, "\n");
      res = res.replace(/<\/li>/gi, "\n");
      res = res.replace(/<li>/gi, "  *  ");
      res = res.replace(/<\/ul>/gi, "\n");
      res = res.replace(/<\/p>/gi, "\n");
      res = res.replace(/<br\s*[\/]?>/gi, "\n");
      res = res.replace(/<[^>]+>/gi, "");

      return res;
    },
    submitData() {
      if (!this.template) {
        Notification.error({title: "Error", message: "Template can't be empty"});
        return false;
      }
      if (this.template_type == "email" && this.subject == '') {
        Notification.error({title: "Error", message: "Subject can't be empty"});
        return false;
      }
      if (this.template_type == "email" && this.template.body == '') {
        Notification.error({title: "Error", message: "Body can't be empty"});
        return false;
      }

      if (this.template_type == "linkedin" && this.template.message == '') {
        Notification.error({title: "Error", message: "Message can't be empty"});
        return false;
      } 

      if (this.template_type == "linkedin" && this.convertToPlainText(this.template.message).length > this.linkedin_max_msg_length) {
        Notification.error({title: "Error", message: "Message lengh should be shorter than " + this.linkedin_max_msg_length + " symbols."});
        return false;
      } 

      if (confirm("Are you sure?")) {
        this.$emit("close");
        this.template.interval = this.interval; // element-ui feature
        this.template.subject = this.subject; // element-ui feature
        this.valueUpdated(this.template);
        console.log("template: ", this.template);
      }
    },
    discardEdit() {
      this.$emit("close");
    }
  },
  created() {
    if (Object.keys(this.templateObj).length != 0) {
      this.template = JSON.parse(JSON.stringify(this.templateObj));

      /* If we create the new object we don't have properties */
      if (this.template_type === "email") {
        if (!this.template.hasOwnProperty("subject")) {
          this.template["subject"] = "";
        } else {
          this.subject = this.template.subject; // element-ui feature
        }
        if (!this.template.hasOwnProperty("body")) {
          this.template["body"] = "";
        }
        if (!this.template.hasOwnProperty("interval")) {
          this.template["interval"] = 1;
        } else {
          this.interval = this.template.interval; // element-ui feature
        }

      } else if (this.template_type === "linkedin") {
        if (!this.template.hasOwnProperty("message")) {
          this.template["message"] = "";
        }
        if (!this.template.hasOwnProperty("interval")) {
          this.template["interval"] = 1;
        } else {
          this.interval = this.template.interval; // element-ui feature
        }
      }
      console.log(this.template);
    }
  }
};
</script>
<style>
.o24_interval_text {
  display: flex;
  align-items: flex-start;
  font-size: 17px;
  font-weight: 100;
  line-height: 50px;
  color: rgb(119, 119, 119);
}
</style>
  