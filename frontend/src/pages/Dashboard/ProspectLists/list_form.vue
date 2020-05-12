<template>
<div>
<card :title="modalTitle">
    <form @submit.prevent="listAddSubmit">
        <card>
        <div class="row">
            <div class="col-12">
                <fg-input name="new_list_input"
                    ref="createNewListInput"
                    placeholder="Input list title"
                    label="Input list title"
                    class="mb-3"
                    v-model="list_title"
                    />
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
    name : 'list-create',
    props : {
        modalTitle: String,
        action: String,
        listObj: Object,
        api_url : String,
        valueUpdated: Function
    },
    data() {
        return {
            list_title : ''
        }
    },
    methods: {
        listAddSubmit(){
            if (this.list_title == ''){
                Notification.error({title: "Error", message: 'List title can not be empty'});
                return false;
            }
            
            const path = this.api_url;
            if (confirm("Are you sure?")){
                var data = new FormData();
                data.append('_list_title', this.list_title);
                if (this.action == 'edit'){
                    data.append('_list_id', this.listObj._id.$oid)
                }
                
                axios
                .post(path, data)
                .then((res) => {
                    var r = res.data;
                    if (r.code > 0){
                        this.$emit('close');
                        this.valueUpdated(this.list_title);
                    }else{
                        var msg = 'Error editing list ' + r.msg;
                        Notification.error({title: "Error", message: msg});
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
        if (this.action == 'edit'){
            this.list_title =  this.listObj.title || '';
        }
    }
}
</script>
<style>
label {
    color:black;
}
</style>
    