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
        <div v-if="model.credentials_type == 'linkedin'">

                <p class="labels">Linkedin profile URL</p>
                <div>
                    <fg-input name="linkedin_account"
                        v-model="model.data.account"
                        placeholder="example: linkedin.com/myaccount"/>
                </div>

                <p class="labels">Linkedin login
                <el-popover
                    placement="top-start"
                    title="Why login better then li_at?"
                    width="200"
                    trigger="hover"
                    content="It's safer for prevent linkedin blocking.">
                    <el-button slot="reference"><i class='el-icon-question'></i></el-button>
                </el-popover>
                </p>
                <div>
                    <fg-input name="linkedin_login"
                        v-model="model.data.login"
                        placeholder="example: myemail@gmail.com"/>
                </div>

                <p class="labels">Linkedin password</p>
                <div>
                    <fg-input name="linkedin_password"
                        v-model="model.data.password"/>
                </div>

                <p class="labels">Linkedin li_at cookie
                <el-popover
                    placement="top-start"
                    title="What is li_at?"
                    width="200"
                    trigger="hover"
                    content='li_at allows us to login linkedin without user password. Get li_at here: //www.some_link.here'>
                    <el-button slot="reference"><i class='el-icon-question'></i></el-button>
                </el-popover>
                </p>
                <div>
                    <fg-input name="linkedin_li_at"
                        v-model="model.data.li_at"/>
                </div>
  
                <p class="labels">Limits per day
                <el-popover
                    placement="top-start"
                    title="What is limits?"
                    width="200"
                    trigger="hover"
                    content='Limits - maximum messages from current account allowd by Linkedin.'>
                    <el-button slot="reference"><i class='el-icon-question'></i></el-button>
                </el-popover>
                </p>
                <div>
                    <fg-input name="limits_per_day"
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
</card>
</div>
</template>

<script>
import { Popover, Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth';

const OAUTH_SERVER = process.env.VUE_APP_API_URL;

export default {
    components: {
        [Select.name]: Select,
        [Option.name]: Option,
        [Popover.name]: Popover,
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
                    password : '',
                    li_at: ''
                }
            }
        }
    },
    methods: {
        addAccount(){
            const path = this.api_url;
            if (this.model.credentials_type == '' ) {
                Notification.error({title: "Error", message: "Select account type"});
                return false;
            } else if (this.model.credentials_type == 'linkedin') {

                if (this.model.data.account == '') {
                    Notification.error({title: "Error", message: "Input your linkedin profile URL"});
                    return false;
                }
                if(!this.model.data.account.includes('linkedin')) {
                    Notification.error({title: "Error", message: "Linkedin profile URL field must be like: www.linkedin.com/example_user/"});
                    return false;
                }
                
                this.model.data.account = this.model.data.account.substring(this.model.data.account.indexOf("www"), this.model.data.account.length -1);
                console.log('acc: ', this.model.data.account)

                if (((this.model.data.login == '') || (this.model.data.password == '')) && (this.model.data.li_at == '')) {
                    Notification.error({title: "Error", message: "Input your login and password or li_at cookie"});
                    return false;
                }
            }

            if (confirm("Are you sure?")) {

                var accountData = new FormData();
                accountData.append("_credentials", JSON.stringify(this.model))

                axios
                .post(path, accountData)
                .then((res) => {
                    var result = res.data;
                    if (result.code > 0){
                        if (result.hasOwnProperty('redirect')) {
                            var redirect_url = OAUTH_SERVER + result.redirect;
                            window.open(redirect_url, "_blank", "width=600,height=400,left=200,top=200");
                        } else {
                            this.valueUpdated(null);
                        }

                        this.$emit('close');
                    } else {
                        var msg = 'Error adding account ' + result.msg;
                        Notification.error({title: "Error", message: msg});
                    }
                })
                .catch((error) => {
                    var msg = 'Error adding account ' + error;
                    Notification.error({title: "Error", message: msg});
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
.el-icon-question {
    font-size: 16px;
    color: #c0c4cc;
    margin: 12px 0 16px;
    line-height: 0px;
}
.labels {
  text-transform: uppercase;
  /*text-align: left;*/
  font-size: 12px;
  font-weight: 100;
  padding: 0px 20px;
  color: #8b8c91;
}
.container {
  display: flex;
  justify-content: space-around;
  padding: 0px 20px;
  align-items: flex-start;
  max-width: 260px;
}
</style>
    