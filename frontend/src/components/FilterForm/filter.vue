<template>
        <div class="row">
                <div class="col-4">
                <el-select
                    class="select-default mb-3"
                    v-model="filterData.filter_data"
                    placeholder=""
                    v-validate='required'
                    v-on:change="filterChanged">
                    <el-option
                        class="select-default"
                        v-for="(item, index) in filterData.filters"
                        :key="'select1' + filter_title + index"
                        :label="item.name"
                        :value="item.type">
                    </el-option>
                  </el-select>
                </div>
                
                <div class="col-4">
                  <el-select
                  class="select-default mb-3"
                  v-validate='required'
                  v-model="filterData.condition_data"
                  placeholder="">
                  <el-option
                      class="select-default"
                      v-for="(item, index) in filterData.conditions[filterData.filter_data]"
                      :key="'select2-' + filter_title + index"
                      :label="item"
                      :value="item">
                  </el-option>
                </el-select>
                </div>
                
                <div class="col-3">
                <el-input type="search"
                class="mb-3"
                v-validate='required'
                v-model="filterData.value_data"
                placeholder="Value"
                :key="'value_input-' + filter_title"
                />
                </div>
        </div>
  </template>
  <script>
    //import filter_data from './filter_data.js'
    import { Select, Option } from 'element-ui'

    export default {
      name : 'o-filter',
      components: {
        [Select.name]: Select,
        [Option.name]: Option
      },
      props : ['filter_title'],
      methods:{
        filterChanged: function(){
            this.filterData.condition_data = '';
            this.filterData.value_data = '';
        }
      },
      data () {
        return {
          filterData:  {
    'filter_data' : '',
    'condition_data' : '',
    'value_data' : '',
    'filters' : [
        {
            'id' : 1,
            'type' : 'String',
            'name' : 'Email' 
        },
        {
            'id' : 2,
            'type' : 'Number',
            'name' : 'Last contacted'
        },
        {
            'id' : 3,
            'type' : 'Date',
            'name' : 'Created at'
        }
    ],
    'conditions' : {
        'String' : ['Contains', 'Not contains', 'Equals', 'Not equals'],
        'Number' : ['Equals', 'Greater than', 'Less than'],
        'Date' : ['is']
    }
}
        }
      }
    }
  </script>
  <style>
  </style>
  