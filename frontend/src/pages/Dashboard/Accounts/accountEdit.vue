<template>
<div class="account-edit-modal">
<card :title="modalTitle">
    <form @submit.prevent="submitAccountData">
        <card>
        <div class="row">
            <div class="col-12">
            <fg-input name="limits_per_day"
                label="Limits per day"
                class="mb-3"
                v-model="account_data.limit_per_day"/>
            </div>
        </div>
        <div v-if="account_data.medium === 'linkedin'">
            <div class="row">
                <div class="col-12">
                    <fg-input name="linkedin_account"
                        label="Linkedin account"
                        class="mb-3"
                        v-model="account_data.data.account"
                        placeholder="example: linkedin.com/your_account"/>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <fg-input name="linkedin_login"
                        label="Linkedin login"
                        class="mb-3"
                        v-model="account_data.data.login"/>
                </div>
            </div>

                <div class="row">
                <div class="col-12">
                    <fg-input name="linkedin_password"
                        label="Linkedin password"
                        class="mb-3"
                        v-model="account_data.data.password"/>
                </div>
            </div>

                <div class="row">
                <div class="col-12">
                    <fg-input name="linkedin_cookie (li_at)"
                        label="li_at cookie value"
                        class="mb-3"
                        v-model="account_data.data.li_at"/>
                </div>
            </div>

        </div>
        </card>
        <div class="row">
                <div class="col-12 d-flex flex-row-reverse">
                    <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Save</button>
                    <button v-on:click="discardEdit" type="button" class="btn btn-outline btn-wd btn-danger">Discard</button>
                </div>
        </div>
    </form>  
</card>
</div>
</template>

<script>
import { Select, Option } from 'element-ui'
import axios from '@/api/axios-auth'

export default {
    components: {
        [Select.name]: Select,
        [Option.name]: Option
    },
    name : 'account-edit',
    props : {
        modalTitle: String,
        accountObj: Object,
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            account_data : {
                medium : '',
                limit_per_day : 0,
                data : {

                }
            }
        }
    },
    methods: {
        submitAccountData(){
            const path = this.api_url;
            if (Object.keys(this.account_data).length === 0 ){
                alert("Data can't be empty");
                return false;
            }

            if (confirm("Are you sure?")){

                var accountData = new FormData();
                accountData.append("_credentials", JSON.stringify(this.account_data))
                accountData.append("_credentials_id", this.account_data._id.$oid)

                axios
                .post(path, accountData)
                .then((res) => {
                    var result = res.data;
                    if (result.code > 0){
                        var updated_account = JSON.parse(result.updated);
                        this.$emit('close');
                        this.valueUpdated(updated_account);
                    }else{
                        var msg = 'Error editing account ' + result.msg;
                        alert(msg)
                    }
                })
                .catch((error) => {
                    var msg = 'Error editing account ' + error;
                    alert(msg);
                });
            };
        },
        discardEdit(){
            this.$emit('close');
        }
    },
    mounted() {
        this.account_data = JSON.parse(JSON.stringify(this.accountObj));
    }
}
</script>
<style>
label {
    color:black;
}
</style>
    