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
          <content-colleges-list
            ref="colleges-favourite"
            v-show="activeNavButton === 'Colleges'"
            :colleges.sync="favouriteColleges"
            :activeSortButton="contentCollegesFavourite.activeSortButton"
            :prevSortButton="contentCollegesFavourite.prevSortButton"
            :checkboxFilters="contentCollegesFavourite.checkboxFilters"
            :statesFilters="contentCollegesFavourite.statesFilters"
            :rangeFilters="contentCollegesFavourite.rangeFilters"
            :restore="contentCollegesFavourite.restore"
          />
          <!-- A list of visited colleges -->
          <content-colleges-list
            ref="colleges-visited"
            v-show="activeNavButton === 'Visited'"
            :colleges="visitedColleges"
            :activeSortButton="contentCollegesVisited.activeSortButton"
            :prevSortButton="contentCollegesVisited.prevSortButton"
            :checkboxFilters="contentCollegesVisited.checkboxFilters"
            :statesFilters="contentCollegesVisited.statesFilters"
            :rangeFilters="contentCollegesVisited.rangeFilters"
            :restore="contentCollegesVisited.restore"
          />
          <!-- A map with colleges -->
          <content-map
            ref="map"
            v-show="activeNavButton === 'Map'"
            :colleges="favouriteColleges"
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
      <!--  Right Sort/Filter Menu for Favourite Colleges  -->
      <menu-filter-colleges-list
        v-show="activeNavButton === 'Colleges'"
        :colleges="favouriteColleges"
        name="contentCollegesFavourite"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCollegesFavourite')"
      />
      <!--  Right Sort/Filter Menu for Visited Colleges  -->
      <menu-filter-colleges-list
        v-show="activeNavButton === 'Visited'"
        :colleges="visitedColleges"
        name="contentCollegesVisited"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCollegesVisited')"
      />
      <!--  Right Filter Menu for Map  -->
      <menu-filter-map
        v-show="activeNavButton === 'Map'"
        :colleges="favouriteColleges"
        name="contentMap"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
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
import MenuFilterCollegesList from '../components/menus/menu-filter-colleges-list.vue';
import MenuFilterMap from '../components/menus/menu-filter-map.vue';
import ContentCollegesList from '../components/contents/content-colleges-list.vue';
import ContentMap from '../components/contents/content-map.vue';

export default {
  name: 'content-layout',
  components: {
    MenuNavigation,
    MenuFilterCollegesList,
    MenuFilterMap,
    ContentCollegesList,
    ContentMap,
  },
  props: ['favourites', 'visited'],
  data() {
    return {
      favouriteColleges: this.favourites,
      visitedColleges: this.visited,
      activeNavButton: 'Colleges',
      classes: {
        navigationMenu: 'd-none d-md-block',
        filterMenu: 'd-none d-md-block',
      },
      mobileMenu: false,
      fab: false,
      fabClose: false,
      contentCollegesFavourite: {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        restore: false,
      },
      contentCollegesVisited: {
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
    changeSortButton(event) {
      const menu = this[event.menu];
      if (menu.activeSortButton && menu.prevSortButton) {
        this.$set(menu, 'prevSortButton', '');
        this.$set(menu, 'activeSortButton', '');
      }
      if (menu.activeSortButton) {
        this.$set(menu, 'prevSortButton', menu.activeSortButton);
      }
      this.$set(menu, 'activeSortButton', event.value);
    },
    updateFiltersValues(event) {
      const menu = this[event.menu];
      this.$set(menu, 'restore', false);
      this.$set(menu, event.filters, event.value);
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