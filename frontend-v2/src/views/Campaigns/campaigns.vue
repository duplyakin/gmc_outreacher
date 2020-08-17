<template>
<div>
<card>
    <div class="container">
        <div class="row">
            <div class="col-4 d-flex align-self-center">
                <h3>
                <i class="nc-icon nc-bullet-list-67"></i> Campaigns
                </h3>
            </div>
            <div class="col-8 d-flex flex-row-reverse align-self-center">
                <button
                    @click.prevent="addCampaign"
                    type="button"
                    class="btn btn-default btn-success mx-1"
                >Create a Campaign</button>
                <button
                    @click.prevent="reload_campaigns"
                    type="button"
                    class="btn btn-default btn-success mx-1"
                >Refresh</button>
            </div>
        </div>
    </div>
</card>

<card>
        <div class="col-12">
            <pulse-loader :loading="loading" :color="color"></pulse-loader>
        </div>

        </card>

        <div v-if="test" class="row">
            <div class="col-12">
                <pre>{{ this.campaigns_data}}</pre>
            </div>

            <div class="col-12">
                {{ this.list_data }}
            </div>
        </div>

</div>
</template>
<script>
import axios from '@/api/axios-auth';

const CAMPAIGNS_API_EDIT = "/campaigns/edit";

const CAMPAIGNS_API_DATA = '/campaigns/data'
const CAMPAIGNS_API_LIST = '/campaigns/list';

const CAMPAIGNS_API_DELETE = '/campaigns/delete';
const CAMPAIGNS_API_START = '/campaigns/start';
const CAMPAIGNS_API_PAUSE = '/campaigns/pause';

export default {
components: {

},
computed: {
},
data() {
    return {
        test : false,

        loading: true,
        color: "#a7a7ff",
        
        status : {
            0 : 'New',
            1 : 'In progress',
            2 : 'On Pause',
           '-1' : 'Failed',
           '-2' : 'Unknown'
        },
        pagination : {
            perPage : 0,
            currentPage : 1,
            perPageOptions: [5, 10, 25, 50],
            total : 0
        },
        list_data : {
            columns : [],
        },
        campaigns_data : {
            campaigns : []
        }
    };
},
methods: {
    detalization(campaign_id) {
      this.$router.push({path: "campaign_statistic", query: { campaign_id: campaign_id }});
    },
    make_action(campaign){
        var path = CAMPAIGNS_API_START;
        if (campaign.status == 1){
            path = CAMPAIGNS_API_PAUSE;
        }
        if (confirm("Are you sure?")) {
            var data = new FormData();
            data.append("_campaign_id", campaign._id.$oid);

            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Action error " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_campaigns();
                }
                })
                .catch(error => {
                    var msg = "Action error " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
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
    },
    delete_campaign(campaign_id){
        if (confirm("Are you sure?")) {
            const path = CAMPAIGNS_API_DELETE;

            var data = new FormData();
            data.append("_campaign_id", campaign_id);

            axios
                .post(path, data)
                .then(res => {
                var r = res.data;
                if (r.code <= 0) {
                    var msg = "Error deleting campaign " + r.msg;
                    Notification.error({title: "Error", message: msg});
                } else {
                    this.load_campaigns();
                }
                })
                .catch(error => {
                    var msg = "Error deleting campaign " + error;
                    Notification.error({title: "Error", message: msg});
                });
        }
    },
    addCampaign() {
        this.$router.push({path: "campaign_form_start"});
    },
    editCampaign(msg_dict) {
        var status = -2;
        if (Object.prototype.hasOwnProperty.call(msg_dict, "status")){
            status = msg_dict['status'];
        }
        if (status == -2 || status == 1){
            Notification.error({title: "Error", message: "Pause campaign for edit, current status: " + status});
            return false;
        }

        let path = CAMPAIGNS_API_EDIT
        let data = new FormData()

        data.append("action", "edit")
        data.append("campaign_id", msg_dict._id.$oid)

        axios
            .post(path, data)
            .then(res => {
            let r = res.data
            if (Object.prototype.hasOwnProperty.call(r, "error") && r.error !== 0) {
                let msg = "Error loading data " + r.msg + " Error:" + r.error
                Notification.error({ title: "Error", message: msg })
            } else {
                if (Object.prototype.hasOwnProperty.call(r, "next_step") && r.next_step) {
                    this.$router.push({ path: r.next_step, query: { action_type: 'edit' } })
                } else {
                    Notification.error({ title: "Error", message: 'Server error: no next step' })
                }
            }
            })
            .catch(error => {
                let msg = "Error loading data. ERROR: " + error
                Notification.error({ title: "Error", message: msg })
            })
    },
    next_page(){
        var page = 2;
        this.load_data(page,0);
    },
    reload_campaigns(){
        return this.load_campaigns(1);
    },
    load_campaigns(page=1){
        const path = CAMPAIGNS_API_LIST;

        var data = new FormData();
        data.append('_page', page);

        axios.post(path, data)
        .then((res) => {
            var r = res.data;
            if (r.code <= 0){
                var msg = "Error loading campaigns." + r.msg;
                Notification.error({title: "Error", message: msg});
            }else{
                this.deserialize_campaigns(r);
            }
            })
            .catch((error) => {
                var msg = "Error loading campaigns. ERROR: " + error;
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
            if (Object.prototype.hasOwnProperty.call(this.list_data, key) && from_data[key]){
                var parsed_data = JSON.parse(from_data[key])
                this.$set(this.list_data, key, parsed_data);
            }
        }
    },
    deserialize_campaigns(from_data){
        if (from_data.pagination){
            var pagination_dict = JSON.parse(from_data.pagination);
            this.$set(this, 'pagination', pagination_dict);
        }

        if (from_data.columns){
            var columns = JSON.parse(from_data.columns);
            this.$set(this.list_data, 'columns', columns);
        }

        if (from_data.campaigns){
            var campaigns = JSON.parse(from_data.campaigns)
            this.$set(this.campaigns_data, 'campaigns', campaigns);
        }

        this.loading = false
    },

},
async mounted() {
    await this.load_campaigns()
}
}; 
</script>
<style>
</style>
