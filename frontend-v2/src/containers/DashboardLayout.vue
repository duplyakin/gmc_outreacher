<template>
  <div>
    <div>
      <b-navbar toggleable="md" type="light" style="background-color: #ffffff;">
        <b-navbar-brand href="#"><img src="./Fav1.png" width="50" height="50" alt=""></b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="/dashboard">Dashboard</b-nav-item>
            <b-nav-item href="/campaigns">Campaigns</b-nav-item>
            <b-nav-item href="/prospects">Leads</b-nav-item>
            <b-nav-item href="/accounts">Accounts</b-nav-item>
            <b-nav-item href="/videos">Videos</b-nav-item>  
          </b-navbar-nav>
    
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">    
            <b-nav-item-dropdown text="Settings" right>
                <b-dropdown-item href="/prospects_list">Lists</b-dropdown-item>
                <b-dropdown-item href="/blacklist">Black List</b-dropdown-item>
                <b-dropdown-item href="/subscription">Billing</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <div class="mx-4 my-4">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>

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
</style>