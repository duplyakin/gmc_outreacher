<template>
<div class="account-login-modal">
<card>
        <h3>Linkedin login</h3>

        <div class="col-6">
            <div>Login</div>
            <el-input placeholder="Enter login" v-model="login"></el-input>
        </div>
        <div class="col-6">
            <div>Password</div>
            <el-input placeholder="Enter password" v-model="password" show-password></el-input>
        </div>
        <p> </p>
        <div v-if="status != 0" class="notification">Loading. Please wait, it can take a minute...</div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="status != 0" v-on:click="addAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Login</button>
                <button :disabled="status != 0" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
            </div>
        </div>

        <div :v-if="test" class="notification">STATUS: {{status}}</div>
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
        status : Number,
        accountLogin: Function,
        accountStatus: Function,
    },
    data() {
        return {
            login: '',
            password: '',

            test: true,
        }
    },
    methods: {
        addAccount(){
            console.log(typeof this.status)
            console.log(this.status)

            if(!this.login) {
                Notification.error({title: "Error", message: "Empty login"});
                return;
            }
            if(!this.password) {
                Notification.error({title: "Error", message: "Empty password"});
                return;
            }

            this.status = 1;

            console.log(typeof this.status)
            console.log(this.status)


            //this.accountLogin(this.login, this.password);

            setTimeout(this.accountStatus(), 3000);
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
    