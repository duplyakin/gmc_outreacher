<template>
  <div>
    <card title="Message create">
      <form @submit.prevent="submitMessageData">
        <card>
          <div class="col-12">
            <fg-input label="Subject" :error="getError('Subject')">
              <textarea
                class="form-control"
                placeholder="Enter Subject"
                rows="1"
                name="Subject"
                v-model="message_data.subject"
                v-validate="modelValidations.message_data.subject"
              ></textarea>
            </fg-input>
            <fg-input :error="getError('body text')">
              <editor
                name="body text"
                v-model="message_data.body"
                v-validate="modelValidations.message_data.body"
                api-key="no-api-key"
                :init="{
         height: 200,
         menubar: false,
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | formatselect | bold italic backcolor | \
           alignleft aligncenter alignright alignjustify | \
           bullist numlist outdent indent | removeformat | help'
       }"
              />
            </fg-input>
          </div>
          <div class="col-3">
            <fg-input label="Interval">
              <el-input-number
                v-model="message_data.interval"
                placeholder="ex: 1.00"
                name="interval"
              ></el-input-number>
            </fg-input>
          </div>
        </card>
        <div class="row">
          <div class="col-12 d-flex flex-row-reverse">
            <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Save</button>
            <button v-on:click="discardEdit" type="button" class="btn btn-outline btn-wd btn-danger">Discard</button>
          </div>
        </div>
      </form>
    </card>
  </div>
</template>

<script>
import { Select, Option } from "element-ui";
import axios from "axios";
import Editor from "@tinymce/tinymce-vue";
var fs = require('fs');

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    editor: Editor
  },
  name: "prospect-edit",
  props: {
    messageObj: Object,
    valueUpdated: Function,
  },
  data() {
    return {
      object_before_changes: null,
      message_data: {
        subject: "",
        body: "",
        interval: ""
      },
      filters: {
        campaings: "",
        lists: ""
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
    validate() {
      return this.$validator.validateAll().then(res => {
        this.$emit("step-2-validated", res, this.model);
        return res;
      });
    },
    submitMessageData() {
        if (confirm("Are you sure?")) {
          var messageData = new FormData();
          messageData.append("message", JSON.stringify(this.message_data));

          //fs.appendFile('msg.js', messageData, function (err) {
            //if (err) throw err;
          //});
          this.$set(messageData);
          this.$emit('close');
          this.valueUpdated(messageData);
        }
    },
    submitMessageData_2() {
      const path = "http://127.0.0.1:5000/prospects/edit";
      if (confirm("Are you sure?")) {
        var prospectData = new FormData();
        prospectData.append("_prospect", JSON.stringify(this.prospect_data));

        axios
          .post(path, prospectData)
          .then(res => {
            var result = res.data;
            if (result.code > 0) {
              var updated_prospect = JSON.parse(result.updated);
              this.$emit("close");
              this.valueUpdated(updated_prospect);
            } else {
              var msg = result.msg;
              alert(msg);
            }
          })
          .catch(error => {
            alert(error);
          });
      }
    },
    discardEdit() {
      this.$emit("close");
    }
  },
  mounted() {
    this.message_data = JSON.parse(JSON.stringify(this.messageObj));
  }
};
</script>
<style>
label {
  color: black;
}
</style>
  