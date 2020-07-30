<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <el-upload
                    action=""
                    :multiple="false" 
                    :limit="1"
                    :on-exceed="handleExceed"
                    :auto-upload = "false"
        
                    :http-request="addFile"
                    :before-remove="beforeRemove"
                    :before-upload="beforeFileUpload"
                    :on-change="onChangeFile"
        
                    accept=".mp4"
                    class="el-upload">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text"><em>click to upload</em></div>
                    <div class="el-upload__tip" slot="tip">
                            Only mp4 accepted
                            <br>
                            [Maximum Upload File Size: 10MB]
                            {{this.model.file}}
                    </div>
                </el-upload> 
    
            </div>
        </div>
      </card>
    </div>  
</template>

<script>
import { Upload } from 'element-ui'

export default {
components: {
    [Upload.name] : Upload
},
data() {
    return {
        model: {
            file: ''
        }
    };
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

    loadUser() {

    }
},
async mounted() {

},
created() {

}
};
</script>