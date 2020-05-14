<template>
<div>
<card>
<div class="row">
    <div class="col-4 d-flex align-self-center">
        <h3>
        <i class="nc-icon nc-single-copy-04"></i> Prospect Lists
        </h3>
    </div>
    <div class="col-8 d-flex flex-row-reverse align-self-center">
    <div>
        <button
            @click.prevent="addList"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Create List</button>
        <button
            @click.prevent="load_lists"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Reload Lists</button>

    </div>
    </div>
</div>
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
                show-overflow-tooltip>
                <template slot-scope="scope">
                    <a @click.prevent="editList(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                    <template v-else-if="column.prop === 'total'">{{  scope.row[column.prop][0] || 0  }}</template>
                    <template v-else> {{ scope.row[column.prop] }} </template>
                </template> 
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Delete">
                <template slot-scope="props">
                <a
                    v-tooltip.top-center="'Delete'"
                    class="btn-danger btn-simple btn-link"
                    @click.prevent="delete_list(props.row._id.$oid, props.$index)"
                >
                    <i class="fa fa-times"></i>
                </a>
                </template>
            </el-table-column>
            </el-table>
        </div>
    
        </card>     

        <div v-if="test" class="row">
            <div class="col-12">
                <pre>{{ this.list_data}}</pre>
            </div>
        </div>
<modal
:width = "720"
name="major_modal">
</modal>
         
</div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import NotificationMessage from './notification.vue';

import ListForm from "./list_form.vue";
import axios from '@/api/axios-auth';

const LISTS_API_LIST = 'http://127.0.0.1:5000/lists/aggregate'
const LISTS_API_ADD = 'http://127.0.0.1:5000/lists/add'
const LISTS_API_DELETE = 'http://127.0.0.1:5000/lists/remove';
const LISTS_API_EDIT = 'http://127.0.0.1:5000/lists/edit';


export default {
components: {
    ListForm,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
computed: {
},
data() {
    return {
        test : false,
        list_data : {
            columns : [],
            lists : []
        },
    };
},
methods: {
    show_data(scope_row, column){
        var data = column.data || '';
        if (data){
            return scope_row.data[column.prop] || '';
        }else{
            var field = column.field || '';
            if (field){
                return scope_row[column.prop][field] || '';
            }else{
                return scope_row[column.prop] || '';
            }
        }

        return '';
    },
    delete_list(list_id, row_index){
        if (confirm("Are you sure?")) {
            const path = LISTS_API_DELETE;

            var data = new FormData();
            data.append("_list_id", list_id);
            
            const index = row_index;
            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error deleting list " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_lists();
                }
                })
                .catch(error => {
                    var msg = "Error deleting list " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
    },
    addList() {
        this.$modal.show(ListForm, {
            listObj: {},
            modalTitle: "Add Prospect List",
            action: 'create',
            api_url : LISTS_API_ADD,
            valueUpdated:(newValue) => {
                this.$notify(
                {
                    component: NotificationMessage,
                    message: 'List created Success',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                })
                this.load_lists();   
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    editList(msg_dict, index) {
        this.$modal.show(ListForm, {
            listObj : msg_dict,
            modalTitle: "Edit Prospect List",
            action: 'edit',
            api_url : LISTS_API_EDIT,
            valueUpdated:(newValue) => {
                this.$notify(
                {
                    component: NotificationMessage,
                    message: 'List edit Success',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                })
                this.load_lists();   
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
    },
    load_lists(){
        const path = LISTS_API_LIST;
    
        var data = new FormData();

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading lists." + r.msg;
                Notification.error({title: "Error", message: msg});
            }else{
                this.deserialize_lists(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading lists. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });

    },
    deserialize_lists(from_data){
        var columns = JSON.parse(from_data.columns);
        this.$set(this.list_data, 'columns', columns);

        if (from_data.lists){
            var lists = JSON.parse(from_data.lists)
            this.$set(this.list_data, 'lists', lists);
        }
    },

},
mounted() {
    this.load_lists();
}
};
</script>
<style>
</style>
