<template>
  <div>
    <h3 class="text-center">Preview & Start</h3>
    <card>
      <h4 class="text-center">Step 0</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign name:</p>
          {{this.$store.state.campaign.name}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign type:</p>
          {{this.$store.state.campaign.funnel}}
        </h5>
      </div>
    </card>
    <card>
      <h4 class="text-center">Step 1</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign account:</p>
          {{this.$store.state.campaign.account}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign prospects:</p>
          {{this.$store.state.campaign.prospectsList}}
        </h5>
      </div>
    </card>
    <card>
      <div v-if="this.$store.state.campaign.funnel === this.funnel_email || this.$store.state.campaign.funnel === this.funnel_email_linkedin">
      <h4 class="text-center">Step 2 Email</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Content:</p>
        </h5>
      </div>
      <ul id="days">
        <li v-for="item in this.$store.state.campaign.messagesListEmail" :key="item.id">
          Day {{ item.id }}:
          Subject: {{ item.subject }}
          Interval: {{ item.interval }}
        </li>
      </ul>
      </div>
    </card>
    <card>
      <div v-if="this.$store.state.campaign.funnel === this.funnel_linkedin || this.$store.state.campaign.funnel === this.funnel_email_linkedin">
      <h4 class="text-center">Step 2 Linkedin</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Content:</p>
        </h5>
      </div>
      <ul id="days">
        <li v-for="item in this.$store.state.campaign.messagesListLinkedin" :key="item.id">
          Day {{ item.id }}:
          Subject: {{ item.subject }}
          Interval: {{ item.interval }}
        </li>
      </ul>
      </div>
    </card>
    <card>
      <h4 class="text-center">Step 3</h4>
      <div class="typo-line">
        <h5>
          <p class="category">From:</p>
          {{this.$store.state.campaign.timeTable.from}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Till:</p>
          {{this.$store.state.campaign.timeTable.till}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Timezone:</p>
          {{this.$store.state.campaign.timeTable.timezone}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Delivery days:</p>
        </h5>
      </div>
      <ul id="days">
        <li
          v-for="item in this.$store.state.campaign.timeTable.days"
          :key="item.day"
        >{{ item.day }} : {{ item.active }}</li>
      </ul>
    </card>
  </div>
</template>
<script>
import { mapFields } from "vee-validate";
import { Table, TableColumn, Select, Option } from "element-ui";
import axios from 'axios'

const CAMPAIGN_API_CREATE = 'http://127.0.0.1:5000/campaign/create';

export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  //props: {
  //campaignName: String,
  //campaignType: String,
  //},
  data() {
    return {
      funnel_email: 'Email campaign',
      funnel_linkedin: 'LinkedIn campaign',
      funnel_email_linkedin: 'Email & LinkedIn campaign',
      //campaignName: this.$store.state.campaign.name, // not working
      messages_data_preview: {}
    };
  },
  methods: {
    getError(fieldName) {
      return this.errors.first(fieldName);
    },
    sendData(campaign) {
      const path = this.CAMPAIGN_API_CREATE;

      if (confirm("Are you sure?")) {
        var campaignData = new FormData();
        campaignData.append("_campaign", JSON.stringify(campaign));

        axios
          .post(path, campaignData)
          .then(res => {
            var result = res.data;
            if (result.code > 0) {
              var updated_campaign = JSON.parse(result.updated);
              this.$emit("close");
              this.valueUpdated(updated_campaign);
            } else {
              var msg = "Error editing campaign " + result.msg;
              alert(msg);
            }
          })
          .catch(error => {
            var msg = "Error editing campaign " + error;
            alert(msg);
          });
      }
    },
    validate() {
      this.sendData(this.$store.state.campaign);
      return this.$validator.validateAll().then(res => {
        this.$emit("on-validated", res, this.model);
        return res;
      });
    }
  }
};
</script>
<style>
</style>
