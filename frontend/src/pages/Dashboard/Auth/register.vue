<template>
  <auth-layout pageClass="login-page">
    <div class="row d-flex justify-content-center align-items-center">
      <div class="col-lg-4 col-md-6 col-sm-8">
        <form method="#" action="#">
          <!--You can specify transitions on initial render. The `card-hidden` class will be present initially and then it will be removed-->
          <card>
            <div slot="header">
              <h3 class="card-title text-center">Register</h3>
            </div>

            <pulse-loader :loading="loading" :color="color"></pulse-loader>

            <div v-if="!loading">
              <fg-input
                label="Email address"
                placeholder="Enter email"
                type="email"
                v-model="model.email"
              ></fg-input>
              <fg-input
                label="passsword"
                type="password"
                placeholder="Password"
                v-model="model.password"
              ></fg-input>
              <fg-input
                label="repeat password"
                type="password"
                placeholder="Password"
                v-model="model.repeat_password"
              ></fg-input>
              <fg-input
                label="invite code"
                type="text"
                placeholder="Invite code"
                v-model="model.invite_code"
              ></fg-input>
              <div v-if="error" class="form-group">
                <small class="text-danger">{{ error }}</small>
              </div>
            </div>
            <div class="text-center">
              <button
                type="submit"
                @click.prevent="onSubmit"
                class="btn btn-fill btn-info btn-round btn-wd"
              >Create Free Account</button>
              <br />
            </div>

          </card>
        </form>
      </div>
    </div>
  </auth-layout>
</template>
<script>
import {
  Checkbox as LCheckbox,
  FadeRenderTransition
} from "src/components/index";
import { PulseLoader } from "vue-spinner/dist/vue-spinner.min.js";

const AuthLayout = () => import('./AuthLayout.vue')

import { mapGetters } from "vuex";

export default {
  components: {
    PulseLoader,
    LCheckbox,
    FadeRenderTransition,
    AuthLayout
  },
  computed: {
    ...mapGetters("auth", {
      // map `this.doneCount` to `this.$store.getters.doneTodosCount`
      error: "getRegisterError",
      isAuth: "isAuthenticated"
    }),
  },

  data() {
    return {
      loading: false,
      color: "#a7a7ff",

      model: {
        email: "",
        password: "",
        repeat_password: "",
        invite_code: ""
      }
    };
  },
  methods: {
    toggleNavbar() {
      document.body.classList.toggle("nav-open");
    },
    closeMenu() {
      document.body.classList.remove("nav-open");
      document.body.classList.remove("off-canvas-sidebar");
    },
    async onSubmit() {
      var _this = this
      this.loading = true

      await this.$store.dispatch("auth/register", this.model).then(
          resolve => {
            _this.$router.push("profile")
            _this.loading = false
          },
          reject => {
            console.log("error here: ", reject)
            _this.loading = false
          }
        )
        .catch(err => {
          console.error("register error: ", err)
          _this.loading = false
        })
    },
  },
  beforeDestroy() {
    this.closeMenu();
  }
};
</script>
<style>
.navbar-nav .nav-item p {
  line-height: inherit;
  margin-left: 5px;
}
</style>
