<template>
  <div ref="map" style="width: 100%; height: 100vh"></div>
</template>

<script>
import gmapsInit from '../../utils/gmaps';

export default {
  name: 'content-map',
  data() {
    return {
      key: '',
    };
  },
  async mounted() {
    try {
      const google = await gmapsInit();
      const mapCenter = {
        lat: 39.589931,
        lng: -95.009003,
      };
      const map = new google.maps.Map(this.$refs.map, {
        center: mapCenter,
        zoom: 3,
      });
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style scoped>

</style>