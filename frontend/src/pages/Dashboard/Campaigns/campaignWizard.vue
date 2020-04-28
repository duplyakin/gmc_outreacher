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
              <zero-step ref="zeroStep" @on-validated="onStepValidated"></zero-step>
            </tab-content>

            <tab-content
              title="Step 1"
              class="col-12"
              :before-change="() => validateStep('firstStep')"
              icon="nc-icon nc-badge"
            >
              <first-step ref="firstStep" @on-validated="onStepValidated"></first-step>
            </tab-content>

            <tab-content
              v-if="this.campaign.funnel === this.funnel_email || this.campaign.funnel === this.funnel_email_linkedin"
              title="Step 2 Email"
              class="col-12"
              :before-change="() => validateStep('secondStepEmail')"
              icon="nc-icon nc-notes"
            >
              <second-step-email ref="secondStepEmail" @on-validated="onStepValidated"></second-step-email>
            </tab-content>

            <tab-content
              v-if="this.campaign.funnel === this.funnel_linkedin || this.campaign.funnel === this.funnel_email_linkedin"
              title="Step 2 LinkedIn"
              class="col-12"
              :before-change="() => validateStep('secondStepLinkedin')"
              icon="nc-icon nc-notes"
            >
              <second-step-linkedin ref="secondStepLinkedin" @on-validated="onStepValidated"></second-step-linkedin>
            </tab-content>

            <tab-content
              title="Step 3"
              class="col-12"
              :before-change="() => validateStep('thirdStep')"
              icon="nc-icon nc-notes"
            >
              <third-step ref="thirdStep" @on-validated="onStepValidated"></third-step>
            </tab-content>

            <tab-content
              title="Preview"
              class="col-12"
              :before-change="() => validateStep('lastStep')"
              icon="nc-icon nc-check-2"
            >
              <last-step ref="lastStep" :campaign="campaign" @on-validated="onStepValidated"></last-step>
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
import SecondStepEmail from "./Wizard/SecondStepEmail.vue";
import SecondStepLinkedin from "./Wizard/SecondStepLinkedin.vue";
import ThirdStep from "./Wizard/ThirdStep.vue";
import LastStep from "./Wizard/LastStep.vue";
import swal from "sweetalert2";

export default {
  data() {
    return {
      funnel_email: 'Email campaign',
      funnel_linkedin: 'LinkedIn campaign',
      funnel_email_linkedin: 'Email & LinkedIn campaign',
      campaign: {
        name: '',
        funnel: '',
        account: '',
        prospectsList: '',
        messagesListEmail: [],
        messagesListLinkedin: [],
        timeTable: {
          from: '',
          till: '',
          timezone: '',
          days: [],
        },
      },
      wizardModel: {
        stepsData: {}
      }
    };
  },
  components: {
    FormWizard,
    TabContent,
    ZeroStep,
    FirstStep,
    SecondStepEmail,
    SecondStepLinkedin,
    ThirdStep,
    LastStep
  },
  methods: {
    validateStep(ref) {
      return this.$refs[ref].validate();
    },
    onStepValidated(step, validated, model) {
      //this.wizardModel.stepsData[step] = JSON.parse(JSON.stringify(model));
      switch(step) {
        case 'step_0': 
          //console.log('step_0: ', model);
          this.campaign.name = model.campaignName;
          this.campaign.funnel = model.campaignType;
          break;
        case 'step_1':
          this.campaign.account = model.account;
          this.campaign.prospectsList = model.prospectsList;
          break;
        case 'step_2_email':
          //console.log('step_2_email: ', model);
          //console.log('step_2_email campaign: ', this.campaign.messagesListEmail);
          this.campaign.messagesListEmail = model.messages;
          break;
        case 'step_2_linkedin':
          this.campaign.messagesListLinkedin = model.messages;
          break;
        case 'step_3':
          this.campaign.timeTable = model.timeTable;
          break;
      }
    },
    wizardComplete() {
      swal("Good job!", "You clicked the finish button!", "success");
    }
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
