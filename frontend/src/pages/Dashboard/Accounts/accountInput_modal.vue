<template>
<div class="account-login-modal">
<card>
        <h3>Input code</h3>
        <card>
            <img v-bind:src="'data:image/jpeg;base64,' + screenshot" />
        </card>

        <div class="col-6">
            <div>Input</div>
            <el-input placeholder="Enter code" v-model="input"></el-input>
        </div>
        
        <p> </p>
        <div v-if="ack != 0" class="notification">Loading. Please wait, it can take a minute...</div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="ack != 0" v-on:click="inputAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Input</button>
                <button :disabled="ack != 0" v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
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
        screenshot: String,
        credentials_id: String,
        accountInputBS: Function,
    },
    data() {
        return {
            input: '',
            ack: 0,
        }
    },
    methods: {
        async inputAccount(){

            if(!this.input) {
                Notification.error({title: "Error", message: "Empty input"});
                return;
            }

            this.ack = 1;

            this.accountInputBS(this.credentials_id, this.input);
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
    