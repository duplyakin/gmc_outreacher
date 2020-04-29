<template>
  <div>
    <h5 class="text-center">Let's create campaign!</h5>
    <div class="row">
      <div class="col-6">
        <fg-input
          label="Campaign name"
          name="Campaign name"
          v-validate="modelValidations.campaignName"
          v-model="model.campaignName"
          :error="getError('Campaign name')"
          placeholder="ex: My email campaign"
        ></fg-input>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <fg-input label="Campaign type" :error="getError('Campaign type')">
          <el-select
            class="select-primary"
            name="Campaign type"
            size="large"
            placeholder="Select campaign type"
            v-model="selects.simple"
            v-validate="modelValidations.campaignType"
          >
            <el-option
              v-for="option in selects.types"
              class="select-primary"
              :value="option.value"
              :label="option.label"
              :key="option.label"
            ></el-option>
          </el-select>
        </fg-input>
      </div>
    </div>
  </div>
</template>
<script>
import { Input, Button, Select, Option } from "element-ui";
import {
  Progress as LProgress,
  Switch as LSwitch,
  Radio as LRadio,
  Checkbox as LCheckbox,
  FormGroupInput as FgInput
} from "src/components/index";

export default {
  props: {
    campaign: {
        name: String,
        funnel: String,
    },
  },
  components: {
    [Input.name]: Input,
    [Button.name]: Button,
    [Option.name]: Option,
    [Select.name]: Select,
    LSwitch
  },
  data() {
    return {
      model: {
        campaignName: '',
        campaignType: '',
      },
      selects: {
        //simple: this.campaign.funnel,
        simple: '',
        types: [
          { value: "Email campaign", label: "Email campaign" },
          { value: "LinkedIn campaign", label: "LinkedIn campaign" },
          { value: "Email & LinkedIn campaign", label: "Email & LinkedIn campaign" }
        ],
        multiple: "ARS"
      },
      //campaignName: this.campaign.name,
      //campaignType: this.campaign.funnel,
      modelValidations: {
        campaignName: {
          required: true,
          min: 5
        },
        campaignType: {
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
        if(res) {
          this.model.campaignType = this.selects.simple;
          this.$emit('on-validated', 'step_0', res, this.model);
        };
        return res;
      });
    }
  },
  mounted() {
    this.$nextTick(function () {
      //console.log("zero step campaign: ", this.campaign);
      this.model.campaignName = this.campaign.name;
      this.selects.simple = this.campaign.funnel;
      //console.log("zero step campaignName: ", this.campaignName);
    })
  }
};
</script>
<style>
</style>
