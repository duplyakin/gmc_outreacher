<template>
    <div>
      <card>
        <div class="text-center container">
            <div>
                <i class="el-icon-video-camera-solid"></i>
                <h3>You don't have any videos yet</h3>
                <p class="text-secondary">Click here to create a new video.</p>
                <a href="#"><el-button type="primary" style="height: 70px; width: 257px;">Create Video</el-button></a>
            </div>
        </div>
      </card>
    </div>  
</template>

<script>
import axios from "@/api/axios-auth";
import { Notification, Select, Option } from "element-ui";

const Change_password_modal = () => import('./change_password_modal.vue')

const PROFILE_API_LIST = '/profile';

export default {
data() {
    return {
    user_data: {}
    };
},
methods: {
    change_password() {
    this.$modal.show(
        Change_password_modal,
        {
        valueUpdated: newValue => {
        }
        },
        {
        width: "400",
        height: "auto",
        scrollable: true
        }
    );
    },
    onLogout() {
    var _this = this;
    this.$store.dispatch("auth/logout").then(
        resolve => {
            _this.$router.push("login");
        },
        reject => {
            console.log("error here: ", reject);
        }
        )
        .catch(err => {
        console.error("login error: ", err);
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
            //console.log('user: ', this.user_data)
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
    //console.log(this.user_data)
},
created() {
}
};
</script>