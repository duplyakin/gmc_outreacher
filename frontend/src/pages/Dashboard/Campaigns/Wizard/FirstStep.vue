<template>
  <div>
    <div class="row">
        <div class="col-12">
          <card title="Select accounts based on medium (Linkedin or email)">
            
            <div v-if="hasMedium('email')" class="col-6">
                <p>Select email account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select email account"
                  v-model="model.account_email"
                  v-validate="modelValidations.account">
                    <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'email'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account._id.$oid">
                    </el-option>
                </el-select>  
                
            </div>
            <div v-if="hasMedium('linkedin')" class="col-6">
                <p>Select linkedin account</p>
                <el-select
                  class="select-default mb-3"
                  style="width: 100%;"
                  placeholder="Select linkedin account"
                  v-model="model.account_linkedin"
                  v-validate="modelValidations.account">
                    <el-option
                    class="select-default"
                    v-for="(account,index) in list_data.credentials"
                    v-if="account.medium == 'linkedin'"
                    :key="account._id.$oid"
                    :label="account.data.account"
                    :value="account._id.$oid">
                    </el-option>
                </el-select>  
            </div>
          </card>
        </div>
    </div>
    
    <div class="row">
          <div class="col-12">
              <card title="Select prospects list">
              <p>Select prospects list</p>
              <el-select
                class="select-default mb-3"
                style="width: 100%;"
                placeholder="Select prospects list"
                v-model="model.prospectsList">
                  <el-option
                  class="select-default"
                  v-for="(list,index) in list_data.prospect_lists"
                  :key="list._id.$oid"
                  :label="list.title"
                  :value="list._id.$oid">
                  </el-option>
              </el-select>  
            </card>
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
export default {
  props: {
    campaign: {
        funnel: Object,
        credentials: Array,
        prospectsList: String,
    },
    list_data: {
      credentials: Array,
      prospect_lists: Array,
    },
    email_data: Object,
    linkedin_data: Object,
  },
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
      model: {
        account_email: '',
        account_linkedin: '',
        prospectsList: '',
      },
      modelValidations: {
        account: {
          required: true,
        },
        prospects: {
          required: true
        }
      }
    };
  },
  methods: {
    hasMedium(medium){
    
    var templates_required = this.campaign.funnel.templates_required || null;
    if (templates_required){
        var email = templates_required.email || null;
        var linkedin = templates_required.linkedin || null;

        if (medium == 'email'){
          if (email){
            return true;
          }else{
            return false;
          }
        }

        if (medium == 'linkedin'){
          if (linkedin){
            return true;
          }else{
            return false;
          }
        }
    }

    return false;
  },
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      return this.$validator.validateAll().then(res => {
        if(res) {
          this.$emit("on-validated", 'step_1', res, this.model);
        }
        return res;
      });
    }
  },
  created() {
    let arr = this.campaign.credentials;
    if(typeof arr !== 'undefined' && arr.length > 0) {
      //TODO: check if undefined
      this.model.account_email = arr.find(x => x.medium == 'email').data.account;
      this.model.account_linkedin = arr.find(x => x.medium == 'linkedin').data.account;
    } else {
      this.model.account_email = '';
      this.model.account_linkedin = '';
    }
    this.model.prospectsList = this.campaign.prospectsList;
    //console.log('olololol: ', this.model.account_linkedin)
  }
};
</script>
<style>
</style>
