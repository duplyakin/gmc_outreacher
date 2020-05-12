<template>
<div>
    <button type="button" @click.prevent="onLogout" class="btn btn-fill btn-info btn-round btn-wd ">Logout</button>
    <button type="button" @click.prevent="loadUser" class="btn btn-fill btn-info btn-round btn-wd ">Load user</button>

    <pre>{{ user_data }}</pre>
</div>
</template>
<script>

import axios from '@/api/axios-auth';
import { Notification, Table, TableColumn, Select, Option } from "element-ui";

const PROFILE_API_LIST = 'http://127.0.0.1:5000/profile';

export default {
data () {     
    return {
        user_data : ''
    }
},
methods: {
    onLogout(){
        this.$store.dispatch('auth/logout').then(() => {
                        this.$router.push('/admin');
		});
    },
    loadUser(){
        const path = PROFILE_API_LIST;
    
        var data = new FormData();

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading user." + r.msg;
                Notification.error({title: "Error", message: msg});
            }else{
                this.user_data = JSON.parse(JSON.stringify(r.user))
            }
            })
            .catch((error) => {
                var msg = "Error loading lists. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
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
