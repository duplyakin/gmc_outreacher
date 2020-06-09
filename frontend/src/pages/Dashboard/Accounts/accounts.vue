<template>
<div>
    <card>
    <div class="row">
        <div class="col-6 d-flex align-self-center">
            <span font-><h3><i class="nc-icon nc-single-02"></i>Accounts managment</h3></span>
        </div>
        <div class="col-6 d-flex flex-row-reverse align-self-center">
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
                <el-table-column :min-width="80" fixed="right">
                    <template slot-scope="props">
                    <a
                        v-tooltip.top-center="'Reconnect'"
                        class="btn-info btn-simple btn-link"
                        @click.prevent="loginLinkedinModal(props.row._id.$oid)"
                    >
                        <p class="small green" v-if="props.row.status != -1">Login linkedin</p>
                        <p class="small red" v-if="props.row.status == -1">Login linkedin required</p>
                    </a>
                    </template>
                </el-table-column>
                <el-table-column :min-width="40" fixed="right">
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

<modals-container ref="modal_login"/>
</div>
</template>
<script>
    import { Notification, Table, TableColumn, Select, Option } from 'element-ui'
    import axios from '@/api/axios-auth'
    import * as bs_axios from 'axios'


    const O24Pagination = () => import('src/components/O24Pagination.vue')
    const AccountEdit = () => import('./accountEdit.vue')
    const AccountAdd = () => import('./accountAdd.vue')
    const AccountLogin = () => import('./accountLogin_modal.vue')
    const AccountInput = () => import('./accountInput_modal.vue')

    const CREDENTIALS_API_LIST = '/credentials/list';
    const CREDENTIALS_API_EDIT = '/credentials/edit';
    const CREDENTIALS_API_DELETE = '/credentials/delete';
    const CREDENTIALS_API_ADD = '/credentials/add';
    //const CREDENTIALS_API_REFRESH = '/credentials/refresh';

    const BS_API_STATUS = 'http://127.0.0.1:3000/bs/api/status/';
    const BS_API_LOGIN = 'http://127.0.0.1:3000/bs/api/login/';
    const BS_API_INPUT = 'http://127.0.0.1:3000/bs/api/input/';


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
        async loginLinkedinModal(credentials_id, row_index) {
            this.$modal.show(AccountLogin, {
                credentials_id: credentials_id,
                accountStatusBS: this.accountStatusBS,
                accountLoginBS: this.accountLoginBS,
            },
            {
                width: '620',
                height: 'auto',
                scrollable: true,
                clickToClose: false
            })
        },
        async inputLinkedinModal(credentials_id, screenshot) {
            this.$modal.show(AccountInput, {
                screenshot: screenshot,
                credentials_id: credentials_id,
                accountStatusBS: this.accountStatusBS,
                accountInputBS: this.accountInputBS,
            },
            {
                width: '620',
                height: 'auto',
                scrollable: true,
                clickToClose: false
            })
        },
        async accountInputBS(credentials_id, input) {
            //console.log("accountInputBS started with credentials_id: ", credentials_id);
            const path = BS_API_INPUT;

            var result = {
                credentials_id: credentials_id,
                input: input,
            }

            await bs_axios
                .post(path, result)
                .then(res => {
                    var r = res.data;

                    //console.log("accountInputBS status: ", r.code);

                    if(r.code == -1) {
                        Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                    } else {
                        // ok
                    }

                })
                .catch(error => {
                    console.log("Error status ", error);
                    Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                    this.$emit('close');
                });
        },
        async accountStatusBS(credentials_id) {
            //console.log("accountStatusBS started with credentials_id: ", credentials_id);
            const path = BS_API_STATUS;
            let _this = this;

            var result = {
                credentials_id: credentials_id,
            }

            await bs_axios
                .post(path, result)
                .then(res => {
                    var r = res.data;
                    let status = r.code;

                    //console.log("accountStatusBS status: ", status);

                    if(status == -1) {
                        Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                        this.$refs["modal_login"].modals = [];
                    }

                    if(status == 0) {
                        Notification.success({title: "Success", message: "Success."});
                        this.$refs["modal_login"].modals = [];
                        this.loadCredentials(); // update table
                    }

                    if(status == 1) {
                        setTimeout(async function () {_this.accountStatusBS(credentials_id)}, 3000); // in progress
                    }

                    if(status == 2) {
                        Notification.info({title: "Info", message: "Need action."});
                        this.$refs["modal_login"].modals = [];
                        if(r.screenshot) {
                            this.inputLinkedinModal(credentials_id, r.screenshot);
                        } else {
                            Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                        }
                    }

                    if(status == 4) {
                        Notification.error({title: "Error", message: "Wrong login or password."});
                    }

                })
                .catch(error => {
                    console.log("Error status ", error);
                    Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                    this.inputLinkedinModal(credentials_id);
                });
        },
        async accountLoginBS(credentials_id, login, password) {
            const path = BS_API_LOGIN;
            //console.log("accountLoginBS started with credentials_id: ", credentials_id);

            var result = {
                credentials_id: credentials_id,
                login: login,
                password: password,
            }

            await bs_axios
                .post(path, result)
                .then(res => {
                    var r = res.data;
                    if (r.code == -2) {
                        Notification.error({title: "Error", message: "Empty login or password."});
                    } else if (r.code == 1) {
                        Notification.info({title: "Info", message: "Login in progress."});
                    } else {
                        Notification.error({title: "Error", message: "Something went wrong... Please, contact support."});
                    }
                })
                .catch(error => {
                    Notification.error({title: "Error", message: "Error login " + error});
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
            } else {
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
    }
</script>
<style>
.red {
color: red;
}
.green {
color: rgb(3, 212, 3);
}
</style>
