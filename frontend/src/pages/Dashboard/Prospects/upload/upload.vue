<template>
<div>
    <div class="row d-flex justify-content-center">
        <div class="card card-wizard" id="wizardCard">
        <form-wizard shape="tab"
                        @on-complete="wizardComplete"
                        error-color="#FB404B"
                        color="#35495E">

            <tab-content title="Select file"
                        class="col-12"
                        :before-change="() => validateStep('firstStep')"
                        icon="nc-icon nc-cloud-upload-94">
            <first-step ref="firstStep" @on-validated="onStepValidated"></first-step>
            </tab-content>

            <tab-content title="Map fields"
                        class="col-12"
                        :before-change="() => validateStep('secondStep')"
                        icon="nc-icon nc-bullet-list-67">
            <second-step ref="secondStep" @on-validated="onStepValidated"></second-step>
            </tab-content>

            <tab-content title="Add list name"
                class="col-12"
                :before-change="() => validateStep('thirdStep')"
                icon="nc-icon nc-tag-content">
            <third-step ref="thirdStep" @on-validated="onStepValidated"></second-step>
            </tab-content>

            <tab-content title="Check status"
                        class="col-12"
                        icon="nc-icon nc-check-2">
            <div>
                <h2 class="text-center text-space">Done!
                <br>
                <small>Prsing data - it should soon appear in the table.</small>
                </h2>
            </div>
            </tab-content>

            <button slot="prev" class="btn btn-default btn-fill btn-wd btn-back">Back</button>
            <button slot="next" class="btn btn-default btn-fill btn-wd btn-next">Next</button>
            <button slot="finish" class="btn btn-success btn-fill btn-wd">Upload</button>
        </form-wizard>
        </div>
    </div>
</div>
</template>
<script>
import {FormWizard, TabContent} from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'

import FirstStep from './firstStep.vue'
import SecondStep from './secondStep.vue'
import ThirdStep from './thirdStep.vue'


export default {
    name: 'upload',
    data () {
    return {
        upload_data: {}
    }
    },
    components: {
        FormWizard,
        TabContent,
        FirstStep,
        SecondStep,
        ThirdStep
    },
    methods: {
    validateStep (ref) {
        return this.$refs[ref].validate()
    },
    onStepValidated (validated, model) {
        this.upload_data = {...this.upload_data, ...model}
    },
    wizardComplete () {
        //Upload to server code here
        console.log(this.upload_data);
    }
    }
}
</script>
<style lang="scss">
.vue-form-wizard .wizard-icon-circle.tab_shape {
    background-color: #9A9A9A !important;
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
