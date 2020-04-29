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
                v-validate="modelValidations.subject"
              ></textarea>
            </fg-input>
            <fg-input :error="getError('body text')">
              <editor
                name="body text"
                output-format="html"
                v-model="message_data.body"
                api-key="o5wuoncsvrewlx7zeflsjb4wo2a252lvnrnlslv30ohh31ex"
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
           bullist numlist outdent indent | removeformat | help \
           image | link | autolink'
       }"
              />
            </fg-input>
          </div>
          <div class="col-3">
            <fg-input label="Interval">
              <el-input-number
                v-model="message_data.interval"
                placeholder="ex: 1.00"
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

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    editor: Editor
  },
  props: {
    messageObj: Object,
    valueUpdated: Function,
  },
  data() {
    return {
      message_data: {
        subject: '',
        body: '',
        //body_plain: '',
        //body_html: '',
        interval: ''
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
    convertToPlainText(htmlText){
      let res = htmlText.replace(/<style([\s\S]*?)<\/style>/gi, '');
      res = res.replace(/<script([\s\S]*?)<\/script>/gi, '');
      res = res.replace(/<\/div>/ig, '\n');
      res = res.replace(/<\/li>/ig, '\n');
      res = res.replace(/<li>/ig, '  *  ');
      res = res.replace(/<\/ul>/ig, '\n');
      res = res.replace(/<\/p>/ig, '\n');
      res = res.replace(/<br\s*[\/]?>/gi, "\n");
      res = res.replace(/<[^>]+>/ig, '');

      return res;
    },
    submitMessageData() {
        if (confirm("Are you sure?")) {
          // variant 1
          //this.message_data.body_plain = this.message_data.body.replace(/<(style|script|iframe)[^>]*?>[\s\S]+?<\/\1\s*>/gi,'').replace(/<[^>]+?>/g,'').replace(/\s+/g,' ').replace(/ /g,' ').replace(/>/g,' '); 
          // variant 2
          //this.message_data.body_plain = this.convertToPlainText(this.message_data.body);
          this.$emit('close');
          this.valueUpdated(this.message_data);
          console.log('TEXT: ', this.message_data);
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
  