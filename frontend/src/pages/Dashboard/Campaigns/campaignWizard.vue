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
              title="Step 2"
              class="col-12"
              :before-change="() => validateStep('secondStep')"
              icon="nc-icon nc-notes"
            >
              <second-step ref="secondStep" @on-validated="onStepValidated"></second-step>
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
              <last-step ref="lastStep" @on-validated="onStepValidated"></last-step>
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

export default {
  data() {
    return {
      //campaignName: '11111111',
      //campaignType: '',
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
    SecondStep,
    ThirdStep,
    LastStep
  },
  methods: {
    validateStep(ref) {
      return this.$refs[ref].validate();
    },
    onStepValidated(step, validated, model) {
      this.wizardModel.stepsData[step] = JSON.parse(JSON.stringify(model));
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
