<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <h3>
            <i class="nc-icon"></i>Google App Settings
          </h3>
        </div>
      </div>
    </card>

        <card>
        <div class="col-12" v-for="(value, key) in limits">
        <p>{{ key }}</p>
        <fg-input>
              <textarea
                class="form-control"
                placeholder="Enter new value"
                rows="1"
                v-model="limits[key]"
              ></textarea>
        </fg-input>
        </div>

        <div class="col-12 d-flex flex-row-reverse">
          <button
            type="submit"
            v-on:click="submit"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Save</button>
        </div>

    </card>

    <div v-if="test" class="row">
      <div class="col-12">{{ this.list_data }}</div>
    </div>
  </div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";

import axios from "@/api/axios-auth";

const LIMITS_API_LIST = "/admin/...";
const EDIT_LIMITS_API_LIST = "/admin/...";

export default {
  components: {
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {},
  data() {
    return {
      test: false,
      limits: {}
    };
  },
  methods: {
    editLimits() {
      
    },
    load_limits() {
      const path = LIMITS_API_LIST;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading limits." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
              //console.log(r)
            this.deserialize_limits(r);
          }
        })
        .catch(error => {
          var msg = "Error loading limits. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_limits(from_data) {
      if (from_data.limits) {
        this.limits = JSON.parse(from_data.limits);
      }
    },
    submit() {
      this.editLimits();
      console.log(this.limits);
    },
  },
  async mounted() {
    await this.load_limits();
  }
};
</script>
<style>
</style>
