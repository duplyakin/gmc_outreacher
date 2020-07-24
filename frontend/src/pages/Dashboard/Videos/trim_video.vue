<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <el-upload
                    action=""
                    :multiple="false" 
                    :limit="1"
                    :auto-upload = "false"
        
                    :http-request="addFile"
                    :before-remove="beforeRemove"
                    :before-upload="beforeFileUpload"
                    :on-change="onChangeFile"
        
                    accept=".mp4"
                    class="el-upload">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text"><em>Upload video</em></div>
                    <div class="el-upload__tip" slot="tip">
                            Only mp4 accepted
                            <br>
                            [Maximum Upload File Size: 30MB]
                            <br>
                            {{this.video_file}}
                    </div>
                </el-upload> 
    
            </div>

            <div>
                <video v-on:loadeddata="onVideoChange" ref="trim-video-element" width="650" height="320" controls :disabled="disabled">
                </video> 
            </div>
            <div>
                <p>Select video fragment for personalization</p>
            </div>
            <div>
                <el-slider
                    v-model="trim_range"
                    :max="video_length"
                    width="650"
                    range
                    :disabled="disabled">
                </el-slider>
            </div>
            
            <div>
                <p>Selected fragment</p>
                <p>{{this.trim_range[0]}}...{{this.trim_range[1]}}</p>
            </div>

            <div>
                <el-button v-on:click="playSelected" type="primary" :disabled="disabled">Play Fragment</el-button>
            </div>
            
        
            <div>
                <el-button v-on:click="nextStep" type="error">Test Next (FOR TEST ONLY)</el-button>
            </div>

            </div>
      </card>
    </div>  
</template>

<script>
import { Slider, Button, Upload } from 'element-ui'

export default {
components: {
    [Slider.name] : Slider,
    [Button.name] : Button,
    [Upload.name] : Upload
},
data() {
    return {
        trim_range: [0, 5],
        video_length: 60,
        video_file: '',
        disabled: true,
        maximum_size: 30, //Mb
        allowed_type: 'video/mp4'
    };
},
watch: {
    trim_range: function (newValue, oldValue) {
        if (newValue[0] != oldValue[0]){
            this.$refs['trim-video-element'].currentTime = newValue[0];
        }else if (newValue[1] != oldValue[1]){
            this.$refs['trim-video-element'].currentTime = newValue[1];
        }
    }
},
methods: {
    nextStep(){
        this.$router.push({ path: "personalize_video" });
    },
    checkTime() {
        var video = this.$refs['trim-video-element'];
        var endTime = this.trim_range[1];

        if (video.currentTime >= endTime) {
           video.pause();
        } else {
           setTimeout(this.checkTime, 100);
        }
    },
    playSelected(){
        var video = this.$refs['trim-video-element'];
        if (!video){
            alert("Please upload the video first");
            return;
        }

        video.currentTime = this.trim_range[0];
        video.play();
        this.checkTime();
    },

    handleExceed(files, fileList){
    },
    addFile(files, fileList){
    },
    beforeFileUpload(file){
    },
    beforeRemove(file, fileList){
        fileList.pop();

        // Update dynamic
        this.video_file = '';

        this.video_length = 60;
    },
    _checkVideo(video){
        var duration = video.duration;
        if (duration <= 0 || duration >= 91){
            return false;
        }

        return true;
    },
    onVideoChange(obj){
        var video = this.$refs['trim-video-element'];
        if (!video || !video.duration){
            return;
        }

        var isValid = this._checkVideo(video);
        if (!isValid){
            this.disabled = true;
            video.src = "";

            var error = "Wrong video: 90 seconds maximum allowed"            
            alert(error);
            return;
        }

        this.disabled = false;

        // Update dynamic
        this.video_length = video.duration + 1;

        this.$set(this.trim_range, 0, 0);
        this.$set(this.trim_range, 1, 5);

        video.currentTime = 0;
        video.pause();
    },
    _checkFile(file){
        console.log(file);
        var raw = file.raw;
        if (!raw){
            return false;
        }

        var size = raw.size;
        if (size <= 0){
            return false;
        }

        var mb_size = size / 1024 / 1024;
        if (mb_size >= this.maximum_size){
            return false;
        }

        var file_type = raw.type;
        if (!file_type || file_type != this.allowed_type){
            return false;
        }

        return true;
    },
    onChangeFile(file, fileList){
        var video = this.$refs['trim-video-element'];

        fileList.pop();

        var isValid = this._checkFile(file);
        if (!isValid){
            this.disabled = true;
            video.src = "";
            
            var error = "Wrong video: .mp4 up to 30Mb allowed only"            
            alert(error);
            return;
        }

        this.disabled = false;
        this.video_file = file.name;

        var fileUrl = URL.createObjectURL(file.raw);
        video.src = fileUrl;
    },

},
async mounted() {

},
created() {

}
};
</script>