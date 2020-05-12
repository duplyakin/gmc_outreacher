<template>
  <div>
    <div class="row">
      <card>
        <youtube :video-id="videoId" player-width="750" player-height="400" :player-vars="{host: 'https://www.youtube.com'}"></youtube>
      </card>
    </div>
  </div>
</template>
<script>
import { getIdFromURL, getTimeFromURL } from "vue-youtube-embed";
export default {
  data() {
    return {
      videoId: '',
      //domain: 'http://192.168.0.104:8080/'
    };
  },
  methods: {
  },
  mounted() {
    this.videoId = getIdFromURL("https://www.youtube.com/watch?v=6pqOZq9eBBg&list=LLFo6SCt0GGcF5D7c-yGNuUQ&index=18&t=0s");
  }
};
</script>
<style>
</style>
