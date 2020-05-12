<template>
<div>
<card title="Add prospects to the list">
    <form @submit.prevent="listAddSubmit">
        <card>
        <div class="row">
            <div class="col-12">
                    <el-select
                    ref="selected_list"
                    class="select-default mb-3"
                    v-model="prospect_list"
                    placeholder="Select list">
                    <el-option
                        class="select-default"
                        v-for="list in lists"
                        :key="list._id.$oid"
                        :label="list.title"
                        :value="list._id.$oid">
                    </el-option>
                    </el-select>
            </div>
        </div>
        </card>
        <div class="row">
                <div class="col-12 d-flex flex-row-reverse">
                    <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Save</button>
                    <button v-on:click="discardAssign" type="button" class="btn btn-outline btn-wd btn-danger">Discard</button>
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
    name : 'prospect-assign',
    props : {
        lists: Array,
        valueUpdated: Function
    },
    data() {
        return {
            prospect_list : ''
        }
    },
    methods: {
        listAddSubmit(){
            if (this.prospect_list == ''){
                alert('List can not be empty');
                return false;
            }
            if (confirm("Are you sure?")){
                var list_id = this.$refs.selected_list.value;
                
                this.$emit('close');
                this.valueUpdated(list_id);
            }
        },
        discardAssign(){
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
    