<template>
<div class="second-step">
    <h5 class="text-center">Map columns to fields</h5>
    <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
            {{ error_message }}
    </div>
    <card>
    <div class="row text-center">
        <div class="col-12">
        <label for="update_existing_checkbox" class="form-check-label">
            <div class="container"> 
                <div><input :value="model._update_existing" @change="toggleUpdateExisting" id="update_existing_checkbox" type="checkbox" class="form-check-input"></div>
                <div class="red"> Update existing if duplicates found </div> 
            </div>
        </label>
        <br>
    </div>
    </div>
                
    <div class="row">
    <div class="col-12">
            <el-table stripe
            ref="map_fields_table"
            style="width: 100%;"
            @selection-change="handleSelectionChange"
            :data="csv_data"
            max-height="500"
            border>
            <el-table-column
                    type="selection"
                    width="55"
                    v-if="csv_data"
                    fixed>
            </el-table-column>
            <el-table-column
                label="Select columns to upload"
                prop="header"
                width="auto">
            </el-table-column>
            <el-table-column
                label="Sample data in column"
                prop="sample_data"
                width="auto">
            </el-table-column>
            <el-table-column
                label="Map column to"
                width="auto">
                <template slot-scope="props">
                        <el-select
                        class="select-default mb-3"
                        placeholder="Select field"
                        v-model="props.row.map_selected">
                            <el-option
                            class="select-default"
                            v-for="(field,index) in data_fields"
                            :key="index"
                            :label="field"
                            :value="field">
                            </el-option>
                        </el-select>
                </template>
            </el-table-column>
        </el-table>
    </div>
    </div>
</card>
</div>
</template>
<script>
import { Table, TableColumn, Select, Option } from 'element-ui'
import { drop, every, forEach, some, get, isArray, map, set } from 'lodash';

import Papa from 'papaparse';
import mimeTypes from "mime-types";

export default {
    name : 'second-step',
    props : ['file'],
    components: {
      [Select.name]: Select,
      [Option.name]: Option,
      [Table.name]: Table,
      [TableColumn.name]: TableColumn
    },
    data () {
    return {
        model:{
            _update_existing : 0,
            _csv: null,
            columnsChecked : []
        },
        error: false,
        error_message : 'Selection required',
        csv_data : [],

        _sample: null,
        modelValidations: {
          map_selected: {
            required: true
          },
        },

        current_file : '',
        map_selected : '',
        data_fields: ['email', 'linkedin', 'first_name', 'last_name', 'url']
    }
    },
    watch: {
        file(newValue) {
            this.clearState();

            this.current_file = newValue.raw;
            
            this._load(this.current_file);
        }
    },
    methods: {
        toggleUpdateExisting() {
                this.model._update_existing = !this.model._update_existing;
        },

        clearState(){
            this.model._csv = null;

            this.error = false;
            this.model.columnsChecked = [];
            this.csv_data = [];

            this._sample = null;

            this.current_file = '';
            this.map_selected = '';
        },
        _checkValid(){
            if (this.model.columnsChecked.length == 0){
                this.error = true;
                this.error_message = 'Mapping should not be empty';
                return false;
            }else{
                var isError = some(this.model.columnsChecked, function (val, i) {
                                var map_selected = val.map_selected || '';
                                return !map_selected;
                                });
                if (isError){
                    this.error = true;
                    this.error_message = 'Select map to field for a column';
                    return false;
                }
            }

            if (this.model._csv == null){
                this.error = true;
                this.error_message = 'Mapping error';
                return false;
            }

            this.error = false;
            return true;
        },
        handleSelectionChange(val) {
            this.model.columnsChecked = val;
        },
        validate () {
            var isValid = this._checkValid();
            
            if (!isValid){
                return false;
            }


            this.$emit('on-validated', 'fields_mapped', isValid, this.model);
            return isValid;
        },

        /* CSV file loading methods */
        _load(file) {
            const _this = this;
            this._readFile(file, (output) => {
                _this._sample = get(Papa.parse(output, { preview: 2, skipEmptyLines: true }), "data");
                _this.model._csv = get(Papa.parse(output, { skipEmptyLines: true }), "data");
                
                var _headers = _this._sample[0];
                forEach(_headers, function(val, i) {
                    _this.csv_data.push({
                        'header' : _this._sample[0][i],
                        'sample_data': _this._sample[1][i]
                    })
                })
            });
        },
        _readFile(file, callback) {
                if (file) {
                    let reader = new FileReader();
                    reader.readAsText(file, "UTF-8");
                    reader.onload = function (evt) {
                        callback(evt.target.result);
                    };
                    reader.onerror = function () {
                        this.error = true;
                        this.error_message = 'File reading error';
                    };
                }
        },
    }
}
</script>
<style>
.second-step {
    width: 100%;
    margin: 10px, 10px, 10px, 10px;
    overflow: auto;
}
.container {
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding: 10px 20px;
}
.red {
    color: red;
}
</style>
