<template>
<div class="account-edit-modal">
<card :title="modalTitle">
    <form @submit.prevent="submitAccountLimitsData">
        <card>
                <div class="row" v-for="column in limits.columns">
                    <div class="col-3">
                        <label>{{ column.label }}
                            <el-popover
                                placement="top-start"
                                width="auto"
                                trigger="hover"
                                :content="column.explanation">
                                <el-button slot="reference" size="mini" icon="el-icon-question" circle></el-button>
                            </el-popover>
                        </label>    

                    </div>
                    <div class="col-9">
                        <el-slider
                        v-model="limits.current[column.prop]"
                        :max="limits.maximum[column.prop]"
                        show-input>
                      </el-slider>
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
import {Button, Popover, Notification, Slider, Option } from 'element-ui'
import axios from '@/api/axios-auth'

const CREDENTIALS_API_LIMITS_SHOW = '/limits/show';

export default {
    components: {
        [Slider.name]: Slider,
        [Button.name]: Button,
        [Option.name]: Option,
        [Popover.name]: Popover,
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
            
            limits : {
                maximum : {},
                current : {},
                columns : []
            }
        }
    },
    methods: {
        submitAccountLimitsData(){
            const path = this.api_url;

            if (confirm("Are you sure?")){

                var data = new FormData();
                data.append("_credentials_id", this.accountObj._id.$oid)
                data.append("_limits_data", JSON.stringify(this.limits.current));

                axios
                .post(path, data)
                .then((res) => {
                    var result = res.data;
                    if (result.code > 0){
                        this.$emit('close');
                        this.valueUpdated(result);
                    }else{
                        var msg = 'Error editing limits ' + result.msg;
                        Notification.error({title: "Error", message: msg});
                    }
                })
                .catch((error) => {
                    var msg = 'Error editing limits ' + error;
                    Notification.error({title: "Error", message: msg});
                });
            };

        },
        discardEdit(){
            this.$emit('close');
        },
        deserialize_data(data){
            if (data.email_columns || data.linkedin_columns){
                if (this.account_data.medium == 'email'){
                    var email_columns = JSON.parse(data.email_columns);
                    this.$set(this.limits, 'columns', email_columns);
                }else{
                    var linkedin_columns = JSON.parse(data.linkedin_columns);
                    this.$set(this.limits, 'columns', linkedin_columns);
                }
            }

            if (data.limits){
                var limits = JSON.parse(data.limits);

                this.$set(this.limits, 'maximum', limits.maximum);
                this.$set(this.limits, 'current', limits.current);
            }
        },
        load_limits(credentials_id){
            var data = new FormData();
            data.append('_credentials_id', credentials_id);

            const path = CREDENTIALS_API_LIMITS_SHOW;

            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code > 0){
                    this.deserialize_data(r);
                }else{
                    Notification.error({title: "Error", message: r.msg});
                }
            })
            .catch((error) => {
                var msg = 'Error loading limits ' + error;
                Notification.error({title: "Error", message: msg});
            });
        }
    }, 
    mounted() {
        this.account_data = JSON.parse(JSON.stringify(this.accountObj));
        this.load_limits(this.accountObj._id.$oid);
    }
}
</script>
<style>
label {
    color:black;
}
</style>
    