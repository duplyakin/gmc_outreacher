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
          {{this.credentials}}
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
import axios from "axios";

const CAMPAIGNS_API_CREATE = "http://127.0.0.1:5000/campaigns/create";

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  props: {
    campaign: Object,
    email_data: Object,
    linkedin_data: Object
  },
  data() {
    return {
        credentials: [],
    };
  },
  methods: {
    submit(){
        this.createCampaign();
    },
    discard() {
      this.$emit("close");
    },
    credentialsDefine() {
        if (this.email_data.email_account_selected.length != 0) {
        console.log("email account");
        console.log(this.email_data.email_account_selected);

        this.credentials.push(this.email_data.email_account_selected);
      }

      if (this.linkedin_data.linkedin_account_selected.length != 0) {
        console.log("linkedin account");
        console.log(this.linkedin_data.linkedin_account_selected);

        this.credentials.push(this.linkedin_data.linkedin_account_selected);
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
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    validate() {
      return this.$validator.validateAll().then(res => {
        this.$emit("on-validated", res, this.model);
        return res;
      });
    }
  },
  created() {
      this.credentialsDefine();
  }
};
</script>
<style>
</style>
