<template>
  <div class="row">
    <div class="col-12">
      <card title="Create content">
        <div>
          <div class="col-12">
            <l-button v-on:click="editMessage" type="primary" wide>+ Add message</l-button>&nbsp;
            <el-table stripe
                      style="width: 100%;"
                      :data="queriedData"
                      border>
              <el-table-column v-for="column in tableColumns"
                               :key="column.label"
                               :min-width="column.minWidth"
                               :prop="column.prop"
                               :label="column.label">
                               
              </el-table-column>
              <el-table-column
                :min-width="120"
                fixed="right"
                label="Send test">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Test'" class="btn-info btn-simple btn-link"
                     @click="handleTest(props.$index, props.row)">
                    <i class="fa fa-heart"></i></a>
                </template>
              </el-table-column>
              <el-table-column
                :min-width="120"
                fixed="right"
                label="Edit">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Edit'" class="btn-warning btn-simple btn-link"
                     @click.prevent="editMessage(props.row, props.$index)">
                     <i class="fa fa-edit"></i></a>
                </template>
              </el-table-column>
              <el-table-column
                :min-width="120"
                fixed="right"
                label="Delete">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Delete'" class="btn-danger btn-simple btn-link"
                     @click="handleDelete(props.$index, props.row)"><i class="fa fa-times"></i></a>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div slot="footer" class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
          <l-pagination class="pagination-no-border"
                        v-model="pagination.currentPage"
                        :per-page="pagination.perPage"
                        :total="pagination.total">
          </l-pagination>
        </div>
      </card>
    </div>
  </div>
</template>
<script>
  import { Table, TableColumn, Select, Option } from 'element-ui'
  import {Pagination as LPagination} from 'src/components/index'
  import get_messages from './messages'
  import Fuse from 'fuse.js'
  import MessageEdit from './messageEdit.vue'
  import NotificationMessage from './notification.vue';

  export default {
    components: {
      MessageEdit,
      LPagination,
      [Select.name]: Select,
      [Option.name]: Option,
      [Table.name]: Table,
      [TableColumn.name]: TableColumn
    },
    props: {
      newMessageObj: Object,
    },
    computed: {
      pagedData () {
        return this.tableData.slice(this.from, this.to)
      },
      /***
       * Searches through table data and returns a paginated array.
       * Note that this should not be used for table with a lot of data as it might be slow!
       * Do the search and the pagination on the server and display the data retrieved from server instead.
       * @returns {computed.pagedData}
       */
      queriedData () {
        let result = this.tableData
        if (this.searchQuery !== '') {
          result = this.fuseSearch.search(this.searchQuery)
          this.pagination.total = result.length
        }
        return result.slice(this.from, this.to)
      },
      to () {
        let highBound = this.from + this.pagination.perPage
        if (this.total < highBound) {
          highBound = this.total
        }
        return highBound
      },
      from () {
        return this.pagination.perPage * (this.pagination.currentPage - 1)
      },
      total () {
        this.pagination.total = this.tableData.length
        return this.tableData.length
      }
    },
    data () {
      return {
        pagination: {
          perPage: 5,
          currentPage: 1,
          perPageOptions: [5, 10, 25, 50],
          total: 0
        },
        searchQuery: '',
        tableColumns: [
          {
            prop: 'subject',
            label: 'Subject',
            minWidth: 300
          },
          {
            prop: 'interval',
            label: 'Interval',
            minWidth: 100
          },
        ],
        new_message_data: {
          id: "",
          subject: "",
          body: "",
          interval: ""
        },
        messages_data: {
          columns : null,
          messages : get_messages,
          lists : null,
          campaigns: null
        },
        tableData: get_messages,
        fuseSearch: null
      }
    },
    methods: {
      handleTest (index, row) {
        alert(`Your want to like ${row.name}`)
      },
      handleEdit (index, row) {
        alert(`Your want to edit ${row.name}`)
      },
      handleDelete (index, row) {
        let indexToDelete = this.tableData.findIndex((tableRow) => tableRow.id === row.id)
        if (indexToDelete >= 0) {
          this.tableData.splice(indexToDelete, 1)
        }
      },
      editMessage (msg_dict, row_index) {
        const current_index = row_index;
        //const _table = this.$refs.prospects_data_table;

        this.$modal.show(MessageEdit, {
            messageObj: msg_dict,
            valueUpdated:(newValue) => {
              this.$set(this.messages_data.messages, current_index, newValue);
              //_table.$forceUpdate();
              this.$notify(
                {
                  component: NotificationMessage,
                  message: 'Updated Success',
                  icon: 'nc-icon nc-bulb-63',
                  type: 'success'
                })
            }
          },
          {
            width: '720',
            height: 'auto'
          })
      },
    },
    mounted () {
      this.fuseSearch = new Fuse(this.tableData, {keys: ['name', 'email']});
      this.new_message_data = JSON.parse(JSON.stringify(this.newMessageObj));
      this.$set(this.tableData, 1, this.new_message_data);
    },
  }
</script>
<style>
</style>
