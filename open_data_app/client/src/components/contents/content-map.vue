<template>
  <div ref="map" style="width: 100%; height: 100vh"></div>
</template>

<script>
import gmapsInit from '../../utils/gmaps';
import { filterColleges } from '../../utils/helpers';

export default {
  name: 'content-map',
  props: ['colleges', 'checkboxFilters', 'statesFilters', 'rangeFilters', 'reset'],
  data() {
    return {
      google: '',
      key: '',
      markers: '',
      map: '',
      filteredColleges: this.colleges,
    };
  },
  methods: {
    getColleges() {
      return filterColleges(this.filteredColleges, {
        checkboxFilters: this.checkboxFilters,
        statesFilters: this.statesFilters,
        rangeFilters: this.rangeFilters,
      });
    },
    createMarkers() {
      const { google } = this;
      this.markers = this.filteredColleges.map((college) => {
        const contentString = `
            <div class="mapInfo">
            <h4>${college.name}</h4>
            <p><span class="icon-container"><i class="fab fa-internet-explorer" data-toggle="tooltip" data-placement="top"></i></span>: <a href="/institution/${college.id}/${college.slug}">College page</a></p>
            <p><span class="icon-container"><i class="fas fa-map-marker-alt" data-toggle="tooltip" data-placement="top"></i></span>: ${college.city}, ${college.state__name}</p>
            <p><span class="icon-container"><i class="fas fa-city" data-toggle="tooltip" data-placement="top"></i></span>: ${college.locale__description}</p>
            <p><span class="icon-container"><i class="fas fa-user-graduate" data-toggle="tooltip" data-placement="top"></i></span>: ${college.undergrad_students}</p>
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
    deleteMarkers() {
      this.markers.forEach((marker) => {
        marker.setMap(null);
      });
    },
    updateColleges() {
      this.filteredColleges = this.getColleges();
      this.deleteMarkers();
      this.createMarkers();
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
      this.createMarkers();
    } catch (error) {
      console.error(error);
    }
  },
  watch: {
    reset(val) {
      if (val) {
        this.filteredColleges = this.colleges;
        this.createMarkers();
      }
    },
  },
  created() {
    this.$root.$on('map-checkbox-click', () => {
      this.updateColleges();
    });
    this.$root.$on('map-state-click', () => {
      this.updateColleges();
    });
    this.$root.$on('map-range-input', () => {
      this.updateColleges();
    });
  },
};
</script>

<style scoped>

</style>