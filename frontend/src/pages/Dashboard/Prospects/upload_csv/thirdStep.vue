<template>
<div class="second-step">
    <h5 class="text-center">Select ot create the list</h5>
    <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
            {{ error_message }}
    </div>
    <card>
    <div class="row text-center">
    <div class="col-12">
        <label for="create_new_checkbox_id" class="form-check-label">
            <input :value="model.createNew" @change="toggleCreateNew" id="create_new_checkbox_id" type="checkbox" class="form-check-input">
                <span class="form-check-sign"></span>Create the new list
        </label>
        <br>
    </div>
    </div>
    <div class="row d-flex">
    <div class="col-12">
        <fg-input name="new_list_input"
            ref="createNewListInput"
            placeholder="Input list title"
            label="Input list name"
            class="mb-3"
            v-model="model.list.list_new_label"
            v-if="model.createNew"/>

        <el-select
        v-if="!model.createNew"
        class="select-default mb-3"
        placeholder="Select existing list"
        v-model="model.list.list_selected_id">
            <el-option
            class="select-default"
            v-for="(list,index) in lists"
            :key="index"
            :label="list.label"
            :value="list._id.$oid">
            </el-option>
        </el-select>
    </div>
    </div>
</card>
</div>
</template>
<script>
import { Select, Option } from 'element-ui'
import { drop, every, forEach, get, isArray, map, set } from 'lodash';

export default {
    name : 'third-step',
    props : ['lists'],
    components: {
        [Select.name]: Select,
        [Option.name]: Option,
    },
    data () {
    return {
        model:{
            list : {
                list_selected_id : '',
                list_new_label : '',
            },
            createNew : false
        },
        error: false,
        error_message : 'Create or select the list',
    }
    },
    methods: {
        clearState(){
            this.model.list.list_selected_id = '';
            this.model.list.list_new_label = '';
            this.model.createNew = false;

            this.error = false;
        },
        _checkValid(){
            if (this.model.createNew){
                if (this.model.list.list_new_label == ''){
                    this.error = true;
                    this.error_message = 'Input title of the list';
                    return false;
                }
            }else{
                if (this.model.list.list_selected_id == ''){
                    this.error = true;
                    this.error_message = 'Select list';
                    return false;
                }
            }

            this.error = false;
            return true;
        },
        validate () {
            var isValid = this._checkValid();
            if (!isValid){
                return false;
            }

            this.$emit('on-validated', 'list_selected', isValid, this.model);
            return isValid;
        },
        toggleCreateNew() {
                this.model.createNew = !this.model.createNew;
        },
    }
}
</script>
<style>
.second-step{
    width: 100%;
    margin: 10px, 10px, 10px, 10px;
    overflow: auto;
}
</style>
