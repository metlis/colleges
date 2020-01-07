<template>
  <v-row dense>
    <!--  Header  -->
    <v-col cols="12">
      <h3>{{header}}</h3>
    </v-col>
    <!--  Map  -->
    <v-col cols="12">
      <div
        :class="$style.map"
        ref="map"
        id="map"
      />
    </v-col>
  </v-row>
</template>

<script>
import init from '../../utils/mapsInit';
import { selectColleges, addCommas } from '../../utils/helpers';

export default {
  name: 'content-map',
  props: ['colleges', 'menu', 'header'],
  data() {
    return {
      vendor: '',
      key: '',
      markers: '',
      map: '',
      selectedColleges: this.colleges,
      lat: 39.589931,
      lng: -95.009003,
      zoom: 3,
    };
  },
  methods: {
    getCollegesList() {
      return selectColleges(this.colleges, this.menu);
    },
    createMarkerText(college) {
      return `<h3>${college.name}</h3>
      <p><span class="icon-container"><i class="fab fa-internet-explorer" data-toggle="tooltip" data-placement="top"></i></span>: <a href="/institution/${college.id}/${college.slug}">College page</a></p>
      <p><span class="icon-container"><i class="fas fa-map-marker-alt" data-toggle="tooltip" data-placement="top"></i></span>: ${college.city}, ${college.state__name}</p>
      <p><span class="icon-container"><i class="fas fa-city" data-toggle="tooltip" data-placement="top"></i></span>: ${college.locale__description}</p>
      <p><span class="icon-container"><i class="fas fa-user-graduate" data-toggle="tooltip" data-placement="top"></i></span>: ${addCommas(college.undergrad_students)}</p>
      <p><span class="icon-container"><i class="fas fa-home" data-toggle="tooltip" data-placement="top"></i></span>: ${college.ownership__description}</p>`;
    },
    updateCollegesList() {
      this.selectedColleges = this.getCollegesList();
      // update google map
      if (this.vendor.maps) {
        this.deleteGmapMarkers();
        this.createGmapMarkers();
      // update yandex map
      } else {
        this.deleteYmapMarkers();
        this.createYmapMarkers();
      }
    },
    addCommas(num) {
      return addCommas(num);
    },
    // google maps methods
    createGmapMarkers() {
      const { vendor } = this;
      this.markers = this.selectedColleges.map((college) => {
        const contentString = `
            <div class="mapInfo">
            ${this.createMarkerText(college)}
            </div>
        `;
        const infoWindow = new vendor.maps.InfoWindow({
          content: contentString,
        });
        const marker = new vendor.maps.Marker({
          position: {
            lat: Number(college.latitude),
            lng: Number(college.longitude),
          },
          title: `${college.name}\n${college.city}, ${college.state__name}`,
          map: this.map,
        });
        vendor.maps.event.addListener(marker, 'click', () => {
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
    // yandex maps methods
    createYmapMarkers() {
      const { vendor } = this;
      const clusterer = new vendor.Clusterer({
        preset: 'islands#invertedBlueClusterIcons',
        clusterHideIconOnBalloonOpen: false,
        geoObjectHideIconOnBalloonOpen: false,
      });
      this.markers = this.selectedColleges.map((college) => {
        const point = [Number(college.latitude), Number(college.longitude)];
        const pointData = {
          balloonContentBody: this.createMarkerText(college),
          clusterCaption: `<strong>${college.name}</strong>`,
        };
        return new vendor.Placemark(point, pointData);
      });
      clusterer.add(this.markers);
      this.map.geoObjects.add(clusterer);
    },
    deleteYmapMarkers() {
      this.map.geoObjects.removeAll();
    },
  },
  async mounted() {
    try {
      this.vendor = await init();
      const { vendor } = this;
      // google map
      if (vendor.maps) {
        const mapCenter = {
          lat: this.lat,
          lng: this.lng,
        };
        this.map = new vendor.maps.Map(this.$refs.map, {
          center: mapCenter,
          zoom: this.zoom,
        });
        this.createGmapMarkers();
      // yandex map
      } else {
        const mapCenter = [this.lat, this.lng];
        this.map = new vendor.Map('map', {
          center: mapCenter,
          zoom: this.zoom,
        });
        this.createYmapMarkers();
      }
    } catch (error) {
      console.error(error);
    }
  },
  watch: {
    colleges() {
      this.updateCollegesList();
    },
    'menu.restore': function (val) {
      if (val) {
        this.selectedColleges = this.colleges;
        this.updateCollegesList();
      }
    },
    'menu.checkboxFilters': function () {
      this.updateCollegesList();
    },
    'menu.statesFilters': function () {
      this.updateCollegesList();
    },
    'menu.rangeFilters': function () {
      this.updateCollegesList();
    },
  },
};
</script>

<style lang="stylus" module>
  .map
    width 100%
    height 100vh
</style>