<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <h3>
            <i class="nc-icon"></i>Google App Settings
          </h3>
        </div>

        <div class="col-8 d-flex flex-row-reverse align-self-center">
          <div>
              <button
                  @click.prevent="addSettings"
                  type="button"
                  class="btn btn-default btn-success mx-1"
              >Add Settings</button>
          </div>
        </div>
      </div>
    </card>

    <card>
      <div class="col-12">
        <el-table
          stripe
          ref="settings_data_table"
          style="width: 100%;"
          :data="list_data.google_settings"
          max-height="500"
          border
        >
          <el-table-column
            v-for="(column,index) in list_data.columns"
            :key="index"
            :prop="column.prop"
            :label="column.label"
            :fixed="column.prop === 'title' ? true : false"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <a
                @click.prevent="editSettings(scope.row, scope.$index)"
                href="#"
                v-if="column.prop === 'title'"
              >{{ scope.row[column.prop] }}</a>
              <template v-else-if="column.prop === 'title'">{{ status[scope.row[column.prop]] }}</template>
              <template v-else>{{ show_data(scope.row, column) }}</template>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </card>

    <div v-if="test" class="row">
      <div class="col-12">{{ this.list_data }}</div>
    </div>

    <modals-container/>
  </div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";

import axios from "@/api/axios-auth";

const GOOGLE_SETTINGS_API_LIST = "/admin/google/settings/list";

const SettingsEdit = () => import("./google_app_settings_edit_modal.vue");
//const SettingsAdd = () => import("./google_app_settings_add_modal.vue");

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
      pagination: {
        perPage: 0,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50],
        total: 0
      },
      list_data: {
        columns: [],
        google_settings: []
      }
    };
  },
  methods: {
    show_data(scope_row, column) {
      var data = column.data || "";
      if (data) {
        return scope_row.data[column.prop] || "";
      } else {
        var field = column.field || "";
        if (field) {
          return scope_row[column.prop][field] || "";
        } else {
          return scope_row[column.prop] || "";
        }
      }

      return "";
    },
    editSettings(settingsObj, index) {
      var table = this.$refs["settings_data_table"];
      this.$modal.show(
        SettingsEdit,
        {
          settingsId: settingsObj._id.$oid,
          type: 'edit',
          valueUpdated: newValue => {
            this.$set(this.list_data.settings, index, newValue);
            table.$forceUpdate();
          }
        },
        {
          width: "720",
          height: "auto",
          scrollable: true
        }
      );
    },
    addSettings() {
        this.$router.push('google_app_settings_add');
    },
    load_settings() {
      const path = GOOGLE_SETTINGS_API_LIST;

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
            this.deserialize_settings(r);
          }
        })
        .catch(error => {
          var msg = "Error loading settings. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_settings(from_data) {
      if (from_data.columns) {
        var columns = JSON.parse(from_data.columns);
        this.$set(this.list_data, "columns", columns);
      }

      if (from_data.google_settings) {
        var google_settings = JSON.parse(from_data.google_settings);
        this.$set(this.list_data, "google_settings", google_settings);
      }
    }
  },
  async mounted() {
    await this.load_settings();
  }
};
</script>
<style>
</style>
