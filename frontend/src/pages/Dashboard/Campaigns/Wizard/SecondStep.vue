<template>
  <div>
    <h5 class="text-center">Message generation</h5>
    <div class="row">
      <h5 class="text-center">Day 1: Opening</h5>
      <div class="col-12">
        <fg-input label="Subject" :error="getError('Subject')">
          <textarea class="form-control" placeholder="Enter Subject" rows="1" name="Subject" v-validate="modelValidations.subject"></textarea>
        </fg-input>
        <fg-input :error="getError('opening text')">
          <editor
            name="opening text"
            v-model="openingText"
            v-validate="modelValidations.openingText"
            api-key="no-api-key"
            :init="{
         height: 100,
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
    </div>
    <div class="row">
      <h5 class="text-center">Day 2: Follow up 1</h5>
      <div class="col-12">
        <fg-input label="Subject">
          <textarea class="form-control" placeholder="Enter Subject" rows="1"></textarea>
        </fg-input>
        <fg-input>
          <editor
            api-key="no-api-key"
            :init="{
         height: 100,
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
    </div>
    <div class="row">
      <h5 class="text-center">Day 3: Follow up 2</h5>
      <div class="col-12">
        <fg-input label="Subject">
          <textarea class="form-control" placeholder="Enter Subject" rows="1"></textarea>
        </fg-input>
        <fg-input>
          <editor
            api-key="no-api-key"
            :init="{
         height: 100,
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
    </div>
  </div>
</template>

<script>
import { Slider, Tag, Input, Button, Select, Option } from "element-ui";
import {
  Progress as LProgress,
  Switch as LSwitch,
  Radio as LRadio,
  Checkbox as LCheckbox,
  FormGroupInput as FgInput
} from "src/components/index";
import Editor from "@tinymce/tinymce-vue";

export default {
  components: {
    [Slider.name]: Slider,
    [Tag.name]: Tag,
    [Input.name]: Input,
    [Button.name]: Button,
    [Option.name]: Option,
    [Select.name]: Select,
    LSwitch,
    editor: Editor
  },
  data() {
    return {
      openingText: "",
      subject: "",
      model: {
        openingText: "",
        followText: "",
        subject: "",
      },
      modelValidations: {
        openingText: {
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
    }
  }
};
</script>
<style>
</style>
