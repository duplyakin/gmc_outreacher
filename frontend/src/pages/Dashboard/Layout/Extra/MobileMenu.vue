<template>
  <ul class="nav nav-mobile-menu">

    <drop-down>
      <template slot="title">
        <i class="nc-icon nc-bullet-list-67"></i>
      </template>
      <a class="dropdown-item" href="#">
        <i class="nc-icon nc-umbrella-13"></i> Help Center
      </a>
      <a class="dropdown-item" href="#">
        <i class="nc-icon nc-email-85"></i> Messages
      </a><a class="dropdown-item" href="#">
      <i class="nc-icon nc-settings-90"></i> Settings
    </a>
      <div class="divider"></div>
      <a class="dropdown-item" href="#">
        <i class="nc-icon nc-lock-circle-open"></i> Lock Screen
      </a>
      <a href="#" class="dropdown-item text-danger">
        <i class="nc-icon nc-button-power"></i> Log out
      </a>
    </drop-down>
  </ul>
</template>
<script>
  const DropDown = () => import('src/components/Dropdown.vue')

  export default {
    components: {
      DropDown
    }
  }
</script>
<style>
</style>
