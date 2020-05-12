<template>
<div class="account-add-modal">
<card >
        <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
                {{ error_message }}
        </div>        
        <card>
        <div class="row">
            <div class="col-12">
                <p>Select account type</p>
                <el-select
                class="select-default mb-3"
                placeholder="Select type"
                v-model="model.credentials_type">
                    <el-option
                    class="select-default"
                    v-for="(a_type,index) in account_types"
                    :key="index"
                    :label="a_type"
                    :value="a_type">
                    </el-option>
                </el-select>
            </div>
        </div>
        <div v-if="model.credentials_type == 'linkedin'" class="row">
                <div class="col-12">
                    <fg-input name="linkedin_account"
                        label="Linkedin account"
                        class="mb-3"
                        v-model="model.data.account"
                        placeholder="example: linkedin.com/your_account"/>
                </div>
                <div class="col-12">
                    <fg-input name="linkedin_login"
                        label="Linkedin login"
                        class="mb-3"
                        v-model="model.data.login"/>
                </div>
                <div class="col-12">
                    <fg-input name="linkedin_password"
                        label="Linkedin password"
                        class="mb-3"
                        v-model="model.data.password"/>
                </div>     
                <div class="col-12">
                    <fg-input name="limits_per_day"
                    label="Limits per day"
                    class="mb-3"
                    v-model="model.limit_per_day"/>
                </div>
        </div>    
        </card>
        <div class="row">
                <div class="col-12 d-flex flex-row-reverse">
                    <button v-if="model.credentials_type" v-on:click="addAccount"  type="button" class="btn btn-outline btn-wd btn-success mx-1">Add</button>
                    <button v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Close</button>
                </div>
        </div>
    </form>  
</card>
</div>
</template>

<script>
import { Select, Option } from 'element-ui'
import axios from '@/api/axios-auth'

const OAUTH_SERVER = 'http://127.0.0.1:5000';

export default {
    components: {
        [Select.name]: Select,
        [Option.name]: Option
    },
    name : 'account-add',
    props : {
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            error_message : '',
            error : false,
            account_types : ['gmail/gsuite', 'linkedin'],

            model : {
                limit_per_day : 50,
                credentials_type : '',
                data :{
                    account : '',
                    login : '',
                    password : ''
                }
            }
        }
    },
    methods: {
        addAccount(){
            const path = this.api_url;
            if (this.model.credentials_type == '' ){
                alert("Select account type");
                return false;
            }else if (this.model.credentials_type == 'linkedin'){
                if ( (this.model.data.login == '') || 
                    (this.model.data.password == '') ||
                    (this.model.data.account == '')){
                    alert("Input your linkedin account, login and password");
                    return false;
                }
            }

            if (confirm("Are you sure?")){
                var accountData = new FormData();
                accountData.append("_credentials", JSON.stringify(this.model))

                axios
                .post(path, accountData)
                .then((res) => {
                    var result = res.data;
                    if (result.code > 0){
                        if (result.hasOwnProperty('redirect')){
                            var redirect_url = OAUTH_SERVER + result.redirect;
                            window.open(redirect_url, "_blank", "width=600,height=400,left=200,top=200");
                        }else{
                            this.valueUpdated(null);
                        }

                        this.$emit('close');
                    }else{
                        var msg = 'Error adding account ' + result.msg;
                        alert(msg)
                    }
                })
                .catch((error) => {
                    var msg = 'Error adding account ' + error;
                    alert(msg);
                });
            };
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
label {
    color:black;
}
</style>
    