<template>
<div class="account-login-modal">
<card>
        <h3>Resolve captcha</h3>

        <pulse-loader :loading="loading" :color="color"></pulse-loader>

        <div v-if="!loading" class="mb-3">
            <vue-recaptcha @verify="get_response" :sitekey="sitekey" :loadRecaptchaScript="true"></vue-recaptcha>
        </div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="loading" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
            </div>
        </div>

</card>
</div>
</template>

<script>
import { Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth'
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'
import VueRecaptcha from 'vue-recaptcha';

export default {
    components: {
        VueRecaptcha,
        PulseLoader,
        [Select.name]: Select,
        [Option.name]: Option,
    },
    props : {
        sitekey: String,
        credentials_id: String,
        accountInputBS: Function,
    },
    data() {
        return {
            sitekey_captcha: '',

            loading: false,
            color: "#a7a7ff",
        }
    },
    methods: {
        get_response(response) {
            //console.log("response:", response)
            if(response == null || response == '') {
                return
            }

            this.loading = true

            this.accountInputBS(this.credentials_id, response)
        },
        discard(){
            this.$emit('close')
        }
    },
    mounted() {
    },
    created() {
        //this.sitekey_captcha = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
    }
}
</script>
<style>
</style>