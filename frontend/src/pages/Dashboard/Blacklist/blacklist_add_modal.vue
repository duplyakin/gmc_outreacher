<template>
<div>
<card>
    <form @submit.prevent="listAddSubmit">
        <h4>Add to "Do Not Contact list"</h4>
        <card>

        <div class="row">
            <div class="col-12">
                <label>Emails</label>
                <fg-input>
                    <textarea
                        class="form-control"
                        placeholder="john@yahoo.com mikle@gmail.com"
                        rows="3"
                        name="emails"
                        v-model="emails"
                    ></textarea>
                </fg-input>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <label>Domains</label>
                <fg-input>
                    <textarea
                        class="form-control"
                        placeholder="somedomain.com anotherdomain.ua"
                        rows="3"
                        name="domains"
                        v-model="domains"
                    ></textarea>
                </fg-input>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <label>Linkedin accounts</label>
                <fg-input>
                    <textarea
                        class="form-control"
                        placeholder="www.linkedin.com/in/john www.linkedin.com/in/mikle"
                        rows="3"
                        name="linkedins"
                        v-model="linkedins"
                    ></textarea>
                </fg-input>
            </div>
        </div>

        </card>
        <div class="row">
            <div class="col-12 d-flex flex-row-reverse">
                <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Save</button>
                <button v-on:click="discard" type="button" class="btn btn-outline btn-wd btn-danger">Discard</button>
            </div>
        </div>
    </form>  
</card>
</div>
</template>

<script>
import axios from '@/api/axios-auth';;
import { Notification } from "element-ui";

export default {
    components: {
    },
    props : {
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            emails: '',
            domains: '',
            linkedins: '',
        }
    },
    methods: {
        split_data(str) {
            str = str.replace(new RegExp('\rn', 'g'), ' ')
            str = str.replace(new RegExp('\r', 'g'), ' ')
            str = str.replace(new RegExp('\n', 'g'), ' ')
            str = str.replace(new RegExp(',', 'g'), ' ')

            var arr = str.split(" ")
                .filter(function (item) {
                    if (item != '') {
                        return item
                    }
                })

            return arr
        },
        listAddSubmit(){
            if (this.emails == '' && this.domains == '' && this.linkedins == ''){
                Notification.error({title: "Error", message: 'Enter emails or domains or lincedin accounts'})
                return 
            }

            if (confirm("Are you sure?")) {
                let entities = {
                    emails: this.split_data(this.emails),
                    domains: this.split_data(this.domains),
                    linkedin: this.split_data(this.linkedins),
                }

                //console.log(entities)
            
                const path = this.api_url

                var data = new FormData()
                data.append('entities', JSON.stringify(entities))
                
                axios
                .post(path, data)
                .then((res) => {
                    var r = res.data

                    if (r.code > 0){
                        this.$emit('close')
                        this.valueUpdated()

                    } else {
                        var msg = 'Error edditing list ' + r.msg
                        Notification.error({title: "Error", message: msg})
                    }
                })
                .catch((error) => {
                    var msg = 'Error editing list ' + error;
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
</style>
    