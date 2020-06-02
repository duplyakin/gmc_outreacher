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
                    icon="nc-icon nc-cloud-upload-94">
                <second-step style="width: 100%;" :file="file" ref="secondStep" @on-validated="onStepValidated"></second-step>
                </tab-content>

                <tab-content title="Select list"
                    class="col-12"
                    :before-change="() => validateStep('thirdStep')"
                    icon="nc-icon nc-cloud-upload-94">
                    <third-step style="width: 100%;" :lists="lists" ref="thirdStep" @on-validated="onStepValidated"></third-step>
                </tab-content>

            
                <tab-content title="Check status"
                            class="col-12"
                            icon="nc-icon nc-check-2">
                <div>
                    <h2 class="text-center text-space">Last step!
                    <br>
                    <small>Press upload to send data.</small>
                    </h2>
                </div>
                <div v-if="upload_error" class="text-center text-danger invalid-feedback" style="display: block;">
                        {{ upload_error_message }}
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

const FirstStep = () => import('./firstStep.vue')
const SecondStep = () => import('./secondStep.vue')
const ThirdStep = () => import('./thirdStep.vue')

import axios from '@/api/axios-auth'


export default {
    name: 'upload',
    props : ['lists', 'api_url'],
    data () {
        return {
            upload_data: {},
            file : null,
            upload_error: false,
            upload_error_message: ''
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
        onStepValidated (step, validated, model) {
            if (!validated){
                return;
            }

            if (step == 'file_upload' && validated){
                this.file = model.file;
            }

            this.upload_data[step] = JSON.parse(JSON.stringify(model));
        },
        wizardComplete () {
            this.upload_error = false;
            
            const path = this.api_url;

           if (confirm("Are you sure?")){
                var uploadData = new FormData();
                uploadData.append("_upload_data", JSON.stringify(this.upload_data))

                var _this = this;

                axios
                .post(path, uploadData)
                .then((res) => {
                    var result = res.data;
                    
                    if (result.code > 0){
                        var uploaded = JSON.parse(result.uploaded);

                        this.$emit('close');

                        this.valueUpdated(uploaded);
                    }else{
                        _this.upload_error = true;
                        _this.upload_error_message = 'Error upload lead ' + result.msg;
                    }
                })
                .catch((error) => {
                    _this.upload_error = true;
                    _this.upload_error_message = 'Error upload lead ' + error;
                });
           };
        }
    }
}
</script>
<style lang="scss">
.card-wizard {
    width: 100%;
    margin: 10px, 10px, 10px, 10px;
    overflow: auto;
}

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
