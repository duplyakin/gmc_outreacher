<template>
<div>
<card title="Assign selected prospects">
    <form @submit.prevent="assignSubmit">
        <card>
        <div class="row">
            <div class="col-12">
                    <el-select
                    ref="selected_campaign"
                    class="select-default mb-3"
                    v-model="campaign"
                    placeholder="Select campaign">
                    <el-option
                      class="select-default"
                      v-for="campaign in campaigns"
                      :key="campaign._id.$oid"
                      :label="campaign.title"
                      :value="campaign._id.$oid">
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
import axios from 'axios'

export default {
    components: {
        [Select.name]: Select,
        [Option.name]: Option
    },
    name : 'prospect-assign',
    props : {
        campaigns: Array,
        valueUpdated: Function
    },
    data() {
        return {
            campaign : ''
        }
    },
    methods: {
        assignSubmit(){
            if (this.campaign == ''){
                alert('Campaign should not be empty');
                return false;
            }
            if (confirm("Are you sure?")){
                var campaign_id = this.$refs.selected_campaign.value;
                
                this.$emit('close');
                this.valueUpdated(campaign_id);
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
    