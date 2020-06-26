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
            </div>

            <div v-if="multipleSelection.length > 0">
              <button 
                @click.prevent="delete_data"
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
          ref="list_table"
          style="width: 100%;"
          :data="list_data.list"
          max-height="500"
          border
          @selection-change="handleSelectionChange"
        >
          <el-table-column
            type="selection"
            width="55">
          </el-table-column>
          <el-table-column
            width="270"
            v-for="(column,index) in list_data.columns"
            :key="index"
            :prop="column.prop"
            :label="column.label"
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
      test: false,
      multipleSelection: [],
      list_data: {
        columns: [{label: "Email | Domain | Linkedin", prop: "source"}, {label: "Type", prop: "type"}, {label: "Added date", prop: "date"}],
        list: []
      }
    };
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    delete_data() {
      if (confirm("Are you sure?")) {
        const path = LIST_API_DELETE

        let list = this.multipleSelection.map(function(elem) {
          return elem.source
        })

        var data = new FormData()
        data.append("ids", JSON.stringify(list))

        axios
          .post(path, data)
          .then(res => {
            var r = res.data;
            if (r.code <= 0) {
              var msg = "Error deleting list " + r.msg
              Notification.error({ title: "Error", message: msg })
            } else {
              this.load_list()
            }
          })
          .catch(error => {
            var msg = "Error deleting list " + error
            Notification.error({ title: "Error", message: msg })
          });
      }
    },

    add_data() {
      this.$modal.show(
        ListForm,
        {
          api_url: LIST_API_ADD,
          valueUpdated: () => {
            Notification.success({ title: "Success", message: "List updated" });
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
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading blacklist." + r.msg;
            Notification.error({ title: "Error", message: msg });

          } else {
            if(r.data != null) {
              this.deserialize_list(r.data)
            }

          }
        })
        .catch(error => {
          var msg = "Error loading blacklist. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    deserialize_list(from_data) {
      if (from_data != null) {
        from_data = JSON.parse(from_data)
      } else {
        return
      }

      var emails = []
      var domains = []
      var linkedin = []

      if (from_data.emails != null) {
        var emails_obj = JSON.parse(from_data.emails)
        emails = Object.keys(emails_obj).map(function(key) {
          return { source: key, date: emails_obj[key], type: "Email" }
        })
      }

      if (from_data.domains != null) {
        var domains_obj = JSON.parse(from_data.domains)
        domains = Object.keys(domains_obj).map(function(key) {
          return { source: key, date: domains_obj[key], type: "Domain" }
        })
      }

      if (from_data.linkedin != null) {
        var linkedin_obj = JSON.parse(from_data.linkedin)
        linkedin = Object.keys(linkedin_obj).map(function(key) {
          return { source: key, date: linkedin_obj[key], type: "Linkedin" }
        })
      }

      var list_arr = emails
      list_arr.push(...domains)
      list_arr.push(...linkedin)

      this.$set(this.list_data, "list", list_arr)

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
