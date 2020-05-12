<template>
<div class="prospect-edit-modal">
<card :title="modalTitle">
    <form @submit.prevent="submitProspectData">
        <card>
        <div class="row">
            <div class="col-12">
            <fg-input name="Email"
                label="Email"
                class="mb-3"
                v-model="prospect_data.data.email"/>
            </div>
        </div>
        <div class="row">
                <div class="col-12">
                <fg-input name="Linkedin"
                    label="Linkedin"
                    class="mb-3"
                    v-model="prospect_data.data.linkedin"/>
                </div>
            </div>
        <div class="row">
                <div class="col-6">
                <fg-input name="First Name"
                    label="First Name"
                    class="mb-3"
                    v-model="prospect_data.data.first_name"/>
                </div>
                <div class="col-6">
                        <fg-input name="Last Name"
                            label="Last Name"
                            class="mb-3"
                            v-model="prospect_data.data.last_name"/>
                </div>
        </div>
        <div class="row">
            <div class="col-12">
                    <fg-input name="Company"
                    label="Company"
                    class="mb-3"
                    v-model="prospect_data.data.company"/>
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
import axios from '@/api/axios-auth'
import { Notification, Select, Option } from 'element-ui'

export default {
    components: {
      [Select.name]: Select,
      [Option.name]: Option
    },
    name : 'prospect-edit',
    props : {
        modalTitle: String,
        action: String,
        prospectObj: Object,
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            object_before_changes : null,
            prospect_data : {
                data : {
                    email : '',
                    linkedin : '',
                    first_name : '',
                    last_name : '',
                    lists : '',
                    company : ''
                },
            },
            filters : {
                campaings: '',
                lists : ''
            }
        }
    },
    methods: {
        submitProspectData(){
           const path = this.api_url;
            if (this.prospect_data.data.email == ''){
                Notification.error({title: "Error", message: "Email can't be empty"});
                return false;
            }
            
            console.log(this.prospect_data.data.email)

           if (confirm("Are you sure?")){
                var prospectData = new FormData();
                var _prospect = JSON.stringify(this.prospect_data);
                prospectData.append("_prospect", _prospect);

                axios
                .post(path, prospectData)
                .then((res) => {
                    var result = res.data;
                    if (result.code > 0){
                        var updated_prospect = null;
                        if (result.updated){
                            updated_prospect = JSON.parse(result.updated);
                        }

                        this.$emit('close');
                        this.valueUpdated(updated_prospect);
                    }else{
                        var msg = 'Answer Error editing prospect ' + result.msg;
                        Notification.error({title: "Error", message: msg});
                    }
                })
                .catch((error) => {
                    var msg = 'Answer Error editing prospect ' + error;
                    Notification.error({title: "Error", message: msg});
                });
           };
        },
        discardEdit(){
            this.$emit('close');
        }
    },
    mounted() {
        if (this.action == 'edit'){
            this.prospect_data =  JSON.parse(JSON.stringify(this.prospectObj));
        }
    }
}
</script>
<style>
label {
    color:black;
}
</style>
  