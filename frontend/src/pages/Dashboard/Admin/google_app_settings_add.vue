<template>
  <div>
    <card title="Google App Settings - Create">
        <div>
            <button
                @click.prevent="uploadCredentials"
                type="button"
                class="btn btn-default btn-success mx-1"
            >Upload Credentials</button>
        </div>

      <div>

        <div class="col-12" v-for="column in columns">
        <p>{{ column.label }}</p>
        <fg-input>
              <textarea
                class="form-control"
                placeholder="Enter new value"
                rows="1"
                v-model="current_settings[column.prop]"
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
      <div class="col-12">{{ this.columns }}</div>
    </div>

    </card>
  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";

import axios from "@/api/axios-auth";

const Upload = () => import('./upload_credentials.vue')

// add
const FIELDS_SETTINGS_API = "/admin/google/settings/fields";
const CREATE_SETTINGS_API = "/admin/google/settings/create";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
  },
  data() {
    return {
        columns: [],
        current_settings: {},
    };
  },
  methods: {
    create_settings() {
      const path = CREATE_SETTINGS_API;

      var data = new FormData();
      data.append("_data", JSON.stringify(this.current_settings));

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error create settings." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            Notification.success({title: "Success", message: "Settings created"});
          }
        })
        .catch(error => {
          var msg = "Error create settings. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    load_settings() {
      const path = FIELDS_SETTINGS_API;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading settings." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            //console.log(r)
            if(r.columns) {
              this.columns = JSON.parse(r.columns);
            }
          }
        })
        .catch(error => {
          var msg = "Error loading settings. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    uploadCredentials() {
      this.$modal.show(
        Upload,
        {
          valueUpdated: newValue => {
            this.$set(this.current_settings, 'credentials', newValue); // ? file format
          }
        },
        {
          width: "720",
          height: "auto",
          scrollable: true
        }
      );
    },
    submit() {
      this.create_settings();
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
  