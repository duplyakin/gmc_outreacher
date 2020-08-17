<template>
  <div>
    <b-container fluid class="mb-5">
      <b-row class="no-gutters">
        <b-col cols="6" md="auto">
          <h4 class="ml-3">Choose Campaign type</h4>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row align-h="center" class="justify-content-md-center">

        <h2>What type of campaign do you want to create?</h2>

        <b-card-group class="mt-3">
          <a @click="$router.push({ path: '/campaign_data_form_type' })">
            <b-card class="mr-3 mb-3">
              <b-card-body class="text-center mx-4">
                <b-card-text>Data enrichment</b-card-text>
                <b-card-text>Enrich leads (emails, LinkedIn accounts and personal data) from LinkedIn</b-card-text>
              </b-card-body>
            </b-card>
          </a>

          <a @click="$router.push({ path: '/campaign_form_type' })">
            <b-card class="mr-3 mb-3">
              <b-card-body class="text-center mx-4">
                <b-card-text>Outreach</b-card-text>
                <b-card-text>Create sequences to contact your leads</b-card-text>
              </b-card-body>
            </b-card>
          </a>
        </b-card-group>

      </b-row>
    </b-container>

  </div>
</template>
<script>
export default {
  components: {

  },
  data() {
    return {

    };
  },
  methods: {

  },
  async mounted() {
  }
};
</script>
<style>

</style>
