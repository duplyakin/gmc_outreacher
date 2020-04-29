<template>
<div class="test-modal">
<card>
    <form v-if="template" @submit.prevent="submitData">
        <card v-if="template_type === 'email'">
        <div class="row">
            <div class="col-12">
            <input name="subject"
                placeholder="Input subject"
                type="text"
                label="Subject"
                class="mb-3"
                v-model="template.subject"/>
            </div>
        </div>
        <div class="row">
                <div class="col-12">
                <input name="email_body"
                    placeholder="Input body"
                    type="text"
                    label="Email body"
                    class="mb-3"
                    v-model="template.body"/>
                </div>
        </div>
        <div class="row">
                <div class="col-12">
                <input name="email_interval"
                    placeholder="Input interval"
                    type="text"
                    label="Interval in days"
                    class="mb-3"
                    v-model="template.interval"/>
                </div>
        </div>
        </card>


        <card v-if="template_type === 'linkedin'">
                <div class="row">
                    <div class="col-12">
                    <input name="linkedin_message"
                        placeholder="Input message"
                        type="text"
                        label="Message"
                        class="mb-3"
                        v-model="template.message"/>
                    </div>
                </div>
                <div class="row">
                        <div class="col-12">
                        <input name="linkedin_interval"
                            placeholder="Input interval"
                            type="text"
                            label="Interval in days"
                            class="mb-3"
                            v-model="template.interval"/>
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
import { Select, Option, Input } from 'element-ui'
import axios from 'axios'

export default {
    components: {
        [Select.name]: Select,
        [Option.name]: Option,
        [Input.name]: Input
    },
    props : {
        template_type: String,
        templateObj: Object,
        valueUpdated: Function
    },
    data() {
        return {
            template : null,
        }
    },
    methods: {
        submitData(){
            const path = this.api_url;
            /* Don't forget to validate here */
            if (!this.template){
                alert("Template can't be empty")
                return false;
            }

            if (confirm("Are you sure?")){
                this.$emit('close');
                this.valueUpdated(this.template);
            };
        },
        discardEdit(){
            this.$emit('close');
        }
    },
    created() {
        if (Object.keys(this.templateObj).length != 0){
            this.template =  JSON.parse(JSON.stringify(this.templateObj));
            
            /* If we create the new object we don't have properties */
            if (this.template_type === 'email'){
                if (!this.template.hasOwnProperty('subject')){
                    this.template['subject'] = '';
                }
                if (!this.template.hasOwnProperty('body')){
                    this.template['body'] = '';
                }
                if (!this.template.hasOwnProperty('interval')){
                    this.template['interval'] = '';
                }
            }else if(this.template_type === 'linkedin'){
                if (!this.template.hasOwnProperty('message')){
                    this.template['message'] = '';
                }
                if (!this.template.hasOwnProperty('interval')){
                    this.template['interval'] = '';
                }
            }
            console.log(this.template);
        }
    }
}
</script>
<style>
label {
    color:black;
}
</style>
    