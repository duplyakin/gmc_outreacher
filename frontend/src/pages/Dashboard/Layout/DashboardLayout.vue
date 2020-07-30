<template>
  <div>
    <div>
      <el-menu router="router" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item @click="$router.push('/dashboard')" style="margin-top: 10px;"><img class="o24_menu" src="../../../../public/static/img/Fav1.png"></el-menu-item>
        
        <el-menu-item index="/dashboard" style="margin-top: 20px;"><p class="o24_menu">Dashboard</p></el-menu-item>
        <el-menu-item index="/campaigns" style="margin-top: 20px;"><p class="o24_menu">Campaigns</p></el-menu-item>
        <el-menu-item index="/prospects" style="margin-top: 20px;"><p class="o24_menu">Leads</p></el-menu-item>
        <el-menu-item index="/accounts" style="margin-top: 20px;"><p class="o24_menu">Accounts</p></el-menu-item>
        <el-menu-item index="/videos" style="margin-top: 20px;"><p class="o24_menu">Videos</p></el-menu-item>

        <el-menu-item index="/prospects_list" style="margin-top: 20px;"><p class="o24_menu">Leads lists</p></el-menu-item>
        <el-menu-item index="/blacklist" style="margin-top: 20px;"><p class="o24_menu">Blacklist</p></el-menu-item>
        <el-menu-item index="/subscription" style="margin-top: 20px;"><p class="o24_menu">Subscription</p></el-menu-item>

        <el-submenu index="settings" style="margin-top: 20px;">
          <template slot="title">Settings</template>
          <el-menu-item index="/prospects_list"><p class="o24_menu">Leads lists</p></el-menu-item>
          <el-menu-item index="/blacklist"><p class="o24_menu">Blacklist</p></el-menu-item>
          <el-menu-item index="/subscription"><p class="o24_menu">Subscription</p></el-menu-item>
        </el-submenu>

        <el-submenu index="admin" style="margin-top: 20px;" v-if="role==='admin'">
          <template slot="title">Admin pannel</template>
          <el-menu-item index="/admin/users_list"><p class="o24_menu">Users list</p></el-menu-item>
          <el-menu-item index="/admin/google_app_settings"><p class="o24_menu">Google App Settings</p></el-menu-item>
          <el-menu-item index="/admin/limits"><p class="o24_menu">Limits</p></el-menu-item>
        </el-submenu>

      </el-menu>
    </div>

    <div class="mx-4 my-4">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>
import { Menu, Submenu, MenuItem, MenuItemGroup } from "element-ui";



  export default {
    components: {
      [Menu.name]: Menu,
      [Submenu.name]: Submenu,
      [MenuItem.name]: MenuItem,
      [MenuItemGroup.name]: MenuItemGroup,
    },
  data() {
    return {
      role: '',
      
      router: true,
      activeIndex: '/dashboard'
    }
  },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },

    },
    mounted() {
      this.role = localStorage.getItem('role');
    }
  }

</script>
<style>
body, html {
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100%;
}
body {
  background-color: rgb(245, 245, 245);
}
.o24_menu {
  color: #262a79; 
  line-height: 50px;
  font-size: 14px;
}
</style>