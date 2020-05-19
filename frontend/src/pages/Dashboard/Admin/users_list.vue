<template>
<div>
<card>
<div class="row">
    <div class="col-4 d-flex align-self-center">
        <h3>
        <i class="nc-icon nc-bag"></i> LinkedIn actions
        </h3>
    </div>
    <div class="col-8 d-flex flex-row-reverse align-self-center">
    <div>
        <button
            @click.prevent="addCampaign"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Add action</button>
        <button
            @click.prevent="reload_users"
            type="button"
            class="btn btn-default btn-success mx-1"
        >Reload actions</button>

    </div>
    </div>
</div>
</card>

<card>
        <div class="col-12">
            <el-table
            stripe
            ref="campaigns_data_table"
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
                :fixed="column.prop === 'title' ? true : false"
                show-overflow-tooltip>
                <template slot-scope="scope">
                    <a @click.prevent="editCampaign(scope.row, scope.$index)" href="#"  v-if="column.prop === 'title'">{{ scope.row[column.prop] }}</a>
                    <template v-else-if="column.prop === 'status'">{{  status[scope.row[column.prop]] }}</template>
                    <template v-else> {{ show_data(scope.row, column) }} </template>
                </template>
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Action">
                <template slot-scope="props">
                <a
                    class="btn-simple btn-link"
                    @click.prevent="make_action(props.row, props.$index)"
                    href="#"
                >
                    {{ props.row.status == 1 ? 'Pause' : 'Start' }}
                </a>
                </template>
            </el-table-column>
            <el-table-column :min-width="50" fixed="right" label="Delete">
                <template slot-scope="props">
                <a
                    v-tooltip.top-center="'Delete'"
                    class="btn-danger btn-simple btn-link"
                    @click.prevent="delete_user(props.row._id.$oid, props.$index)"
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
                {{ this.list_data }}
            </div>
        </div>

</div>
</template>
<script>
import { Notification, Table, TableColumn, Select, Option } from "element-ui";
import { Pagination as LPagination } from "src/components/index";

import axios from '@/api/axios-auth';

const CHANGE_ROLES_API = '/admin/roles/data';
const USERS_API_LIST = '/admin/users/list';

export default {
components: {
    LPagination,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
},
computed: {
},
data() {
    return {
        test : true,
        pagination : {
            perPage : 0,
            currentPage : 1,
            perPageOptions: [5, 10, 25, 50],
            total : 0
        },
        list_data : {
            columns : [],
            users: [],
            roles: [],
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
    delete_user(user_id, row_index){
        if (confirm("Are you sure?")) {
            const path = CAMPAIGNS_API_DELETE;

            var data = new FormData();
            data.append("_campaign_id", campaign_id);

            const index = row_index;
            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error deleting user " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_users();
                }
                })
                .catch(error => {
                    var msg = "Error deleting user " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
    },
    editCampaign(msg_dict, index) {
        var status = -2;
        if (msg_dict.hasOwnProperty('status')){
            status = msg_dict['status'];
        }
        if (status == -2 || status == 1){
            Notification.error({title: "Error", message: "Pause campaign for edit, current status: " + status});
            return false;
        }

        this.$router.push({ path: "campaign_edit_form", query: { campaign_id: msg_dict._id.$oid } })
    },
    next_page(){
        var page = 2;
        this.load_data(page,0);
    },
    reload_users(event){
        return this.load_users(1);
    },
    load_users(page=1){
        const path = USERS_API_LIST;

        var data = new FormData();
        data.append('_page', page);

        axios.post(path, data).then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading users." + r.msg;
                Notification.error({title: "Error", message: msg});
            } else {
                this.deserialize_users(r);
                //console.
            }
            })
            .catch((error) => {
                var msg = "Error loading users. ERROR: " + error;
                Notification.error({title: "Error", message: msg});
            });

    },
    load_data(){
        const path = CAMPAIGNS_API_DATA;

        var data = new FormData();
        axios
            .post(path, data)
            .then(res => {
            var r = res.data;
            if (r.code <= 0) {
                var msg = "Error loading data " + r.msg;
                Notification.error({title: "Error", message: msg});
            } else {
                this.deserialize_data(r);
            }
            })
            .catch(error => {
                var msg = "Error loading data " + error;
                Notification.error({title: "Error", message: msg});
            });
    },
    deserialize_data(from_data){
        for (var key in from_data){
            if (this.list_data.hasOwnProperty(key) && from_data[key]){
                var parsed_data = JSON.parse(from_data[key])
                this.$set(this.list_data, key, parsed_data);
            }
        }
    },
    deserialize_users(from_data){
        var pagination_dict = JSON.parse(from_data.pagination);
        this.$set(this, 'pagination', pagination_dict);

        var columns = JSON.parse(from_data.columns);
        this.$set(this.list_data, 'columns', columns);

        if (from_data.users){
            var users = JSON.parse(from_data.users)
            this.$set(this.list_data, 'users', users);
        }

        if (from_data.roles){
            var roles = JSON.parse(from_data.users)
            this.$set(this.list_data, 'roles', roles);
        }
    },

},
async mounted() {
    //await this.load_data();
    await this.load_users();
}
};
</script>
<style>
</style>
