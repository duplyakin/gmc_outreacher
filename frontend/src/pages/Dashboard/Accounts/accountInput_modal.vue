<template>
<div class="account-login-modal">
<card>
        <h3>Input code</h3>

        <pulse-loader :loading="loading" :color="color"></pulse-loader>

        <div v-if="!loading">
        <div class="row">
            <div class="col-6 mb-5">
                <el-input placeholder="Enter code" v-model="input" :disabled="loading"></el-input>
            </div>
        </div>

        <card>
            <img v-bind:src="'data:image/jpeg;base64,' + screenshot" />
        </card>
        
        <p> </p>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="loading" v-on:click="inputAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Input</button>
                <button :disabled="loading" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
            </div>
        </div>
        </div>

</card>
</div>
</template>

<script>
import { Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth'
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'

export default {
    components: {
        PulseLoader,
        [Select.name]: Select,
        [Option.name]: Option,
    },
    props : {
        screenshot: String,
        credentials_id: String,
        accountInputBS: Function,
    },
    data() {
        return {
            input: '',

            loading: false,
            color: "#a7a7ff",
        }
    },
    methods: {
        async inputAccount(){

            if(!this.input) {
                Notification.error({title: "Error", message: "Empty input"})
                return
            }

            this.loading = true

            this.accountInputBS(this.credentials_id, this.input)
        },
        discard(){
            this.$emit('close')
        }
    },
    mounted() {
    }
}
</script>
<style>
</style>
    