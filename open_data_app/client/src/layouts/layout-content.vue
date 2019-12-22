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
      <menu-navigation
        ref="nav"
        :initial="activeNavButton"
        @navigationClick="updateNavButton"
      />
    </v-col>
    <!--  Content Area  -->
    <v-col
      v-show="!mobileMenu"
      class="px-md-12"
      xs="12"
      sm="12"
      md="8"
      ref="content"
    >
      <v-content>
        <v-container fluid class="pa-0">
          <!-- A list of favourite colleges -->
          <content-colleges-list
            ref="colleges-favourite"
            v-show="activeNavButton === 'Favourite'"
            :colleges="favouriteColleges"
            :favourites.sync="favouriteColleges"
            :menu="filterMenus.contentCollegesFavourite"
            limit="12"
            header="Favourite colleges"
          />
          <!-- A list of visited colleges -->
          <content-colleges-list
            ref="colleges-visited"
            v-show="activeNavButton === 'Visited'"
            :colleges="visitedColleges"
            :favourites.sync="favouriteColleges"
            :menu="filterMenus.contentCollegesVisited"
            limit="12"
            header="Visited colleges"
          />
          <!-- A list of recommended colleges -->
          <content-colleges-list
            ref="colleges-recommended"
            v-show="activeNavButton === 'Recommended'"
            :colleges="recommendedColleges"
            :favourites.sync="favouriteColleges"
            :menu="filterMenus.contentCollegesRecommended"
            limit="12"
            header="Recommended colleges"
          />
          <!-- A map with colleges -->
          <content-map
            ref="map"
            v-show="activeNavButton === 'Map'"
            :colleges="favouriteColleges"
            :menu="filterMenus.contentMap"
            header="Favourite colleges on the map"
          />
          <!-- Comparison of colleges -->
          <content-compare
            ref="compare"
            v-show="activeNavButton === 'Compare'"
            :colleges="favouriteColleges"
            :menu="filterMenus.contentCompare"
            header="Comparison of colleges"
          />
          <!-- History of colleges -->
          <content-history
            ref="history"
            v-show="activeNavButton === 'History'"
            :colleges="favouriteColleges"
            :menu="filterMenus.contentHistory"
            :credentials="credentials"
            header="Historic data"
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
      <menu-filter-and-sort
        v-show="activeNavButton === 'Favourite'"
        :colleges="favouriteColleges"
        name="contentCollegesFavourite"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCollegesFavourite')"
      />
      <!--  Right Sort/Filter Menu for Visited Colleges  -->
      <menu-filter-and-sort
        v-show="activeNavButton === 'Visited'"
        :colleges="visitedColleges"
        name="contentCollegesVisited"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCollegesVisited')"
      />
      <!--  Right Sort/Filter Menu for Recommended Colleges  -->
      <menu-filter-and-sort
        v-show="activeNavButton === 'Recommended'"
        :colleges="recommendedColleges"
        name="contentCollegesRecommended"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCollegesRecommended')"
      />
      <!--  Right Filter Menu for Map  -->
      <menu-filter
        v-show="activeNavButton === 'Map'"
        :colleges="favouriteColleges"
        name="contentMap"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentMap')"
      />
      <!--  Right Filter Menu for Compare  -->
      <menu-filter-and-sort
        v-show="activeNavButton === 'Compare'"
        :colleges="favouriteColleges"
        name="contentCompare"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentCompare')"
      />
      <!--  Right Filter Menu for History  -->
      <menu-filter-and-sort
        v-show="activeNavButton === 'History'"
        :colleges="favouriteColleges"
        name="contentHistory"
        @sortClick="changeSortButton($event)"
        @checkboxFilterChanged="updateFiltersValues($event)"
        @statesFilterChanged="updateFiltersValues($event)"
        @rangeFilterChanged="updateFiltersValues($event)"
        @restore="clearFilters('contentHistory')"
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
import MenuFilterAndSort from '../components/menus/menu-filter-and-sort.vue';
import MenuFilter from '../components/menus/menu-filter.vue';
import ContentCollegesList from '../components/contents/content-colleges-list.vue';
import ContentMap from '../components/contents/content-map.vue';
import ContentCompare from '../components/contents/content-compare.vue';
import ContentHistory from '../components/contents/content-history.vue';

export default {
  name: 'content-layout',
  components: {
    MenuNavigation,
    MenuFilterAndSort,
    MenuFilter,
    ContentCollegesList,
    ContentMap,
    ContentCompare,
    ContentHistory,
  },
  props: ['favourites', 'visited', 'recommended', 'page', 'credentials'],
  data() {
    return {
      favouriteColleges: this.favourites,
      visitedColleges: this.visited,
      recommendedColleges: this.recommended,
      activeNavButton: this.page,
      scorecardApiCredentials: '',
      classes: {
        navigationMenu: 'd-none d-md-block',
        filterMenu: 'd-none d-md-block',
      },
      mobileMenu: false,
      fab: false,
      fabClose: false,
      filterMenus: {
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
        contentCollegesRecommended: {
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
        contentCompare: {
          activeSortButton: '',
          prevSortButton: '',
          checkboxFilters: '',
          statesFilters: '',
          rangeFilters: '',
          restore: false,
        },
        contentHistory: {
          activeSortButton: '',
          prevSortButton: '',
          checkboxFilters: '',
          statesFilters: '',
          rangeFilters: '',
          restore: false,
        },
      },
    };
  },
  methods: {
    updateNavButton(val) {
      this.activeNavButton = val;
    },
    changeSortButton(event) {
      const menu = this.filterMenus[event.menu];
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
      const menu = this.filterMenus[event.menu];
      this.$set(menu, 'restore', false);
      // for some reason, checkbox filters are not reactive without deleting the hole object
      this.$set(menu, event.filters, '');
      this.$set(menu, event.filters, event.value);
    },
    clearFilters(menu) {
      this.filterMenus[menu] = Object.assign({}, this.filterMenus[menu], {
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
  watch: {
    activeNavButton(val) {
      // fetch recommended colleges when the page with recommended colleges
      // is opened for the first time
      if (val === 'Recommended' && this.recommendedColleges.length === 0) {
        this.$emit('fetchRecommendedColleges');
      }
      // fetch scorecard api credentials when the page with history is opened for the first time
      if (val === 'History' && !this.scorecardApiCredentials) {
        this.$emit('fetchScorecardApiCredentials');
      }
      // scroll to the top of the page
      goTo(this.$refs.content);
    },
  },
  mounted() {
    // scroll to the top of the page
    goTo(this.$refs.content);
  },
};
</script>

<style scoped>
</style>