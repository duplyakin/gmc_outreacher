<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <p>Enter the phrase that will be cloning with your voice.</p>
            </div>
            <div>
                <el-input
                    type="textarea"
                    :rows="2"
                    width="650"
                    placeholder="Hi {first_name}! Just view your {company} website. Do you want to meet online or in person?"
                    v-model="phrase">
              </el-input>
            </div>
            
            <div>
                <el-button v-on:click="playPersonal" type="primary">Check The Voice</el-button>
            </div>

            <div>
                <video v-on:loadeddata="onVideoChange" ref="trim-video-element" width="650" height="320" controls>
                </video> 
            </div>            
        
            <div>
                <el-button v-on:click="nextStep" type="error">Test Next (FOR TEST ONLY)</el-button>
            </div>

            </div>
      </card>
    </div>  
</template>

<script>
import { Input, Button } from 'element-ui'

export default {
components: {
    [Button.name] : Button,
    [Input.name] : Input
},
data() {
    return {
        phrase: "",
    };
},
methods: {
    nextStep(){
        this.$router.push({ path: "personalize_gif" });

    },
    playPersonal(){
        /* 
        Call to o24 backend to receive audio
        */
    },
    onVideoChange(){
        
    }
},
async mounted() {

},
created() {

}
};
</script>