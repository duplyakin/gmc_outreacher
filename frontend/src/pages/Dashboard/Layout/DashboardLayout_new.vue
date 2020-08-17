<template>
  <div>
    <div>
      <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #ffffff;">
        <div class="container">
        <a class="navbar-brand" href="#">
          <img src="../../../../public/static/img/Fav1.png" width="30" height="30" class="d-inline-block align-top" alt="">
        </a>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto mt-3">

            <li class="nav-item">
              <a class="nav-link" href="/dashboard"><p class="o24_menu">Dashboard</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/campaigns"><p class="o24_menu">Campaigns</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/prospects"><p class="o24_menu">Leads</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/accounts"><p class="o24_menu">Accounts</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/videos"><p class="o24_menu">Videos</p></a>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="/prospects_list"><p class="o24_menu">Leads lists</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/blacklist"><p class="o24_menu">Blacklist</p></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/subscription"><p class="o24_menu">Subscription</p></a>
            </li>


          </ul>
          

        </div>
        </div>
      </nav>
    </div>
    

    <div class="mx-4 my-4">
      <router-view></router-view>
    </div>

    <div>
      <nav class="navbar navbar-light fixed-bottom" style="background-color: #ffffff;">
        <!-- Navbar content -->
      </nav>
    </div>

  </div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway';
  export default {
    components: {
    },
    props: ['id'],
  mixins: [ clickaway ],
  data() {
    return {
      role: '',
      isDropdownActive: false,
    }
  },
    methods: {
away() {
      this.isDropdownActive = false;
    }

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