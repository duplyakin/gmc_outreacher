<template>
<div>
    <h5 class="text-center">Upload .csv file with data</h5>
    <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
        {{ error_message }}
    </div>
    <div class="row">
    <div class="col-12 text-center">
            <el-upload
            action=""
            :multiple="false" 
            :limit="1"
            :on-exceed="handleExceed"
            :auto-upload = "false"
            :file-list="model.file_list"

            :http-request="addFile"
            :before-remove="beforeRemove"
            :before-upload="beforeFileUpload"
            :on-change="onChangeFile"

            accept=".csv"
            class="el-upload">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">
                    Your file must contain a column with header: email. The value of this column will be your prospects email address.
                    <br>
                    [Maximum Upload File Size: 5MB or 10,000 rows]
                    {{this.model.file}}
            </div>
            </el-upload> 
    </div>
    </div>
</div>
</template>
<script>
import { Upload } from 'element-ui'


export default {
    name : 'first-step',
    components: {
      [Upload.name] : Upload
    },
    data () {
        return {
            model : {
                file : {},
            },
            error : false,
            error_message : 'File required',
            max_size : 5*1024*1024,
            available_types : ["application/vnd.ms-excel", "text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
        }
    },
    methods: {
    handleExceed(files, fileList){
        alert('1 file at a time.');
    },
    addFile(files, fileList){
        alert("addFile");
    },
    beforeFileUpload(file){
        alert(file);
    },
    beforeRemove(file, fileList){
        if (confirm(`Remove file: ${ file.name } ?`)){
            this.model.file = {};
            fileList.pop();
            return true;
        }
        return false;
    },
    onChangeFile(file, fileList){
        var isValid = this._checkValid(file);

        if (!isValid){
            fileList.pop();
        }else{
            this.model.file = file;
        }
    },
    validate () {
        var isValid = this._checkValid(this.model.file);

        if (!isValid){
            return false;
        }

        this.$emit('on-validated', 'file_upload', isValid, this.model);

        return true;
    },
    _checkValid(file){
        
        if (Object.keys(file).length === 0){
            this.error_message = 'File required';
            this.error = true;
            return false;
        }

        var raw_file = file.raw;

        if (!(this.available_types.includes(raw_file.type))){
            this.error_message = 'Wrong file format - only csv allowed';
            this.error = true;
            return false;
        }

        if (raw_file.size > this.max_size){
            this.error_message = 'File size exceed: 5MB maxim';
            this.error = true;
            return false;
        }

        if (raw_file.size <= 0){
            this.error_message = 'File can not be empty';
            this.error = true;
            return false;
        }
        
        this.error_message = '';
        this.error = false;

        return true;
    }
    
    }
}
</script>
<style>
.el-icon-upload {
    font-size: 67px;
    color: #c0c4cc;
    margin: 40px 0 16px;
    line-height: 50px;
}
</style>
