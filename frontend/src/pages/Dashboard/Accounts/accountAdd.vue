<template>
<div class="account-add-modal">
<card > 
        <card>
        <div class="row">
            <div class="col-6">
                <label>Select account type</label>
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

                <div class="row">
                    <div class="col-6">
                        <label>Select Linkedin account type</label>
                        <el-select
                            class="select-default mb-3"
                            placeholder="Select type"
                            v-model="model.modification">
                                <el-option
                                class="select-default"
                                v-for="(a_type,index) in linkedin_account_types"
                                :key="index"
                                :label="a_type"
                                :value="a_type">
                                </el-option>
                        </el-select>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <label>Linkedin profile URL</label>
                        <fg-input name="linkedin_account"
                            v-model="model.data.account"
                            placeholder="example: linkedin.com/myaccount"/>
                    </div>
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
import { Button, Popover, Checkbox, Notification, Select, Option } from 'element-ui'
import axios from '@/api/axios-auth';

const OAUTH_SERVER = process.env.VUE_APP_API_URL;

export default {
    components: {
        [Button.name]: Button,
        [Select.name]: Select,
        [Option.name]: Option,
        [Popover.name]: Popover,
        [Checkbox.name]: Checkbox
    },
    name : 'account-add',
    props : {
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            error: false,
            account_types: ['gmail/gsuite', 'linkedin'],
            linkedin_account_types: ['basic', 'premium'],

            model: {
                credentials_type: '',
                modification: '',
                data: {
                    account: '',
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
                    Notification.error({title: "Error", message: "Input your Linkedin profile URL"});
                    return false;
                }
                if(!this.model.data.account.includes('linkedin')) {
                    Notification.error({title: "Error", message: "Linkedin profile URL field must be like: www.linkedin.com/example_user/"});
                    return false;
                }
                if (this.model.modification == '') {
                    Notification.error({title: "Error", message: "Select Linkedin account type"});
                    return false;
                }
                
                this.model.data.account = this.model.data.account.substring(this.model.data.account.indexOf("www"), this.model.data.account.length -1);
                console.log('acc: ', this.model)

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


</style>
    