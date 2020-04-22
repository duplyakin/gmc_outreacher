<template>
<div>
  <card>
    <div class="row">
      <div class="col-4 d-flex align-self-center">
          <span font-><h3><i class="nc-icon nc-badge"></i> Prospects</h3></span>
      </div>
      <div class="col-8 d-flex flex-row-reverse align-self-center">

          <button type="button" class="btn btn-wd btn-danger mx-1">Delete</button>
          <button type="button" class="btn btn-default btn-success mx-1">Unassign</button>
          <button type="button" class="btn btn-default btn-success mx-1">Assign</button>

          <button type="button" class="btn btn-default btn-success mx-1">Upload</button>
          <button type="button" class="btn btn-default btn-success mx-1">Add manually</button>
      
        </div>

    </div>
  </card>    

  <div class="row">
    <div class="col-12">
      <card title="">
        <div> 
          <div class="col-12 d-flex">
            <card title="Filter prospects by:">
              <form @submit.prevent="submitFilter">
              <div class="row">
                <div class="col-3">
                    <el-select
                    class="select-default mb-3"
                    v-model="filters.column"
                    placeholder="Filter by column">
                    <el-option
                      class="select-default"
                      v-for="column in prospects_data.columns"
                      :key="column.label"
                      :label="column.label"
                      :value="column.label">
                    </el-option>
                  </el-select>      
        
                </div>
                <div class="col-5">
                 <fg-input name="filterInput"
                    class="mb-3"
                    :disabled="filters.column === '' ? true : false"
                    placeholder="Contains value..."
                    v-model="filters.contains"/>
                </div>
                <div class="col-2">
                    <el-select
                    class="select-default mb-3"
                    v-model="filters.campaign"
                    placeholder="Select campaign">
                    <el-option
                      class="select-default"
                      v-for="campaign in prospects_data.campaigns"
                      :key="campaign._id.$oid"
                      :label="campaign.title"
                      :value="campaign.title">
                    </el-option>
                  </el-select>      
                </div>
                <div class="col-2">
                    <el-select
                    class="select-default mb-3"
                    v-model="filters.list"
                    placeholder="Select list">
                    <el-option
                      class="select-default"
                      v-for="list in prospects_data.lists"
                      :key="list._id.$oid"
                      :label="list.title"
                      :value="list.title">
                    </el-option>
                  </el-select>
      
                </div>
              </div>
              <div class="row">
                  <div class="col-6 d-flex">
                      <p class="text-danger" v-if="this.filters.error != ''">
                        {{ this.filters.error }}
                      </p>  
                  </div>
                  <div class="col-6 d-flex flex-row-reverse">
                    <button type="submit" class="btn btn-outline btn-wd btn-success mx-1">Apply Filter</button>
                    <button v-on:click="filterClear" type="button" class="btn btn-outline btn-wd btn-danger">Clear Filter</button>
                  </div>
              </div>
              </form>
            </card>

          </div>
          <div class="col-12">
            <el-table stripe
                      style="width: 100%;"
                      @selection-change="handleSelectionChange"
                      :data="prospects_data.prospects"
                      max-height="500"
                      border>
              <el-table-column
                      type="selection"
                      width="55"
                      v-if="prospects_data.columns"
                      fixed>
              </el-table-column>
              <el-table-column v-for="column in prospects_data.columns"
                        :key="column.label"
                        :prop="column.prop"
                        :label="column.label"
                        :fixed="column.label === 'Email' ? true : false"
                        show-overflow-tooltip>
                        <template slot-scope="scope">
                          <a href=""  v-if="column.label === 'Email'">{{ scope.row.data[column.prop] }}</a>
                          <template v-else> {{ scope.row.data[column.prop] }} </template>
                        </template>     
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div slot="footer" class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
          <div class="">
            <p class="card-category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>
          </div>
          <l-pagination class="pagination-no-border"
                        v-model="pagination.currentPage"
                        :per-page="pagination.perPage"
                        :total="pagination.total">
          </l-pagination>
        </div>
      </card>
    </div>
  </div>
</div>
</template>
<script>
  import { Table, TableColumn, Select, Option } from 'element-ui'
  import {Pagination as LPagination} from 'src/components/index'
  import users from './dummy.js'
  import Fuse from 'fuse.js'
  import axios from 'axios'

  export default {
    components: {
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
        pagination: {
          perPage: 50,
          currentPage: 1,
          perPageOptions: [5, 10, 25, 50],
          total: 0
        },
        modelValidations: {
          requiredText: {
            required: true
          }
        },
        requiredText: '',
        searchQuery: '',
        propsToSearch: ['name', 'email', 'age'],
        tableColumns: [
          {
            prop: 'name',
            label: 'Name',
            minWidth: 200
          },
          {
            prop: 'email',
            label: 'Email',
            minWidth: 250
          },
          {
            prop: 'age',
            label: 'Age',
            minWidth: 100
          },
          {
            prop: 'salary',
            label: 'Salary',
            minWidth: 120
          }
        ],
        tableData: users,
        prospects_data: {
          columns : null,
          prospects : [],
          lists : null,
          campaigns: null
        },
        multipleSelection: [],
        filters: {
          campaign : '',
          list : '',
          column : '',
          contains: '',
          error: '',
          message: ''
        },
        fuseSearch: null
      }
    },
    methods: {
      filterClear(){
        this.filters.column = '';
        this.filters.campaign = '';
        this.filters.list = '';
        this.filters.contains = '';
        this.filters.error = '';
      },
      submitFilter(event) {
        if (this.filters.contains == ''){
          this.filters.error = 'Input contains value';
          return false;
        }
        this.filters.error = '';

        var filterFormData = new FormData();
        filterFormData.append('_contains', this.filters.contains);
        filterFormData.append('_campaign_field', this.filters.campaign);

        const path = 'http://127.0.0.1:5000/prospects';
        axios
          .post(path, filterFormData)
          .then((res) => {
            var r = res.data;
            console.log("request received");
            console.log(r);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });

        console.log(this.filters);
      },
      initProspects() {
        const path = 'http://127.0.0.1:5000/prospects';
        axios.get(path)
          .then((res) => {
            var r = res.data;
            this.prospects_data.campaigns = JSON.parse(r.campaigns);
            this.prospects_data.lists = JSON.parse(r.lists);

            this.prospects_data.prospects = JSON.parse(r.prospects);
            this.prospects_data.columns = JSON.parse(r.columns);

          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
  
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(this.multipleSelection);
      },
      handleLike (index, row) {
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
      }
    },
    mounted () {
      this.fuseSearch = new Fuse(this.tableData, {keys: ['email']})
    },
    created() {
      this.initProspects();
    },

  }
</script>
<style>
</style>
