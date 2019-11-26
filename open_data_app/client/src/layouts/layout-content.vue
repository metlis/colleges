<template>
  <v-row class="mx-0" ref="top">
    <!--  Left Navigation Menu  -->
    <v-col
      :class="classes.navigationMenu"
      class="pa-0"
      xs="12"
      sm="12"
      md="2"
    >
      <menu-navigation @navigationClick="changeNavButton" />
    </v-col>
    <!--  Content Area  -->
    <v-col
      v-show="!mobileMenu"
      class="px-md-12"
      xs="12"
      sm="12"
      md="8"
    >
      <v-content>
        <v-container fluid class="pa-0">
          <!-- A list of favourite colleges -->
          <content-colleges-favourite
            ref="colleges-favourite"
            v-show="activeNavButton === 'Colleges'"
            :colleges.sync="fetchedColleges"
            :activeSortButton="contentColleges.activeSortButton"
            :prevSortButton="contentColleges.prevSortButton"
            :checkboxFilters="contentColleges.checkboxFilters"
            :statesFilters="contentColleges.statesFilters"
            :rangeFilters="contentColleges.rangeFilters"
            :restore="contentColleges.restore"
          />
          <!-- A map with colleges -->
          <content-map
            ref="map"
            v-show="activeNavButton === 'Map'"
            :colleges="fetchedColleges"
            :checkboxFilters="contentMap.checkboxFilters"
            :statesFilters="contentMap.statesFilters"
            :rangeFilters="contentMap.rangeFilters"
            :restore="contentMap.restore"
          />
        </v-container>
      </v-content>
    </v-col>
    <!--  Right Filter Menu  -->
    <v-col
      :class="classes.filterMenu"
      xs="12"
      sm="12"
      md="2"
    >
      <!--  Right Sort/Filter Menu for Colleges  -->
      <menu-filter-colleges-favourite
        v-if="activeNavButton === 'Colleges'"
        :colleges="fetchedColleges"
        @sortClick="changeSortButton('contentColleges', 'colleges-sort-click', $event)"
        @checkboxFilterChanged=
          "updateFiltersValues('contentColleges', 'checkboxFilters', 'colleges-checkbox-click',
          $event)"
        @statesFilterChanged=
          "updateFiltersValues('contentColleges', 'statesFilters', 'colleges-state-click', $event)"
        @rangeFilterChanged=
          "updateFiltersValues('contentColleges', 'rangeFilters', 'colleges-range-input', $event)"
        @restore="clearFilters('contentColleges')"
      />
      <!--  Right Filter Menu for Map  -->
      <menu-filter-map
        v-if="activeNavButton === 'Map'"
        :colleges="fetchedColleges"
        @checkboxFilterChanged=
          "updateFiltersValues('contentMap', 'checkboxFilters', 'map-checkbox-click', $event)"
        @statesFilterChanged=
          "updateFiltersValues('contentMap', 'statesFilters', 'map-state-click', $event)"
        @rangeFilterChanged=
          "updateFiltersValues('contentMap', 'rangeFilters', 'map-range-input', $event)"
        @restore="clearFilters('contentMap')"
      />
    </v-col>
    <!--  Mobile button for the menus  -->
    <v-speed-dial
      v-if="!fabClose"
      v-model="fab"
      fixed
      bottom
      right
      direction="top"
      transition="slide-y-reverse-transition"
      class="d-inline-block d-md-none"
    >
      <template v-slot:activator>
        <v-btn
          v-model="fab"
          fab
          color="blue darken-2"
        >
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else >mdi-tools</v-icon>
        </v-btn>
      </template>
      <v-btn
        fab
        dark
        small
        color="green"
      >
        <v-icon @click="showMenu('filterMenu')">mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        color="indigo"
      >
        <v-icon @click="showMenu('navigationMenu')">mdi-menu</v-icon>
      </v-btn>
    </v-speed-dial>
    <!--  Close button  -->
    <v-btn
      v-if="fabClose"
      fab
      fixed
      bottom
      right
      color="red"
    >
      <v-icon @click="hideMenu">mdi-close</v-icon>
    </v-btn>
  </v-row>
</template>

<script>
import goTo from 'vuetify/es5/services/goto';
import MenuNavigation from '../components/menus/menu-navigation.vue';
import MenuFilterCollegesFavourite from '../components/menus/menu-filter-colleges-favourite.vue';
import MenuFilterMap from '../components/menus/menu-filter-map.vue';
import ContentCollegesFavourite from '../components/contents/content-colleges-favourite.vue';
import ContentMap from '../components/contents/content-map.vue';

export default {
  name: 'content-layout',
  components: {
    MenuNavigation,
    MenuFilterCollegesFavourite,
    MenuFilterMap,
    ContentCollegesFavourite,
    ContentMap,
  },
  props: ['colleges'],
  data() {
    return {
      fetchedColleges: this.colleges,
      activeNavButton: 'Colleges',
      classes: {
        navigationMenu: 'd-none d-md-block',
        filterMenu: 'd-none d-md-block',
      },
      mobileMenu: false,
      fab: false,
      fabClose: false,
      contentColleges: {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        restore: false,
      },
      contentMap: {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        restore: false,
      },
    };
  },
  methods: {
    changeNavButton(val) {
      this.activeNavButton = val;
    },
    changeSortButton(page, event, val) {
      if (this[page].activeSortButton) {
        this[page].prevSortButton = this[page].activeSortButton;
      }
      this[page].activeSortButton = val;
      setTimeout(() => {
        this.$root.$emit(event);
      }, 0);
    },
    updateFiltersValues(page, filter, event, val) {
      this[page][filter] = val;
      this[page].restore = false;
      setTimeout(() => {
        this.$root.$emit(event);
      }, 0);
    },
    clearFilters(page) {
      this[page] = Object.assign({}, this[page], {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        restore: true,
      });
      goTo(this.$refs.top);
    },
    showMenu(menu) {
      if (menu && this.classes[menu] && this.classes[menu].indexOf('d-none') > -1) {
        this.classes[menu] = 'd-block';
        this.mobileMenu = true;
        this.fabClose = true;
        goTo(this.$refs.top);
      } else {
        this.hideMenu();
      }
    },
    hideMenu() {
      this.classes.filterMenu = 'd-none d-md-block';
      this.classes.navigationMenu = 'd-none d-md-block';
      this.mobileMenu = false;
      this.fab = false;
      this.fabClose = false;
    },
  },
};
</script>

<style scoped>
</style>