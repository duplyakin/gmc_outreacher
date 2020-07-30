<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <p>Customize your landing page.</p>
            </div>

            <div>
                <img src="static/img/lp_template.png" />
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
        this.$router.push({ path: "personalize_preview" });

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