<template>
<div>
    <card>
    <h5 class="text-center">Upload .json file with data</h5>
    <div v-if="error" class="text-center text-danger invalid-feedback" style="display: block;">
        {{ error_message }}
    </div>
    <div class="row text-center">
    <div class="col-12">
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
                    Your file must contain something with credentials
                    <br>
                    [Maximum Upload File Size: 5MB or 10,000 rows]
                    {{this.model.file}}
            </div>
            </el-upload> 
    </div>
    </div>
    
    </card>

    <div class="col-12 d-flex flex-row-reverse">
          <button
            type="submit"
            v-on:click="submit"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Save</button>
          <button
            v-on:click="discard"
            type="discard"
            class="btn btn-outline btn-wd btn-danger"
          >Discard</button>
        </div>
</div>
</template>
<script>
import { Notification, Upload } from 'element-ui'

export default {
    components: {
      [Upload.name] : Upload
    },
    props: {
        valueUpdated: Function,
    },
    data () {
        return {
            model : {
                file : {},
            },
            error : false,
            error_message : 'File required',
            max_size : 5*1024*1024,
            available_types : ["application/json", "application/txt"]
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

        if(!isValid) {
            fileList.pop();
        } else {
            this.model.file = file;
        }
    },
    _checkValid(file){
        
        if (Object.keys(file).length === 0){
            this.error_message = 'File required';
            this.error = true;
            return false;
        }

        var raw_file = file.raw;

        if (!(this.available_types.includes(raw_file.type))){
            this.error_message = 'Wrong file format - only json allowed';
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
    },
    submit() {
      var isValid = this._checkValid(this.model.file);

      if (!isValid) {
          Notification.error({ title: "Error", message: this.error_message });
          return;
      }

      this.valueUpdated(this.model.file);
      Notification.success({ title: "Success", message: 'File credentials uploaded' });  
      this.$emit("close");
    },
    discard() {
      this.$emit("close");
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
