<template>
  <div>
    <card>
      <div class="col-4 d-flex align-self-center">
        <h3>
          <i class="nc-icon nc-circle-09"></i> Profile
        </h3>
      </div>
      <card>
        <p class="info">E-mail</p>
        <p>{{ user_data.email }}</p>
        <div v-if="!user_data.roles">
          <p class="info">Roles</p>
          <p>{{ user_data.roles }}</p>
        </div>
        <p class="info">Bonus code for friends</p>
        <p>{{ user_data.invite_code }}</p>
      </card>

      <button
        type="button"
        @click.prevent="onLogout"
        class="btn btn-fill btn-info btn-round btn-wd"
      >Logout</button>
    </card>
  </div>
</template>
<script>
import axios from "@/api/axios-auth";
import { Notification, Table, TableColumn, Select, Option } from "element-ui";

const PROFILE_API_LIST = "http://127.0.0.1:5000/profile";

export default {
  data() {
    return {
      user_data: ""
    };
  },
  methods: {
    onLogout() {
      this.$store.dispatch("auth/logout").then(() => {
        this.$router.push("/admin");
      });
    },
    loadUser() {
      const path = PROFILE_API_LIST;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading user." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.user_data = JSON.parse(r.user);
          }
        })
        .catch(error => {
          var msg = "Error loading lists. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    }
  },
  async mounted() {
    await this.loadUser();
  },
  created() {
    //this.loadUser();
  }
};
</script>
<style>
.card_title {
  text-align: center;
  font-size: 35px;
  font-weight: 500;
}
.info {
  font-size: 20px;
  font-weight: 600;
  height: 10px;
}
</style>
