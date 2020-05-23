<template>
  <div class="test-modal">
    <card title="Message create">
      <form v-if="template" @submit.prevent="submitData">
        <card v-if="template_type === 'email'">
          <div class="col-12">
            <fg-input label="Subject" :error="getError('Subject')">
              <textarea
                class="form-control"
                placeholder="Enter Subject"
                rows="1"
                name="Subject"
                v-model="template.subject"
                v-validate="modelValidations.subject"
              ></textarea>
            </fg-input>
            <fg-input :error="getError('body text')">
              <editor
                name="body text"
                output-format="html"
                v-model="template.body"
                api-key="o5wuoncsvrewlx7zeflsjb4wo2a252lvnrnlslv30ohh31ex"
                :init="editorSettings"
              />
            </fg-input>
          </div>
          <div class="container">
            <p
              class="interval_text"
            >If no reply is received for previous email, this email will be sent after</p>
            <div class="col-2">
              <fg-input label>
                <el-input-number v-model="interval" placeholder="ex: 1.00" :min="1" :max="365"></el-input-number>
              </fg-input>
            </div>
            <p class="interval_text">day(s) from previous email</p>
          </div>
        </card>

        <card v-if="template_type === 'linkedin'">
          <div class="col-12">
            <fg-input :error="getError('body text')">
              <editor
                name="body text"
                output-format="html"
                v-model="template.message"
                api-key="o5wuoncsvrewlx7zeflsjb4wo2a252lvnrnlslv30ohh31ex"
                :init="editorSettings"
              />
            </fg-input>
          </div>
          <div class="container">
            <p
              class="interval_text"
            >If no reply is received for previous message, this message will be sent after</p>
            <div class="col-2">
              <fg-input label>
                <el-input-number v-model="interval" placeholder="ex: 1.00" :min="1" :max="365"></el-input-number>
              </fg-input>
            </div>
            <p class="interval_text">day(s) from previous message</p>
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
    editor: Editor
  },
  props: {
    template_type: String,
    templateObj: Object,
    valueUpdated: Function
  },
  data() {
    return {
      interval: 1, // feature
      template: null,
      editorSettings: {
        height: 200,
        menubar: false,
        plugins: [
          "advlist autolink lists link image charmap print preview anchor",
          "searchreplace visualblocks code fullscreen",
          "insertdatetime media table paste code help wordcount autoresize"
        ],
        toolbar:
          "undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help \
           image | link | autolink"
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
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
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
      if (this.template_type == "email" && (this.template.subject == '' || this.template.body == '')) {
        Notification.error({title: "Error", message: "Subject and body can't be empty"});
        return false;
      }
      if (this.template_type == "linkedin" && this.template.message == '') {
        Notification.error({title: "Error", message: "Message can't be empty"});
        return false;
      }
      if (confirm("Are you sure?")) {
        this.$emit("close");
        this.template.interval = this.interval; // feature
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
      this.interval = this.template.interval; // feature

      /* If we create the new object we don't have properties */
      if (this.template_type === "email") {
        if (!this.template.hasOwnProperty("subject")) {
          this.template["subject"] = "";
        }
        if (!this.template.hasOwnProperty("body")) {
          this.template["body"] = "";
        }
        if (!this.template.hasOwnProperty("interval")) {
          this.template["interval"] = 1;
        }
      } else if (this.template_type === "linkedin") {
        if (!this.template.hasOwnProperty("message")) {
          this.template["message"] = "";
        }
        if (!this.template.hasOwnProperty("interval")) {
          this.template["interval"] = 1;
        }
      }
      console.log(this.template);
    }
  }
};
</script>
<style>
label {
  color: black;
}
.container {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding: 10px 20px;
}
.interval_text {
  display: flex;
  align-items: flex-start;
  font-size: 17px;
  font-weight: 100;
  line-height: 50px;
  color: rgb(119, 119, 119);
}
</style>
  