<template>
<div class="account-login-modal">
<card>
        <h3>Input code</h3>

        <div class="row">
            <div class="col-6 mb-5">
                <el-input placeholder="Enter code" v-model="input" :disabled="ack"></el-input>
            </div>
        </div>

        <card>
            <img v-bind:src="'data:image/jpeg;base64,' + screenshot" />
        </card>
        
        <p> </p>

        <div v-if="ack" class="o24_notification mb-3">Loading. Please wait, it can take a minute...</div>

        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button :disabled="ack" v-on:click="inputAccount" type="button" class="btn btn-outline btn-wd btn-success mx-1">Input</button>
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
        screenshot: String,
        credentials_id: String,
        accountInputBS: Function,
    },
    data() {
        return {
            input: '',
            ack: false,
        }
    },
    methods: {
        async inputAccount(){

            if(!this.input) {
                Notification.error({title: "Error", message: "Empty input"});
                return;
            }

            this.ack = true;

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
.o24_notification {
    color: rgb(56, 56, 179);
    text-transform: uppercase;
    font-size: 10px;
}
</style>
    