<template>
<div>
    <button type="submit" @click.prevent="onLogout" class="btn btn-fill btn-info btn-round btn-wd ">Logout</button>

</div>
</template>
<script>
export default {
components: {
},
computed: {
},
data () {     
    return {
    }
},
methods: {
    onLogout(){
        this.$store.dispatch('auth/logout').then(() => {
                        this.$router.push('/admin');
		});
    }
},
mounted () {
},
created() {

},
}
</script>
<style>
</style>
