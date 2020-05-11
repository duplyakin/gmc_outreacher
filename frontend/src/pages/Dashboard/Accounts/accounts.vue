<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <span font->
            <h3>
              <i class="nc-icon nc-single-02"></i> Accounts
            </h3>
          </span>
        </div>
        <div class="col-8 d-flex flex-row-reverse align-self-center">
          <div v-if="multipleSelection.length > 0">
            <button
              @click.prevent="deleteAccounts"
              type="button"
              class="btn btn-wd btn-danger mx-1"
            >Delete</button>
          </div>

          <div v-if="multipleSelection.length == 0">
            <button
              @click.prevent="addAccount"
              type="button"
              class="btn btn-default btn-success mx-1"
            >Add account</button>
            <button
              @click.prevent="loadCredentials"
              type="button"
              class="btn btn-default btn-success mx-1"
            >Reload</button>
          </div>
        </div>
      </div>
    </card>

    <div class="row">
      <div class="col-12">
        <card title>
          <div>
            <div class="col-12">
              <el-table
                stripe
                ref="accounts_data_table"
                style="width: 100%;"
                @selection-change="handleSelectionChange"
                :data="accounts_data.credentials"
                max-height="500"
                border
              >
                <el-table-column type="selection" width="55" v-if="accounts_data.columns" fixed></el-table-column>
                <el-table-column
                  v-for="column in accounts_data.columns"
                  :key="column.label"
                  :prop="column.prop"
                  :label="column.label"
                  :fixed="column.prop === 'account' ? true : false"
                  show-overflow-tooltip
                >
                  <template slot-scope="scope">
                    <a
                      @click.prevent="editAccount(scope.row, scope.$index)"
                      href="#"
                      v-if="column.prop === 'account'"
                    >{{ scope.row.data[column.prop] }}</a>
                    <template
                      v-else
                    >{{ column.data ? scope.row.data[column.prop] : scope.row[column.prop] }}</template>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
          <div
            slot="footer"
            class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap"
          >
            <div class>
              <p class="card-category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>
            </div>
            <o24-pagination
              class="pagination-no-border"
              v-model="accounts_data.pagination.currentPage"
              :per-page="accounts_data.pagination.perPage"
              :total="accounts_data.pagination.total"
              v-on:switch-page="switchPage"
            ></o24-pagination>
          </div>
        </card>
      </div>
    </div>

    <modal :width="720" name="major_modal"></modal>
  </div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import O24Pagination from "src/components/O24Pagination.vue";
import O24NotificationMessage from "src/components/O24Notification.vue";
import AccountEdit from "./accountEdit.vue";
import AccountAdd from "./accountAdd.vue";

import axios from "axios";

const CREDENTIALS_API_LIST = "http://127.0.0.1:5000/credentials";
const CREDENTIALS_API_EDIT = "http://127.0.0.1:5000/credentials/edit";
const CREDENTIALS_API_DELETE = "http://127.0.0.1:5000/credentials/delete";
const CREDENTIALS_API_ADD = "http://127.0.0.1:5000/credentials/add";

export default {
  components: {
    O24NotificationMessage,
    O24Pagination,
    AccountEdit,
    AccountAdd,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {
    to() {
      let highBound = this.from + this.accounts_data.pagination.perPage;
      if (this.total < highBound) {
        highBound = this.total;
      }
      return highBound;
    },
    from() {
      return (
        this.accounts_data.pagination.perPage *
        (this.accounts_data.pagination.currentPage - 1)
      );
    },
    total() {
      return this.accounts_data.pagination.total;
    }
  },
  data() {
    return {
      accounts_data: {
        columns: null,

        credentials: [],

        pagination: {
          perPage: 0,
          currentPage: 1,
          total: 0
        }
      },
      multipleSelection: []
    };
  },
  methods: {
    switchPage(page) {
      this.loadCredentials((event = null), (page = page));
    },
    update_accounts_data(newData, init = 0) {
      this.accounts_data.columns = JSON.parse(newData.columns);

      if (newData.credentials) {
        this.accounts_data.credentials = JSON.parse(newData.credentials);
      }
      this.accounts_data.pagination = JSON.parse(newData.pagination);
    },
    loadCredentials(event = null, page = 1) {
      var data = new FormData();
      data.append("_page", page);

      const path = CREDENTIALS_API_LIST;

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code > 0) {
            this.accounts_data.credentials = [];
            this.update_accounts_data(r);
          } else {
            var msg = "Server Error loading credentials " + r.msg;
            Notification.error({
              title: "Error",
              message: msg
            });
          }
        })
        .catch(error => {
          var msg = "Error loading credentials " + error;
          Notification.error({
            title: "Error",
            message: msg
          });
        });
    },
    editAccount(account_dict, row_index) {
      const current_index = row_index;
      const _table = this.$refs.accounts_data_table;

      this.$modal.show(
        AccountEdit,
        {
          accountObj: account_dict,
          api_url: CREDENTIALS_API_EDIT,
          modalTitle: "Account edit",
          valueUpdated: newValue => {
            this.$set(this.accounts_data.credentials, current_index, newValue);
            _table.$forceUpdate();
            this.$notify({
              component: O24NotificationMessage,
              message: "Edit Success",
              icon: "nc-icon nc-bulb-63",
              type: "success"
            });
          }
        },
        {
          width: "720",
          height: "auto"
        }
      );
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    deleteAccounts() {
      if (confirm("Are you sure? This action CAN'T be undone")) {
        const path = CREDENTIALS_API_DELETE;

        var deleteData = new FormData();
        deleteData.append("_delete", JSON.stringify(this.multipleSelection));

        axios
          .post(path, deleteData)
          .then(res => {
            var r = res.data;
            if (r.code <= 0) {
              var msg = "Error deleting account " + r.msg;
              Notification.error({
                title: "Error",
                message: msg
              });
            } else {
              this.$notify({
                component: O24NotificationMessage,
                message: "Delete success",
                icon: "nc-icon nc-bulb-63",
                type: "success"
              });
              this.loadCredentials();
            }
          })
          .catch(error => {
            var msg = "Error deleting account " + error;
            Notification.error({
              title: "Error",
              message: msg
            });
          });
      }
    },
    addAccount() {
      this.$modal.show(
        AccountAdd,
        {
          api_url: CREDENTIALS_API_ADD,
          valueUpdated: newValue => {
            this.$notify({
              component: O24NotificationMessage,
              message: "Account added success",
              icon: "nc-icon nc-bulb-63",
              type: "success"
            });
            this.loadCredentials();
          }
        },
        {
          width: "720",
          height: "auto"
        }
      );
    }
  },
  mounted() {
    this.loadCredentials();
  },
  created() {}
};
</script>
<style>
</style>
