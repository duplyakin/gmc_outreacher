<template>
<b-container fluid>
    <b-navbar toggleable="md" type="light" variant="light">
        <b-navbar-brand href="#">O24</b-navbar-brand>
    
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="#">Dashboard</b-nav-item>
            <b-nav-item href="#">Campaigns</b-nav-item>
            <b-nav-item href="#">Leads</b-nav-item>
            <b-nav-item href="#">Accounts</b-nav-item>
            <b-nav-item href="#">Videos</b-nav-item>  
          </b-navbar-nav>
    
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">    
            <b-nav-item-dropdown text="Settings" right>
                <b-dropdown-item href="#">Lists</b-dropdown-item>
                <b-dropdown-item href="#">Black List</b-dropdown-item>
                <b-dropdown-item href="#">Billing</b-dropdown-item>
            </b-nav-item-dropdown>
    
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
</b-container>
</template>
<script>

</script>
