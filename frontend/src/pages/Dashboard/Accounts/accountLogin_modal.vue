<template>
<div class="account-login-modal">
    <card>
        <h3>Linkedin login</h3>

        <div class="row justify-content-center mb-3">
            <div class="col-12">
                <label>Login</label>
                <el-input placeholder="Enter login" v-model="login"></el-input>
            </div>

        </div>
        <div class="row justify-content-center mb-3">
            <div class="col-12">
                <label>Password</label>
                <el-input placeholder="Enter password" v-model="password" show-password></el-input>
            </div>

        </div>
        <p> </p>
        <div v-if="ack" class="notification">Loading. Please wait, it can take a minute...</div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="ack" v-on:click="addAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Login</button>
                <button :disabled="ack" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
            </div>
        </div>

    </card>
</div>
</template>

<script>
import { Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth';


export default {
    components: {
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
            ack: false,

        }
    },
    methods: {
        async addAccount(){

            if(!this.login) {
                Notification.error({title: "Error", message: "Empty login"});
                return;
            }
            if(!this.password) {
                Notification.error({title: "Error", message: "Empty password"});
                return;
            }

            this.ack = true;

            this.accountLoginBS(this.credentials_id, this.login, this.password);
        },
        discard(){
            this.$emit('close');
        }
    },
    mounted() {
    }
}
</script>
<style>
.notification {
    color: rgb(56, 56, 179);
    text-transform: uppercase;
    font-size: 10px;
}
</style>
    