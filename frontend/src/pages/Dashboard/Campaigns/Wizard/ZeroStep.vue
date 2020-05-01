<template>
  <div>
    <h5 class="text-center">Let's create campaign!</h5>
    <div class="row">
      <div class="col-6">
        <fg-input
          label="Campaign title"
          name="Campaign title"
          v-validate="modelValidations.campaignTitle"
          v-model="model.campaignTitle"
          :error="getError('Campaign title')"
          placeholder="ex: My email campaign"
        ></fg-input>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <fg-input label="Campaign funnel" :error="getError('Campaign funnel')">
          <el-select
                    class="select-default mb-3"
                    name="Campaign funnel"
                    v-on:change="onChangeFunnel"
                    style="width: 100%;"
                    placeholder="Select funnel"
                    v-model="model.funnel_selected"
                    v-validate="modelValidations.campaignFunnel"
                    value-key="title">
                      <el-option
                      class="select-default"
                      v-for="(funnel,index) in list_data.funnels"
                      :key="funnel._id.$oid"
                      :label="funnel.title"
                      :value="funnel">
                      </el-option>
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
    campaign: Object,
    list_data: Object,
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
        campaignTitle: '',
        funnel_selected: {},
        email_templates: [],
        linkedin_templates: [],
      },

      modelValidations: {
        campaignTitle: {
          required: true,
          min: 5
        },
        campaignFunnel: {
          required: true
        }
      }
    };
  },
  methods: {
    onChangeFunnel(){
      /* update tempaltes based on selected funnel */
            
      var templates_required = this.model.funnel_selected.templates_required || null;
      if (templates_required){
        
        var email = templates_required.email || null;
        if (email){
          this.model.email_templates = Object.values(email);

          /*sort by order field*/
          this.model.email_templates.sort(function(first, second) {
            return first['order'] - second['order'];
          });
        }

        var linkedin = templates_required.linkedin || null;
        if (linkedin){
          this.model.linkedin_templates = Object.values(linkedin);
          
          /*sort by order field*/
          this.model.linkedin_templates.sort(function(first, second) {
            return first['order'] - second['order'];
          });

        }
      }

      console.log("new onchangefunnel");
      console.log(this.funnel_selected);
      console.log(this.model.email_templates);
      console.log(this.model.linkedin_templates);

    },
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      return this.$validator.validateAll().then(res => {
        if(res) {
          this.$emit('on-validated', 'step_0', res, this.model);
        };
        return res;
      });
    }
  },
  created() {
      this.model.campaignTitle = this.campaign.title;
      this.model.funnel_selected = this.campaign.funnel;
      //console.log('list_data: ', this.list_data);
  },
};
</script>
<style>
</style>
