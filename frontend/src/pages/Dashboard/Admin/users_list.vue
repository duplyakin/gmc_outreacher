<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <h3>
            <i class="nc-icon"></i>Users
          </h3>
        </div>
      </div>
    </card>

    <card>
      <div class="col-12">
        <el-table
          stripe
          ref="users_data_table"
          style="width: 100%;"
          :data="list_data.users"
          max-height="500"
          border
        >
          <el-table-column
            v-for="(column,index) in list_data.columns"
            :key="index"
            :prop="column.prop"
            :label="column.label"
            :fixed="column.prop === 'email' ? true : false"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <a
                @click.prevent="editUser(scope.row, scope.$index)"
                href="#"
                v-if="column.prop === 'email'"
              >{{ scope.row[column.prop] }}</a>
              <template v-else-if="column.prop === 'status'">{{ status[scope.row[column.prop]] }}</template>
              <template v-else>{{ show_data(scope.row, column) }}</template>
            </template>
          </el-table-column>
        </el-table>
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

const USERS_API_LIST = "/admin/users/list";

const UserEdit = () => import("./user_edit_modal.vue");

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
        users: [],
        roles: []
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
    editUser(userObj, index) {
      var table = this.$refs["users_data_table"];
      this.$modal.show(
        UserEdit,
        {
          userObj: userObj,
          roles: this.list_data.roles,
          valueUpdated: newValue => {
            this.$set(this.list_data.users, index, newValue);
            table.$forceUpdate();
          }
        },
        {
          width: "400",
          height: "auto",
          scrollable: true
        }
      );
    },
    load_users() {
      const path = USERS_API_LIST;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading users data." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            //console.log(r)
            this.deserialize_users(r);
          }
        })
        .catch(error => {
          var msg = "Error loading data. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_users(from_data) {
      if (from_data.columns) {
        var columns = JSON.parse(from_data.columns);
        this.$set(this.list_data, "columns", columns);
      }

      if (from_data.users) {
        var users = JSON.parse(from_data.users);
        this.$set(this.list_data, "users", users);
      }

      if (from_data.roles) {
        var roles = from_data.roles;
        this.$set(this.list_data, "roles", roles);
      }
    }
  },
  async mounted() {
    await this.load_users();
    console.log('roles: ', this.list_data)
  }
};
</script>
<style>
</style>
