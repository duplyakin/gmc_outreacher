<template>
  <div>
    <h5 class="text-center">Select account and prospects</h5>
    <div class="row">
      <div class="col-6">
        <fg-input label="Choose account" :error="getError('Choose account')">
          <el-select
            class="select-primary"
            name="Choose account"
            size="large"
            placeholder="Select account"
            v-model="accountsList.simple"
            v-validate="modelValidations.account"
          >
            <el-option
              v-for="acc in accountsList"
              class="select-primary"
              :value="acc.value"
              :label="acc.label"
              :key="acc.label"
            ></el-option>
          </el-select>
        </fg-input>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <fg-input label="Choose prospects list" :error="getError('Choose prospects list')">
          <el-select
            class="select-primary"
            name="Choose prospects list"
            size="large"
            placeholder="Select prospects list"
            v-model="prospectsLists.simple"
            v-validate="modelValidations.prospect"
          >
            <el-option
              v-for="prospect in prospectsLists"
              class="select-primary"
              :value="prospect.value"
              :label="prospect.label"
              :key="prospect.label"
            ></el-option>
          </el-select>
        </fg-input>
      </div>
    </div>
  </div>
</template>
<script>
import { Slider, Tag, Input, Button, Select, Option } from "element-ui";
import accounts from "../dummy_accs";
import prospects from "../dummy_prosp";
import {
  Progress as LProgress,
  Switch as LSwitch,
  Radio as LRadio,
  Checkbox as LCheckbox,
  FormGroupInput as FgInput
} from "src/components/index";
export default {
  components: {
    [Slider.name]: Slider,
    [Tag.name]: Tag,
    [Input.name]: Input,
    [Button.name]: Button,
    [Option.name]: Option,
    [Select.name]: Select,
    LSwitch
  },
  data() {
    return {
      accountsList: accounts,
      prospectsLists: prospects,
      model: {
        campaignName: "",
        email: ""
      },
      modelValidations: {
        account: {
          required: true,
        },
        prospect: {
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
        this.$emit("step-validated", 1, res, this.model);
        return res;
      });
    }
  }
};
</script>
<style>
</style>
