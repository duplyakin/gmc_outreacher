<template>
  <div>
    <h3 class="text-center">Preview & Start</h3>
    <card>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign name:</p>
          {{this.campaign.title}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign funnel:</p>
          {{this.campaign.funnel.title}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Credentials:</p>
          <ul>
              <li v-if="email_acc !== ''">{{email_acc}}</li>
              <li v-if="linkedin_acc !== ''">{{linkedin_acc}}</li>
          </ul>
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Prospects list:</p>
          {{this.campaign.prospects_list.title}}
        </h5>
      </div>
    </card>

    <div class="col-8 d-flex flex-row-reverse align-self-center">
        <div>
        <button @click.prevent="discard()" type="button" class="btn btn-outline btn-wd btn-danger">Back</button>
          <button
            @click.prevent="submit()"
            type="button"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Save</button>
        </div>
      </div>
  </div>
</template>
<script>
import { mapFields } from "vee-validate";
import { Table, TableColumn, Select, Option } from "element-ui";
import axios from '@/api/axios-auth';;
import Campaigns from "./campaigns.vue";

const CAMPAIGNS_API_CREATE = "/campaigns/create";
const CAMPAIGNS_API_EDIT = "/campaigns/edit";

export default {
  components: {
    Campaigns,
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  props: {
    modified_fields: Object,
    campaign_id: String,
    action_type: String,
    campaign: Object,
    email_data: Object,
    linkedin_data: Object
  },
  data() {
    return {
        credentials: [],
        email_acc: '',
        linkedin_acc: '',
    };
  },
  methods: {
    submit(){
      if(this.action_type == 'edit'){
        this.editCampaign();
      } 
      if(this.action_type == 'add') {
        this.createCampaign();
      }
    },
    discard() {
      this.$emit("close");
    },
    credentialsDefine() {
        if (this.email_data.email_account_selected.length != 0) {
        console.log("email account");
        console.log(this.email_data.email_account_selected);

        this.credentials.push(this.email_data.email_account_selected);
        this.email_acc = this.credentials.find(x => x.medium == 'email').data.account;
      }

      if (this.linkedin_data.linkedin_account_selected.length != 0) {
        console.log("linkedin account");
        console.log(this.linkedin_data.linkedin_account_selected);

        this.credentials.push(this.linkedin_data.linkedin_account_selected);
        this.linkedin_acc = this.credentials.find(x => x.medium == 'linkedin').data.account;
      }
    },
    createCampaign() {
      const path = CAMPAIGNS_API_CREATE;

      this.campaign.templates.email = this.email_data.templates;
      this.campaign.templates.linkedin = this.linkedin_data.templates;
      this.campaign.credentials = this.credentials;
      console.log("RESALT CAMPAIGN: ");
      console.log(this.campaign);

      var createData = new FormData();
      createData.append("_add_campaign", JSON.stringify(this.campaign));

      console.log(createData);
      axios
        .post(path, createData)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error creating campaign " + r.msg;
            alert(msg);
          } else {
              this.$emit('close');
              this.$router.push("Campaigns").catch(err => {
                console.log(err);
              });
          }
        })
        .catch(error => {
          var msg = "Error creating campaign " + error;
          alert(msg);
        });
    },
    editCampaign() {
      const path = CAMPAIGNS_API_EDIT;

      this.campaign.templates.email = this.email_data.templates;
      this.campaign.templates.linkedin = this.linkedin_data.templates;
      this.campaign.credentials = this.credentials;
      console.log("RESALT EDIT CAMPAIGN: ");
      console.log(this.campaign);

      var createData = new FormData();
      createData.append("_campaign_id", JSON.stringify(this.campaign_id));
      createData.append("_modified_fields", JSON.stringify(this.modified_fields));
      createData.append("_edit_campaign_data", JSON.stringify(this.campaign));

      console.log(createData);
      axios
        .post(path, createData)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error creating campaign " + r.msg;
            alert(msg);
          } else {
              this.$emit('close');
              this.$router.push("Campaigns").catch(err => {
                console.log(err);
              });
          }
        })
        .catch(error => {
          var msg = "Error creating campaign " + error;
          alert(msg);
        });
    },
  },
  created() {
      this.credentialsDefine();
  }
};
</script>
<style>
</style>
