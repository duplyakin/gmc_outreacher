<template>
  <div class="test-modal">
    <card title="Change password form">

        <div class="row mb-3">
          <div class="col-12">
            <label>Old password</label>
            <el-input
                placeholder="Enter Old Password"
                rows="1"
                name="Password_old"
                v-model="password_old"
                show-password>
            </el-input>
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-12">
            <label>New password</label>
            <el-input
                placeholder="Enter New Password"
                rows="1"
                name="Password_new"
                v-model="password_new"
                show-password>
            </el-input>
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-12">
            <label>Repeat new password</label>
            <el-input
                placeholder="Enter New Password"
                rows="1"
                name="Password_new_repeat"
                v-model="password_new_repeat"
                show-password>
            </el-input>
          </div>
        </div>


        <div class="col-12 d-flex flex-row-reverse">
          <button
            type="submit"
            v-on:click="submit"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Save</button>
          <button
            v-on:click="discard"
            type="discard"
            class="btn btn-outline btn-wd btn-danger"
          >Discard</button>
        </div>

    </card>
  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";

import axios from "@/api/axios-auth";

const CHANGE_PASSWORD_API = "/change/password";


export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
  },
  data() {
    return {
        password_old: null,
        password_new_repeat: null,
        password_new: null,
    };
  },
  methods: {
    change_password() {
      const path = CHANGE_PASSWORD_API;

      var data = new FormData();
      data.append("_old_password", this.password_old);
      data.append("_new_password", this.password_new);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error updating user password." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            Notification.success({title: "Success", message: "User password changed"});
            this.$emit("close");
          }
        })
        .catch(error => {
          var msg = "Error updating user password. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    submit() {
      if(this.password_new && this.password_new_repeat &&  this.password_old) {
          if(this.password_new.toString().lengh < 8 || this.password_new_repeat.toString().lengh < 8 || this.password_old.toString().lengh < 8 ) {
            Notification.error({title: "Error", message: "Short password"});
            return;
          } else if (this.password_new !== this.password_new_repeat) {
            Notification.error({title: "Error", message: "Repeated password - different"});
            return;
          } else {
              this.change_password();
          }
      } else {
          Notification.error({title: "Error", message: "Passwords can\'t be empty"});
      }
      
      //this.$emit("close");
    },
    discard() {
      this.$emit("close");
    }
  },
  mounted() {
      
  }
};
</script>
<style>

</style>
  