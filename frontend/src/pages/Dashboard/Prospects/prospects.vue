<template>
  <div class="row">
    <div class="col-md-12">
      <h4 class="title">Prospects - upload/filter and view all the info</h4>
    </div>

    <div class="col-12">
      <card title="Prospects">
        <div>
          <div class="col-12 d-flex justify-content-center justify-content-sm-between flex-wrap">
            <el-select
              class="select-default mb-3"
              style="width: 200px"
              v-model="filters.campaign_any"
              placeholder="Select campaign">
              <el-option
                class="select-default"
                v-for="campaign in filters.campaigns"
                :key="campaign._id.$oid"
                :label="campaign.title"
                :value="campaign.title">
              </el-option>
            </el-select>

            <el-select
              class="select-default mb-3"
              style="width: 200px"
              v-model="filters.list_any"
              placeholder="Select list">
              <el-option
                class="select-default"
                v-for="list in filters.lists"
                :key="list._id.$oid"
                :label="list.title"
                :value="list.title">
              </el-option>
            </el-select>
         
          </div>
          <div class="col-sm-12">
            <el-table stripe
                      style="width: 100%;"
                      :data="prospects"
                      max-height="500"
                      border>
              <el-table-column v-for="column in prospects_data.columns"
                               :key="column"
                               :label="column">
              </el-table-column>
              <el-table-column
                :min-width="120"
                fixed="right"
                label="Actions">
                <template slot-scope="props">
                  <a v-tooltip.top-center="'Like'" class="btn-info btn-simple btn-link"
                     @click="handleLike(props.$index, props.row)">
                    <i class="fa fa-heart"></i></a>
                  <a v-tooltip.top-center="'Edit'" class="btn-warning btn-simple btn-link"
                     @click="handleEdit(props.$index, props.row)"><i
                    class="fa fa-edit"></i></a>
                  <a v-tooltip.top-center="'Delete'" class="btn-danger btn-simple btn-link"
                     @click="handleDelete(props.$index, props.row)"><i class="fa fa-times"></i></a>
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
        <div>
          <textarea>
            {{prospects}}
          </textarea>
        </div>
      </card>
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
        prospects: null,
        prospects_data: {
          columns : null,
          prospects : null,
        },

        filters: {
          campaign_any : 'Any campaign',
          list_any : 'Any list',

          lists : null,
          campaigns: null
        },
        fuseSearch: null
      }
    },
    methods: {
      initProspects() {
        const path = 'http://127.0.0.1:5000/prospects';
        axios.get(path)
          .then((res) => {
            var r = res.data;
            this.filters.campaigns = JSON.parse(r.campaigns);
            this.filters.lists = JSON.parse(r.lists);

            this.prospects = JSON.parse(r.prospects);
            this.prospects_data.columns = JSON.parse(r.columns);

          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
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
