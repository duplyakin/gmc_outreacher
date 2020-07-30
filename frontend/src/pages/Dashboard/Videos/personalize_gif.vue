<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <p>Customize the gif that will be inserted to email.</p>
            </div>

            <div class="parent">
                <img style="width:650px; height:340px;" src="static/img/email_template.png" />
                <div class="inner">
                    <img style="width:200px; height:100px;" src="https://media.giphy.com/media/h4x0izlol88ZWrsYtC/giphy.gif"/>
                    <div v-if="checked" class="inner-badge">
                        <img style="width:200px; height:15px;" src="static/img/gif_cover.png"/>
                    </div>
            
                </div>
            </div>
            <div>
                <el-checkbox v-model="checked">Add emulation video bar</el-checkbox>
            </div>
            <div>
                <el-button v-on:click="nextStep" type="error">Test Next (FOR TEST ONLY)</el-button>
            </div>

            </div>
      </card>
    </div>  
</template>

<script>
import { Input, Button, Checkbox } from 'element-ui'

export default {
components: {
    [Button.name] : Button,
    [Input.name] : Input,
    [Checkbox.name] : Checkbox

},
data() {
    return {
        checked: false,
    };
},
methods: {
    nextStep(){
        this.$router.push({ path: "personalize_lp" });

    },
    playPersonal(){
        /* 
        Call to o24 backend to receive audio
        */
    },
},
async mounted() {

},
created() {

}
};
</script>
<style>
.parent{
    width:650px;
    height:340px;
    position:relative;
    z-index:0;
}

.inner{
    position:absolute;
    z-index:1;
    bottom:120px;
    right:420px;
}
.inner-badge{
    position:absolute;
    z-index:2;
    bottom:20px;
    right:0;
}

</style>