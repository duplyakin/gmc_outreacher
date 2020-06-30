<template>
<div class="account-edit-modal">
<card :title="modalTitle">
    <form @submit.prevent="submitAccountLimitsData">
        <card>
            <div v-if="account_data.medium === 'email'">
                <div class="row">
                    <div class="col-12">
                        <el-slider
                        v-model="email_limits.sending_maximum"
                        show-input>
                      </el-slider>
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
import { Notification, Slider, Option } from 'element-ui'
import axios from '@/api/axios-auth'

const CREDENTIALS_API_LIMITS_SHOW = '/limits/show';

export default {
    components: {
        [Slider.name]: Slider,
        [Option.name]: Option
    },
    name : 'account-limits-edit',
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
            },

            email_limits : {
                sending_maximum : 0
            },
            linkedin_limits : {
                account_maximum : 0,
                search_maximum : 0,
                parse_profile_maximum : 0,
                visit_profile_maximum : 0,
                connect_maximum : 0,
                send_message_maximum : 0 
            },
        }
    },
    methods: {
        submitAccountLimitsData(){
            const path = this.api_url;
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
    