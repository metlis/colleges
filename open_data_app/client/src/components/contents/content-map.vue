<template>
  <div ref="map" :class="$style.map"></div>
</template>

<script>
import gmapsInit from '../../utils/gmaps';
import { selectColleges, addCommas } from '../../utils/helpers';

export default {
  name: 'content-map',
  props: ['colleges', 'checkboxFilters', 'statesFilters', 'rangeFilters', 'restore'],
  data() {
    return {
      google: '',
      key: '',
      markers: '',
      map: '',
      selectedColleges: this.colleges,
    };
  },
  methods: {
    getCollegesList() {
      return selectColleges(this.colleges, {
        checkboxFilters: this.checkboxFilters,
        statesFilters: this.statesFilters,
        rangeFilters: this.rangeFilters,
      });
    },
    createGmapMarkers() {
      const { google } = this;
      this.markers = this.selectedColleges.map((college) => {
        const contentString = `
            <div class="mapInfo">
            <h4>${college.name}</h4>
            <p><span class="icon-container"><i class="fab fa-internet-explorer" data-toggle="tooltip" data-placement="top"></i></span>: <a href="/institution/${college.id}/${college.slug}">College page</a></p>
            <p><span class="icon-container"><i class="fas fa-map-marker-alt" data-toggle="tooltip" data-placement="top"></i></span>: ${college.city}, ${college.state__name}</p>
            <p><span class="icon-container"><i class="fas fa-city" data-toggle="tooltip" data-placement="top"></i></span>: ${college.locale__description}</p>
            <p><span class="icon-container"><i class="fas fa-user-graduate" data-toggle="tooltip" data-placement="top"></i></span>: ${addCommas(college.undergrad_students)}</p>
            <p><span class="icon-container"><i class="fas fa-home" data-toggle="tooltip" data-placement="top"></i></span>: ${college.ownership__description}</p>
            </div>
        `;
        const infoWindow = new google.maps.InfoWindow({
          content: contentString,
        });
        const marker = new google.maps.Marker({
          position: {
            lat: Number(college.latitude),
            lng: Number(college.longitude),
          },
          title: `${college.name}\n${college.city}, ${college.state__name}`,
          map: this.map,
        });
        google.maps.event.addListener(marker, 'click', () => {
          infoWindow.open(this.map, marker);
        });
        return marker;
      });
    },
    deleteGmapMarkers() {
      this.markers.forEach((marker) => {
        marker.setMap(null);
      });
    },
    updateCollegesList() {
      this.selectedColleges = this.getCollegesList();
      this.deleteGmapMarkers();
      this.createGmapMarkers();
    },
    addCommas(num) {
      return addCommas(num);
    },
  },
  async mounted() {
    try {
      this.google = await gmapsInit();
      const { google } = this;
      const mapCenter = {
        lat: 39.589931,
        lng: -95.009003,
      };
      this.map = new google.maps.Map(this.$refs.map, {
        center: mapCenter,
        zoom: 3,
      });
      this.createGmapMarkers();
    } catch (error) {
      console.error(error);
    }
  },
  watch: {
    restore(val) {
      if (val) {
        this.selectedColleges = this.colleges;
        this.updateCollegesList();
      }
    },
  },
  created() {
    this.$root.$on('map-checkbox-click', () => {
      this.updateCollegesList();
    });
    this.$root.$on('map-state-click', () => {
      this.updateCollegesList();
    });
    this.$root.$on('map-range-input', () => {
      this.updateCollegesList();
    });
  },
};
</script>

<style lang="stylus" module>
  .map
    width 100%
    height 100vh
</style>