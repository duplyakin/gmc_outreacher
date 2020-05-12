<template>
  <div>
    <h3 class="text-center">Preview & Start</h3>
    <card>
      <h4 class="text-center">Step 0</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign name:</p>
          {{this.campaign.title}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign type:</p>
          {{this.campaign.funnel}}
        </h5>
      </div>
    </card>
    <card>
      <h4 class="text-center">Step 1</h4>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign account:</p>
          {{this.campaign.credentials}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Campaign prospects:</p>
          {{this.campaign.prospectsList}}
        </h5>
      </div>
    </card>
    <div
      v-if="email_data.templates.length != 0"
    >
      <card>
        <h4 class="text-center">Step 2 Email</h4>
        <div class="typo-line">
          <h5>
            <p class="category">Content:</p>
          </h5>
        </div>
        <ul id="days">
          <li v-for="item in email_data.templates" :key="item.id">
            Subject: {{ item.subject }}
            Interval: {{ item.interval }}
          </li>
        </ul>
      </card>
    </div>
    <div
      v-if="linkedin_data.templates.length != 0"
    >
      <card>
        <h4 class="text-center">Step 2 Linkedin</h4>
        <div class="typo-line">
          <h5>
            <p class="category">Content:</p>
          </h5>
        </div>
        <ul id="days">
          <li v-for="item in linkedin_data.templates" :key="item.id">
            Message: {{ item.message }}
            Interval: {{ item.interval }}
          </li>
        </ul>
      </card>
    </div>
    <card>
      <h4 class="text-center">Step 3</h4>
      <div class="typo-line">
        <h5>
          <p class="category">From:</p>
          {{this.campaign.timeTable.from_hour}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Till:</p>
          {{this.campaign.timeTable.to_hour}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Timezone:</p>
          {{this.campaign.timeTable.time_zone}}
        </h5>
      </div>
      <div class="typo-line">
        <h5>
          <p class="category">Delivery days:</p>
          {{this.campaign.timeTable.sending_days}}
        </h5>
      </div>
    </card>
  </div>
</template>
<script>
import { mapFields } from "vee-validate";
import { Table, TableColumn, Select, Option } from "element-ui";
import axios from '@/api/axios-auth';;

const CAMPAIGN_API_CREATE = "http://127.0.0.1:5000/campaign/create";

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

    };
  },
  methods: {
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
};
</script>
<style>
</style>
