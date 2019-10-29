<template>
  <div ref="map" style="width: 100%; height: 100vh"></div>
</template>

<script>
import gmapsInit from '../../utils/gmaps';

export default {
  name: 'content-map',
  props: ['colleges'],
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
      const markers = this.colleges.map((college) => {
        const marker = new google.maps.Marker({
          position: {
            lat: Number(college.latitude),
            lng: Number(college.longitude),
          },
          title: `${college.name}\n${college.city}, ${college.state__name}`,
          map,
        });
        return marker;
      });
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style scoped>

</style>