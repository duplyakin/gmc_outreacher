<template>
<div>
    <card>
    <div class="row">
        <div class="col-4 d-flex align-self-center">
            <span font-><h3><i class="nc-icon nc-badge"></i> Accounts</h3></span>
        </div>
        <div class="col-8 d-flex flex-row-reverse align-self-center">
            <button @click.prevent="addAccount" type="button" class="btn btn-default btn-success mx-1">Add account</button>
            <button @click.prevent="loadCredentials" type="button" class="btn btn-default btn-success mx-1">Reload</button>
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
                        @selection-change="handleSelectionChange"
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
                            <template v-else> {{ show_data(scope.row, column) }} </template>
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
    import { Table, TableColumn, Select, Option } from 'element-ui'
    import O24Pagination from 'src/components/O24Pagination.vue'
    import O24NotificationMessage from 'src/components/O24Notification.vue'
    import AccountEdit from './accountEdit.vue'
    import AccountAdd from './accountAdd.vue'

    import axios from 'axios'

    const CREDENTIALS_API_LIST = 'http://127.0.0.1:5000/credentials/list';
    const CREDENTIALS_API_EDIT = 'http://127.0.0.1:5000/credentials/edit';
    const CREDENTIALS_API_DELETE = 'http://127.0.0.1:5000/credentials/delete';
    const CREDENTIALS_API_ADD = 'http://127.0.0.1:5000/credentials/add';


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
                    alert(msg)
                }
            })
            .catch((error) => {
                var msg = 'Error loading credentials ' + error;
                alert(msg);
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
                this.$notify(
                {
                    component: O24NotificationMessage,
                    message: 'Edit Success',
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
                        alert(msg);
                    } else {
                        this.loadCredentials();
                    }
                    })
                    .catch(error => {
                        var msg = "Error deleting " + error;
                        alert(msg);
                    });
            }
        },
        addAccount(){
            this.$modal.show(AccountAdd, {
            api_url : CREDENTIALS_API_ADD,
            valueUpdated:(newValue) => {
                this.$notify(
                {
                    component: O24NotificationMessage,
                    message: 'Account added success',
                    icon: 'nc-icon nc-bulb-63',
                    type: 'success'
                });
                this.loadCredentials();
            }
            },
            {
                width: '720',
                height: 'auto'
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
</style>
