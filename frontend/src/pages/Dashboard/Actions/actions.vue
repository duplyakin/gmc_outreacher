<template>
  <div>
    <card>
      <div class="row">
        <div class="col-4 d-flex align-self-center">
          <span font->
            <h3>
              <i class="nc-icon nc-tag-content"></i> Actions log
            </h3>
          </span>
        </div>
      </div>
    </card>
    <card>
      <div class="col-12">
        <h5>Sort by action_type:</h5>
                <el-select multiple class="select-primary"
                           size="large"
                           v-model="multiple"
                           placeholder="Multiple Select">
                  <el-option v-for="action in uniqueActionTypes"
                             class="select-primary"
                             :value="action"
                             :label="action"
                             :key="action">
                  </el-option>
                </el-select>
        <div class="col-12 d-flex flex-row-reverse align-self-center">
          <div>
            <button
              @click.prevent="filter()"
              type="button"
              class="btn btn-default btn-success mx-1"
            >Filter</button>
          </div>
        </div>
      </div>
      <div class="col-12">
        <el-table
          stripe
          ref="actions_data_table"
          style="width: 100%;"
          :data="actions_data.actions"
          max-height="500"
          border
        >
          <el-table-column
            v-for="column in actions_data.columns"
            :key="column.label"
            :prop="column.prop"
            :label="column.label"
            show-overflow-tooltip
          >
          </el-table-column>
        </el-table>
      </div>

    </card>
  </div>
</template>
<script>
import { Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";
import get_actions from "./dummy_actions";
import Fuse from "fuse.js";

export default {
  components: {
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  computed: {

    uniqueActionTypes: function () {
      return [...new Set(this.actions_data.actions.map(action => action.action_type))];
    }
  },
  data() {
    return {
      multiple: "ARS",

      actions_data: {
        columns: [
          {
            prop: "action_type",
            label: "Action type",
            minWidth: 300
          },
          {
            prop: "data.value",
            label: "data",
            minWidth: 100
          },
          {
            prop: "medium",
            label: "medium",
            minWidth: 100
          },
          {
            prop: "key",
            label: "key",
            minWidth: 100
          }
        ],

        actions: [],

        pagination: {
          perPage: 0,
          currentPage: 1,
          perPageOptions: [5, 10, 25, 50],
          total: 0
        }
      },
      fuseSearch: null,
    };
  },
  methods: {
    initActions(){
      //TODO: connect to server
      this.actions_data.actions = get_actions;
    },
    filter() {
      let arr = this.multiple;
      if(typeof arr === 'undefined' || arr.length === 0) {
        this.initActions();
        return true;
      }
      this.actions_data.actions = this.actions_data.actions.filter(function(item){
        if(arr.includes(item.action_type))
          return item;
      });
    },
    validate() {
      return this.$validator.validateAll().then(res => {
        this.$emit("on-validated", 1, res, this.model);
        return res;
      });
    }
  },
  mounted() {
    this.initActions();
  }
};
</script>
<style>
</style>
