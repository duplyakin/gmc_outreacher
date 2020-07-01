<template>
  <div class="wrapper" :class="{'nav-open': $sidebar.showSidebar}">
    <notifications></notifications>
    <side-bar>
      <mobile-menu></mobile-menu>
      <template slot-scope="props" slot="links">

        <sidebar-item :link="{name: 'Dashboard', icon: 'nc-icon nc-air-baloon', path: '/dashboard'}"></sidebar-item>
        
        <sidebar-item :link="{name: 'Leads managment', icon: 'nc-icon nc-bag', path: '/linkedin_enrichment'}"></sidebar-item>
        <sidebar-item :link="{name: 'Campaigns', icon: 'nc-icon nc-bullet-list-67', path: '/campaigns'}"></sidebar-item>
        <sidebar-item :link="{name: 'Leads', icon: 'nc-icon nc-layers-3', path: '/prospects'}"></sidebar-item>
        <sidebar-item :link="{name: 'Accounts', icon: 'nc-icon nc-single-02', path: '/accounts'}"></sidebar-item>
        <sidebar-item :link="{name: 'Settings', icon: 'nc-icon nc-notes'}">
          <sidebar-item :link="{name: 'Profile', icon: 'nc-icon nc-circle-09', path: '/profile'}"></sidebar-item>
          <sidebar-item :link="{name: 'Leads Lists', icon: 'nc-icon nc-single-copy-04', path: '/prospects_list'}"></sidebar-item>
          <sidebar-item :link="{name: 'Blacklist', icon: 'nc-icon nc-circle-09', path: '/blacklist'}"></sidebar-item>
          <sidebar-item :link="{name: 'Subscription', icon: 'nc-icon nc-circle-09', path: '/subscription'}"></sidebar-item>

        </sidebar-item>

        <div v-if="role==='admin'">
          <sidebar-item :link="{name: 'Statistics', icon: 'nc-icon nc-chart-bar-32', path: '/statistics'}"></sidebar-item>
          <sidebar-item :link="{name: 'Actions', icon: 'nc-icon nc-tag-content', path: '/admin/actions'}"></sidebar-item>

          <sidebar-item :link="{name: 'Admin', icon: 'nc-icon nc-notes'}">
            <sidebar-item :link="{name: 'Users list', path: '/admin/users_list'}"></sidebar-item>
            <sidebar-item :link="{name: 'Google App Settings', path: '/admin/google_app_settings'}"></sidebar-item>
            <sidebar-item :link="{name: 'Limits', path: '/admin/limits'}"></sidebar-item>
          </sidebar-item>

      </div>
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar">

      </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<script>
  const TopNavbar = () => import('./TopNavbar.vue')
  const ContentFooter = () => import('./ContentFooter.vue')
  const DashboardContent = () => import('./Content.vue')
  const MobileMenu = () => import('./Extra/MobileMenu.vue')

  export default {
    components: {
      TopNavbar,
      ContentFooter,
      DashboardContent,
      MobileMenu,
    },
  data() {
    return {
      role: ''
    }
  },
    methods: {
      toggleSidebar () {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(false)
        }
      }
    },
    mounted() {
      this.role = localStorage.getItem('role');
      //console.log('role: ', this.role);
    }
  }

</script>
