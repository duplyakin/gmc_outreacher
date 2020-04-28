<template>
  <div class="row">
    <div class="col-12">
      <card title="Create content">
        <l-button @click="addMessage" type="primary" wide>+ Add message</l-button>&nbsp;
        <div class="col-12">
            <el-table stripe
                      ref="messages_data_table"
                      style="width: 100%;"
                      :data="messages_data.messages"
                      max-height="500"
                      border>
              <el-table-column v-for="column in messages_data.columns"
                        :key="column.label"
                        :prop="column.prop"
                        :label="column.label"
                        :fixed="column.label === 'subject' ? true : false"
                        show-overflow-tooltip>
                        <template slot-scope="scope">
                          <a @click.prevent="editMessage(scope.row, scope.$index)" href="#"  v-if="column.label === 'Subject'">{{ scope.row[column.prop] }}</a>
                          <template v-else> {{ scope.row[column.prop] }} </template>
                        </template>     
              </el-table-column>
              <el-table-column
                :min-width="50"
                fixed="right"
                label="Send test">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Test'" class="btn-info btn-simple btn-link"
                     @click="handleTest(props.$index, props.row)">
                    <i class="fa fa-heart"></i></a>
                </template>
              </el-table-column>
              <el-table-column
                :min-width="50"
                fixed="right"
                label="Delete">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Delete'" class="btn-danger btn-simple btn-link"
                     @click="handleDelete(props.$index, props.row)"><i class="fa fa-times"></i></a>
                </template>
              </el-table-column>
            </el-table>
          </div>
      </card>
    </div>
  </div>
</template>
<script>
  import { Table, TableColumn, Select, Option } from 'element-ui'
  import {Pagination as LPagination} from 'src/components/index'
  import get_messages from './messages_linkedin'
  import Fuse from 'fuse.js'
  import MessageEdit from './messageEdit.vue'
  import NotificationMessage from './notification.vue';

  export default {
    props: {
    campaign: {
        messagesListLinkedin: Array,
    },
  },
    components: {
      MessageEdit,
      LPagination,
      [Select.name]: Select,
      [Option.name]: Option,
      [Table.name]: Table,
      [TableColumn.name]: TableColumn
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
        model: {
          messages: [],
        },
        pagination: {
          perPage: 5,
          currentPage: 1,
          perPageOptions: [5, 10, 25, 50],
          total: 0
        },
        searchQuery: '',
        
        messages_data: {
          columns : [
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

          //messages : get_messages,
          messages : this.campaign.messagesListLinkedin,
          //messages : [],

          pagination : {
            perPage : 0,
            currentPage : 1,
            total : 0
          }
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
      handleDelete_1 (index, row) {
        let indexToDelete = this.tableData.findIndex((tableRow) => tableRow.id === row.id)
        if (indexToDelete >= 0) {
          this.tableData.splice(indexToDelete, 1)
        }
      },
      handleDelete (index, row) {
        //let indexToDelete = this.tableData.findIndex((tableRow) => tableRow.id === row.id)
        let indexToDelete = this.messages_data.messages.findIndex((tableRow) => tableRow.id === row.id)
        //console.log("arr:", indexToDelete);
        if (indexToDelete >= 0) {
          //this.tableData.splice(indexToDelete, 1)
          this.messages_data.messages.splice(indexToDelete, 1)
        }
      },
      update_messages_data(newData){
        if (newData.body && newData.subject){
          var i = this.messages_data.messages.length;
          this.$set(this.messages_data.messages, i, newData);
        }
        //this.messages_data.pagination = JSON.parse(newData.pagination);
      },
      addMessage () {
        const _table = this.$refs.messages_data_table;
        this.$modal.show(MessageEdit, {
            messageObj: {},
            //modalTitle: "Prospect create",
            //action: 'create',
            //api_url : PROSPECTS_API_CREATE,
            valueUpdated:(newValue) => {
              this.$notify(
                {
                  component: NotificationMessage,
                  message: 'Message created Success',
                  icon: 'nc-icon nc-bulb-63',
                  type: 'success'
                })
                this.update_messages_data(newValue);  
            }
          },
          {
            width: '720',
            height: 'auto'
          })
      },
      editMessage (msg_dict, row_index) {
        const current_index = row_index;
        const _table = this.$refs.messages_data_table;

        this.$modal.show(MessageEdit, {
            messageObj: msg_dict,
            //api_url : 'PROSPECTS_API_EDIT',
            //action: 'edit',
            //modalTitle: "Message edit",
            valueUpdated:(newValue) => {
              this.$set(this.messages_data.messages, current_index, newValue);
              _table.$forceUpdate();
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
      validate() {
        return this.$validator.validateAll().then(res => {
          if(res) {
            this.model.messages = this.messages_data.messages;
            this.$emit("on-validated", 'step_2_linkedin', res, this.model);
          };
          return res;
        });
    }
    },
    mounted () {
      //this.fuseSearch = new Fuse(this.tableData, {keys: ['name', 'email']});
    },
  }
</script>
<style>
</style>
