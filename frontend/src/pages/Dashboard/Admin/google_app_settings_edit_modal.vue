<template>
  <div class="test-modal">
    <card title="Google App Settings - Edit">
      <div>

        <div class="col-12" v-for="(value, key) in current_settings">
        <p>{{ key }}</p>
        <fg-input>
              <textarea
                class="form-control"
                placeholder="Enter new value"
                rows="1"
                v-model="current_settings[key]"
              ></textarea>
        </fg-input>
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

      </div>

<div v-if="false" class="row">
      <div class="col-12">{{ this.current_settings }}</div>
    </div>

    </card>
  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";

import axios from "@/api/axios-auth";

// edit
const GET_SETTINGS_API = "/admin/google/settings/get";
const EDIT_SETTINGS_API = "/admin/google/settings/edit";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
  },
  props: {
    settingsId: String,
    valueUpdated: Function,
  },
  data() {
    return {
        current_settings: {},
    };
  },
  methods: {
    edit_settings() {
      const path = EDIT_SETTINGS_API;

      var data = new FormData();
      data.append("_settings_id", this.settingsId);
      data.append("_data", JSON.stringify(this.current_settings));

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error updating settings." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            Notification.success({title: "Success", message: "Settings changed"});
          }
        })
        .catch(error => {
          var msg = "Error updating settings. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    load_settings() {
      const path = GET_SETTINGS_API;

      var data = new FormData();
      data.append('_settings_id', this.settingsId);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading settings." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            //console.log(r)
            this.current_settings = r;
          }
        })
        .catch(error => {
          var msg = "Error loading settings. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    submit() {
      this.edit_settings();
      console.log(this.current_settings);
      this.$emit("close");
    },
    discard() {
      this.$emit("close");
    }
  },
  created() {
    this.load_settings();
  }
};
</script>
<style>

</style>
  