<template>
  <div>

      <card>
        <div class="col-12 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-air-baloon"></i> Dashboard
          </h3>
        </div>
        <card>
          <youtube
            :video-id="videoId"
            player-width="750"
            player-height="400"
            :player-vars="{host: 'https://www.youtube.com'}"
          ></youtube>
        </card>
      </card>

  </div>
</template>
<script>
import { getIdFromURL, getTimeFromURL } from "vue-youtube-embed";
export default {
  data() {
    return {
      videoId: ""
      //domain: 'http://192.168.0.104:8080/'
    };
  },
  methods: {},
  mounted() {
    this.videoId = getIdFromURL(
      "https://www.youtube.com/watch?v=9AwsM4Cuyrw"
    );
  }
};
</script>
<style>
</style>
