<template>
<div>
    <card>
    <div class="row">
        <div class="col-4 d-flex align-self-center">
            <span font-><h3><i class="nc-icon nc-single-02"></i> Accounts</h3></span>
        </div>
        <div class="col-8 d-flex flex-row-reverse align-self-center">
            <button @click.prevent="loadCredentials" type="button" class="btn btn-default btn-success mx-1">Reload</button>
            <button @click.prevent="addAccount" type="button" class="btn btn-default btn-success mx-1">Add account</button>
        </div>

    </div>
    </card>

    <div class="row">
    <div class="col-12">
        <card title="">
        <div>
            <div class="col-12">
            <el-table stripe
                        ref="accounts_data_table"
                        style="width: 100%;"
                        :data="accounts_data.credentials"
                        max-height="500"
                        border>
                <el-table-column v-for="column in accounts_data.columns"
                        :key="column.label"
                        :prop="column.prop"
                        :label="column.label"
                        :fixed="column.prop === 'account' ? true : false"
                        show-overflow-tooltip>
                        <template slot-scope="scope">
                            <a @click.prevent="editAccount(scope.row, scope.$index)" href="#"  v-if="column.prop === 'account'">{{ scope.row.data[column.prop] }}</a>
                            <template v-else-if="column.prop === 'status'">{{  status[scope.row[column.prop]] }}</template>
                            <template v-else-if="column.prop === 'error_message'"><div class="red">{{ show_data(scope.row, column) }}</div> </template>
                            <template v-else> {{ show_data(scope.row, column) }} </template>
                        </template>
                </el-table-column>
                <el-table-column :min-width="50" fixed="right" label="Refresh">
                    <template slot-scope="props">
                    <a
                        v-tooltip.top-center="'Refresh'"
                        class="btn-info btn-simple btn-link"
                        @click.prevent="refreshCredentials(props.row._id.$oid, props.$index)"
                    >
                        <i class="fa fa-refresh"></i>
                    </a>
                    </template>
                </el-table-column>
                <el-table-column :min-width="50" fixed="right" label="Delete">
                    <template slot-scope="props">
                    <a
                        v-tooltip.top-center="'Delete'"
                        class="btn-danger btn-simple btn-link"
                        @click.prevent="delete_credentials(props.row._id.$oid, props.$index)"
                    >
                        <i class="fa fa-times"></i>
                    </a>
                    </template>
                </el-table-column>

            </el-table>
            </div>
        </div>
        </card>
    </div>
    </div>

    <modal
    :width = "720"
    name="major_modal">
    </modal>

</div>
</template>
<script>
    import { Notification, Table, TableColumn, Select, Option } from 'element-ui'
    import axios from '@/api/axios-auth';

    const O24Pagination = () => import('src/components/O24Pagination.vue')
    const AccountEdit = () => import('./accountEdit.vue')
    const AccountAdd = () => import('./accountAdd.vue')

    const CREDENTIALS_API_LIST = '/credentials/list';
    const CREDENTIALS_API_EDIT = '/credentials/edit';
    const CREDENTIALS_API_DELETE = '/credentials/delete';
    const CREDENTIALS_API_ADD = '/credentials/add';
    const CREDENTIALS_API_REFRESH = '/credentials/refresh';


    export default {
    components: {
        O24Pagination,
        AccountEdit,
        AccountAdd,
        [Select.name]: Select,
        [Option.name]: Option,
        [Table.name]: Table,
        [TableColumn.name]: TableColumn
    },
    data () {
        return {
            status : {
                0 : 'Active',
                1 : 'Changed',
                '-1' : 'Error',
                '-2' : 'Unknown'
            },
            accounts_data: {
                columns : null,
                credentials : [],
            },
        }
    },
    methods: {
        switchPage(page){
            this.loadCredentials(event=null, page=page);
        },
        update_accounts_data(newData, init=0){
            this.accounts_data.columns = JSON.parse(newData.columns);

            if (newData.credentials){
                this.accounts_data.credentials = JSON.parse(newData.credentials);
            }
        },
        loadCredentials(event=null, page=1) {
            var data = new FormData();
            data.append('_page', page);

            const path = CREDENTIALS_API_LIST;

            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code > 0){
                    this.accounts_data.credentials = [];
                    this.update_accounts_data(r);
                }else{
                    var msg = 'Server Error loading credentials ' + r.msg;
                    Notification.error({title: "Error", message: msg});
                }
            })
            .catch((error) => {
                var msg = 'Error loading credentials ' + error;
                Notification.error({title: "Error", message: msg});
            });

        },
        refreshCredentials(credentials_id, row_index) {
            const current_index = row_index;
            const _table = this.$refs.accounts_data_table;

            const path = CREDENTIALS_API_REFRESH;

            var data = new FormData();
            data.append('_credentials_id', credentials_id);

            axios.post(path, data)
            .then((res) => {
                var r = res.data;
                if (r.code > 0) {
                    this.$set(this.accounts_data.credentials, current_index, JSON.parse(r.credentials));
                    _table.$forceUpdate();
                    Notification.success({title: "Success", message: "Account refreshed"});
                } else {
                    var msg = 'Server Error loading credentials ' + r.msg;
                    Notification.error({title: "Error", message: msg});
                }
            })
            .catch((error) => {
                var msg = 'Error loading credentials ' + error;
                Notification.error({title: "Error", message: msg});
            });
        },
        editAccount(account_dict, row_index) {

        const current_index = row_index;
        const _table = this.$refs.accounts_data_table;

        this.$modal.show(AccountEdit, {
            accountObj: account_dict,
            api_url : CREDENTIALS_API_EDIT,
            modalTitle: "Account edit",
            valueUpdated:(newValue) => {
                this.$set(this.accounts_data.credentials, current_index, newValue);
                _table.$forceUpdate();
                Notification.success({title: "Success", message: "Account changed"});
            }
            },
            {
            width: '720',
            height: 'auto',
            scrollable: true
            })
        },
        delete_credentials(credentials_id, row_index){
            if (confirm("Are you sure? This action CAN'T be undone")) {
                const path = CREDENTIALS_API_DELETE;

                var data = new FormData();
                data.append("_credentials_id", credentials_id);

                const index = row_index;
                axios
                    .post(path, data)
                    .then(res => {
                    var r = res.data;
                    if (r.code <= 0) {
                        var msg = "Error deleting " + r.msg;
                        Notification.error({title: "Error", message: msg});
                    } else {
                        this.loadCredentials();
                    }
                    })
                    .catch(error => {
                        var msg = "Error deleting " + error;
                        Notification.error({title: "Error", message: msg});
                    });
            }
        },
        addAccount(){
            this.$modal.show(AccountAdd, {
            api_url : CREDENTIALS_API_ADD,
            valueUpdated:(newValue) => {
                Notification.success({title: "Success", message: "Account added"});
                this.loadCredentials();
            }
            },
            {
                width: '720',
                height: 'auto',
                scrollable: true
            })
        },
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

    },
    mounted () {
        this.loadCredentials();
    },
    created() {
    },
    }
</script>
<style>
.red {
color: red;
}
</style>
