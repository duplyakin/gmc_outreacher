<template>
  <div>
    <div class="row d-flex justify-content-center">
      <div class="col-12">
        <div class="card card-wizard" id="wizardCard">
          <form-wizard
            shape="tab"
            @on-complete="wizardComplete"
            error-color="#FB404B"
            color="#35495E"
          >
            <tab-content
              title="Step 0"
              class="col-12"
              :before-change="() => validateStep('zeroStep')"
              icon="nc-icon nc-badge"
            >
              <zero-step ref="zeroStep" :campaign="campaign" :list_data="list_data" :email_data="email_data" :linkedin_data="linkedin_data" @on-validated="onStepValidated"></zero-step>
            </tab-content>

            <tab-content
              title="Step 1"
              class="col-12"
              :before-change="() => validateStep('firstStep')"
              icon="nc-icon nc-badge"
            >
              <first-step ref="firstStep" :campaign="campaign" :list_data="list_data" :email_data="email_data" :linkedin_data="linkedin_data" @on-validated="onStepValidated"></first-step>
            </tab-content>

            <tab-content
              title="Step 2"
              class="col-12"
              :before-change="() => validateStep('secondStep')"
              icon="nc-icon nc-notes"
            >
              <second-step ref="secondStep" :campaign="campaign" :email_data="email_data" :linkedin_data="linkedin_data" @on-validated="onStepValidated"></second-step>
            </tab-content>


            <tab-content
              title="Step 3"
              class="col-12"
              :before-change="() => validateStep('thirdStep')"
              icon="nc-icon nc-notes"
            >
              <third-step ref="thirdStep" :campaign="campaign" @on-validated="onStepValidated"></third-step>
            </tab-content>

            <tab-content
              title="Preview"
              class="col-12"
              :before-change="() => validateStep('lastStep')"
              icon="nc-icon nc-check-2"
            >
              <last-step ref="lastStep" :campaign="campaign" :email_data="email_data" :linkedin_data="linkedin_data" @on-validated="onStepValidated"></last-step>
            </tab-content>

            <button slot="prev" class="btn btn-default btn-fill btn-wd btn-back">Back</button>
            <button slot="next" class="btn btn-default btn-fill btn-wd btn-next">Next</button>
            <button slot="finish" class="btn btn-success btn-fill btn-wd">Finish</button>
          </form-wizard>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { FormWizard, TabContent } from "vue-form-wizard";
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import ZeroStep from "./Wizard/ZeroStep.vue";
import FirstStep from "./Wizard/FirstStep.vue";
import SecondStep from "./Wizard/SecondStep.vue";
import ThirdStep from "./Wizard/ThirdStep.vue";
import LastStep from "./Wizard/LastStep.vue";
import swal from "sweetalert2";
import axios from 'axios'

const CAMPAIGNS_API_LIST = 'http://127.0.0.1:5000/campaigns';
const CAMPAIGNS_API_CREATE = 'http://127.0.0.1:5000/campaigns/create';


export default {
  data() {
    return {
      response_json : '',
      request_json: '',

      campaign: {},

      wizardModel: {
        stepsData: {}
      },

      list_data : {
            //campaigns : [],
            credentials: [],
            prospect_lists : [],
            funnels : [],
            columns : [],

            pagination : {
                perPage : 0,
                currentPage : 1,
                total : 0
          }
        },

        email_data : {
          email_account_selected: '',
          templates: [],
          table_columns: [
              {
                prop: 'title',
                label: 'Template title',
                minWidth: 300
              },
              {
                prop: 'subject',
                label: 'Subject',
                minWidth: 300
              },
              {
                prop: 'interval',
                label: 'Interval',
                minWidth: 100
              }
          ]
        },

        linkedin_data : {
          linkedin_account_selected: '',
          templates: [],
          table_columns: [
             {
                prop: 'title',
                label: 'Template title',
                minWidth: 300
              },
              {
                prop: 'interval',
                label: 'Interval',
                minWidth: 100
              }
          ],
        },

    };
  },
  components: {
    FormWizard,
    TabContent,
    ZeroStep,
    FirstStep,
    SecondStep,
    ThirdStep,
    LastStep
  },
  methods: {
    initCampaign(){
        let id = this.$route.query.id;
        //console.log('id: ', id);
        let type = this.$route.query.type;
        //console.log('type: ', type);

        if(type == 'edit'){
          // TODO: editing, test this shit
          this.get_campaign_by_id();
          this.email_data.templates = this.campaign.templates.email;
          this.linkedin_data.templates = this.campaign.templates.linkedin;
        }; 
        if(type == 'add'){
          this.newCampaign(1, 1);
          this.campaign = {
            title: '',
            funnel: {},
            credentials: [],
            prospectsList: '',
            templates : {
              'email' : this.email_data.templates,
              'linkedin' : this.linkedin_data.templates,
            },
            timeTable: {
              from_hour: 0,
              to_hour: 0,
              time_zone: '',
              sending_days: {
                '0' : true,
                '1' : true,
                '2' : true, 
                '3' : true,
                '4' : true,
                '5' : false,
               '6' : false
              },
            },
          };
        }

        console.log('initCampaign: ', this.campaign);
    },
    async get_campaign_by_id(){
            /* SENDING TO SERVER HERE */
        var campaign_id = this.campaign_id_get;

        var path = CAMPAIGNS_API_GET_BY_ID;
        var get_data = new FormData();
        get_data.append('_campaign_id', campaign_id);
        
        console.log(get_data);
        this.request_json = this._formdata_to_json(get_data);
        await axios.post(path, get_data)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error getting campaign " + r.msg;
              alert(msg);
            }else{ 
              var updated = r.updated;
              console.log(updated);            
            }
          })
          .catch((error) => {
            var msg = "Error getting campaign " + error;
            alert(msg);
          });
  },
  async newCampaign(page=1, init=0){
        const path = CAMPAIGNS_API_LIST;
        
        var data = new FormData();
        if (init == 1){
            //data.append('_init', 1);
            data.append('_create', 1);
        }
        data.append('_page', page);
        
        console.log(data);
        this.request_json = this._formdata_to_json(data);
        await axios.post(path, data)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error loading campaigns " + r.msg;
              alert(msg);
            }else{                
              this.update_data(r, init);
            }
          })
          .catch((error) => {
            var msg = "Error loading campaigns " + error;
            alert(msg);
          });

    },
    update_data(newJson, init){
        if (init == 1){
          this.list_data.prospect_lists = JSON.parse(newJson.prospect_lists);
          this.list_data.columns = JSON.parse(newJson.columns);
          this.list_data.funnels = JSON.parse(newJson.funnels);
          this.list_data.credentials = JSON.parse(newJson.credentials);
        }

        /* This will help to prevent: JSON parse error in console */
        if (newJson.campaigns){
          this.list_data.campaigns = JSON.parse(newJson.campaigns);

          /* FOR TEST ONLY - to show response in textarea. NO NEED in production */
          this.response_json = newJson;
        }
        this.list_data.pagination = JSON.parse(newJson.pagination);
        console.log('load from server: ', this.list_data);
    },
    createCampaign(){
        const path = CAMPAIGNS_API_CREATE;
        var credentials = [];

        if (this.email_data.email_account_selected.length != 0){
          console.log('email account');
          console.log(this.email_data.email_account_selected);

          credentials.push(this.email_data.email_account_selected);
        }

        if (this.linkedin_data.linkedin_account_selected.length != 0){
          console.log('linkedin account');
          console.log(this.linkedin_data.linkedin_account_selected);

          credentials.push(this.linkedin_data.linkedin_account_selected);
        }

        this.campaign.templates.email = this.email_data.templates;
        this.campaign.templates.linkedin = this.linkedin_data.templates;
        this.campaign.funnel = this.campaign.funnel._id.$oid;
        this.campaign.credentials = credentials;
        console.log('RESALT CAMPAIGN: ');
        console.log(this.campaign);

        var createData = new FormData();
        createData.append('_add_campaign', JSON.stringify(this.campaign));
        
        console.log(createData);
        this.request_json = this._formdata_to_json(createData);
        axios.post(path, createData)
          .then((res) => {
            var r = res.data;
            this.response_json = r;
            if (r.code <= 0){
              var msg = "Error creating campaign " + r.msg;
              alert(msg);
            }else{                
            }
          })
          .catch((error) => {
            var msg = "Error creating campaign " + error;
            alert(msg);
          });
    },
    _formdata_to_json(form_data){
      var object = {};
      form_data.forEach(function(value, key){
        object[key] = value;
      });
      var json = JSON.stringify(object);
      return json;
    },
    validateStep(ref) {
      return this.$refs[ref].validate();
    },
    onStepValidated(step, validated, model) {
      //this.wizardModel.stepsData[step] = JSON.parse(JSON.stringify(model));
      switch(step) {
        case 'step_0': 
          //console.log('step_0: ', model);
          this.campaign.title = model.campaignTitle;
          this.campaign.funnel = model.funnel_selected;
          this.email_data.templates = model.email_templates;
          this.linkedin_data.templates = model.linkedin_templates;
          //console.log('step_0: ', this.campaign.title)
          break;
        case 'step_1':
          this.email_data.email_account_selected = model.account_email;
          this.linkedin_data.linkedin_account_selected = model.account_linkedin;
          this.campaign.prospectsList = model.prospectsList;
          break;
        case 'step_2':
          this.email_data.templates = model.email_templates;
          this.linkedin_data.templates = model.linkedin_templates;
          break;
        case 'step_3':
          this.campaign.timeTable = model.timeTable;
          break;
      }
    },
    wizardComplete() {
      this.createCampaign();
      swal("Good job!", "Campaign created!", "success");
    }
  },
  created() {
    this.initCampaign();
  }
};
</script>
<style lang="scss">
.vue-form-wizard .wizard-icon-circle.tab_shape {
  background-color: #9a9a9a !important;
  color: white;
}
.vue-form-wizard .wizard-tab-content {
  display: flex; // to avoid horizontal scroll when animating
  .wizard-tab-container {
    display: block;
    animation: fadeIn 0.5s;
  }
}
</style>
