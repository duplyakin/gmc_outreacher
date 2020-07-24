<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <p>You are 1 step before finish.</p>
            </div>

            <div>
                <img src="https://blog.hubspot.com/hs-fs/hub/53/file-1528401713-gif/lebowski.gif" />
            </div>
            <div>
                <p>To use this video in your campaigns just add the next tag to your template.</p>
            </div>
            <div>
                <p>{VIDEO_123}</p>
            </div>
            <div>
                <a href="">View landing page for random lead</a>
            </div>

            <div>
                <el-button type="primary">Save Draft</el-button>
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