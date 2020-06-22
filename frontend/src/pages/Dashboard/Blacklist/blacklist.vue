<template>
  <div>
    <card>
      <div class="container">
        <div class="row">
          <div class="col-6 d-flex align-self-center">
            <h3>
              <i class="nc-icon nc-single-copy-04"></i> Do Not Contact list
            </h3>
          </div>
          <div class="col-6 d-flex flex-row-reverse align-self-center">
            <div>
              <button
                @click.prevent="add_data"
                type="button"
                class="btn btn-default btn-success mx-1"
              >Add</button>

              <button
                @click.prevent="load_list"
                type="button"
                class="btn btn-default btn-danger mx-1"
              >Delete</button>
            </div>
          </div>
        </div>
      </div>

      <card class="grey">
        <p>Add Domains, Emails or Linkedin accounts that you don't want to contact in the future from any campaign.</p>
      </card>
    </card>

    <card>
      <div class="col-12">
        <el-table
          stripe
          ref="lists_table"
          style="width: 100%;"
          :data="list_data.lists"
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
          ></el-table-column>
        </el-table>
      </div>
    </card>

    <div v-if="test" class="row">
      <div class="col-12">
        <pre>{{ this.list_data}}</pre>
      </div>
    </div>

    <modals-container />
  </div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";

import axios from "@/api/axios-auth";

const ListForm = () => import("./blacklist_add_modal.vue");

const LIST_API_LIST = "/blacklist/list";
const LIST_API_ADD = "/blacklist/add";
const LIST_API_DELETE = "/blacklist/remove";

export default {
  components: {
    ListForm,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {},
  data() {
    return {
      test: true,
      list_data: {
        columns: [],
        lists: []
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

    delete(list_id, row_index) {
      if (confirm("Are you sure?")) {
        const path = LIST_API_DELETE;

        var data = new FormData();
        data.append("_list_id", list_id);

        const index = row_index;
        axios
          .post(path, data)
          .then(res => {
            var r = res.data;
            if (r.code <= 0) {
              var msg = "Error deleting list " + r.msg;
              Notification.error({ title: "Error", message: msg });
            } else {
              this.load_list();
            }
          })
          .catch(error => {
            var msg = "Error deleting list " + error;
            Notification.error({ title: "Error", message: msg });
          });
      }
    },

    add_data() {
      this.$modal.show(
        ListForm,
        {
          api_url: LIST_API_ADD,
          valueUpdated: () => {
            Notification.success({ title: "Success", message: "List created" });
            this.load_list();
          }
        },
        {
          width: "720",
          height: "auto",
          scrollable: true
        }
      );
    },

    load_list() {
      const path = LIST_API_LIST;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          console.log(res);
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading blacklist." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.deserialize_list(r);
          }
        })
        .catch(error => {
          var msg = "Error loading blacklist. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_list(from_data) {
      if (from_data.columns != null) {
        var columns = JSON.parse(from_data.columns);
        this.$set(this.list_data, "columns", columns);
      }

      if (from_data.lists != null) {
        var lists = JSON.parse(from_data.lists);
        this.$set(this.list_data, "lists", lists);
      }
    }
  },
  mounted() {
    this.load_list();
  }
};
</script>
<style>
.grey {
  background-color: rgb(241, 241, 241);
}
</style>
