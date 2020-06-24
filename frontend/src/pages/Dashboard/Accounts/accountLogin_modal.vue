<template>
<div class="account-login-modal">
    <card>
        <h3>Linkedin login</h3>

        <pulse-loader :loading="loading" :color="color"></pulse-loader>

        <div v-if="!loading">
        <div class="row justify-content-center mb-3">
            <div class="col-12">
                <label>Login</label>
                <el-input placeholder="Enter login" v-model="login" :disabled="loading"></el-input>
            </div>
        </div>

        <div class="row justify-content-center mb-3">
            <div class="col-12">
                <label>Password</label>
                <el-input placeholder="Enter password" v-model="password" show-password :disabled="loading"></el-input>
            </div>
        </div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="loading" v-on:click="addAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Login</button>
                <button :disabled="loading" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
            </div>
        </div>
        </div>

    </card>
</div>
</template>

<script>
import { Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth';
import { PulseLoader } from 'vue-spinner/dist/vue-spinner.min.js'

export default {
    components: {
        PulseLoader,
        [Select.name]: Select,
        [Option.name]: Option,
    },
    props : {
        credentials_id: String,
        accountLoginBS: Function,
    },
    data() {
        return {
            login: '',
            password: '',
            
            loading: false,
            color: "#a7a7ff",

        }
    },
    methods: {
        async addAccount(){

            if(!this.login) {
                Notification.error({title: "Error", message: "Empty login"})
                return
            }
            if(!this.password) {
                Notification.error({title: "Error", message: "Empty password"})
                return
            }

            this.loading = true

            this.accountLoginBS(this.credentials_id, this.login, this.password)
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
    