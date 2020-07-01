<template>
  <div class="account-login-modal">
    <card>
      <h3>Linkedin login</h3>

      <pulse-loader :loading="loading" :color="color"></pulse-loader>

      <div v-if="!loading">
        <div v-if="!checked">
          <div class="row justify-content-center mb-3">
            <div class="col-12">
              <label>Login</label>
              <el-input placeholder="Enter login" v-model="login" :disabled="loading"></el-input>
            </div>
          </div>

          <div class="row justify-content-center mb-3">
            <div class="col-12">
              <label>Password</label>
              <el-input
                placeholder="Enter password"
                v-model="password"
                show-password
                :disabled="loading"
              ></el-input>
            </div>
          </div>
        </div>

        <div v-if="checked">
          <div class="row justify-content-center mb-3">
            <div class="col-12">
              <label>li_at cookie
                <el-popover
                  placement="top-start"
                  title="How to get them?"
                  width="auto"
                  trigger="hover"
                  content="Download chrome extension, go to the Linkedin page with your login / password and extract li_at cookie and past it to the field below">
                  <el-button slot="reference" size="mini" icon="el-icon-question" circle></el-button>
                </el-popover>
                <a href="https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related"> Cookie extension download</a>
              </label>
              <el-input placeholder="Enter li_at cookie" v-model="li_at" :disabled="loading"></el-input>
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-6">
            <el-checkbox v-model="checked">Login with li_at cookie</el-checkbox>
          </div>
        </div>

        <div class="row">
          <div class="col-12 d-flex flex-row-reverse">
            <button
              :disabled="loading"
              v-on:click="addAccount"
              type="button"
              class="btn btn-outline btn-wd btn-success mx-1"
            >Login</button>
            <button
              :disabled="loading"
              v-on:click="discard"
              type="button"
              class="btn btn-outline btn-wd btn-danger"
            >Close</button>
          </div>
        </div>
      </div>
    </card>
  </div>
</template>

<script>
import { Checkbox, Popover, Notification, Button, Select, Option } from "element-ui";
import axios from "@/api/axios-auth";
import { PulseLoader } from "vue-spinner/dist/vue-spinner.min.js";

export default {
  components: {
    [Checkbox.name]: Checkbox,
    [Popover.name]: Popover,
    [Button.name]: Button,
    PulseLoader,
    [Select.name]: Select,
    [Option.name]: Option
  },
  props: {
    credentials_id: String,
    accountLoginBS: Function
  },
  data() {
    return {
      login: "",
      password: "",
      li_at: "",

      checked: false,

      loading: false,
      color: "#a7a7ff"
    };
  },
  methods: {
    async addAccount() {
      if (this.checked) {
        // login with li_at cookie
        if (!this.li_at) {
          Notification.error({ title: "Error", message: "Empty li_at cookie" });
          return;
        }

        this.loading = true;

        this.accountLoginBS(this.credentials_id, 'cookie', this.li_at);
      } else {
        // login with login / password
        if (!this.login) {
          Notification.error({ title: "Error", message: "Empty login" });
          return;
        }
        if (!this.password) {
          Notification.error({ title: "Error", message: "Empty password" });
          return;
        }

        this.loading = true;

        this.accountLoginBS(this.credentials_id, 'regular', this.login, this.password);
      }
    },
    discard() {
      this.$emit("close");
    }
  },
  mounted() {}
};
</script>
<style>
</style>
    