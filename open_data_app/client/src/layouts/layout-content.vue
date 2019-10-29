<template>
  <v-row class="mx-0" ref="top">
    <!--  Left Navigation Menu  -->
    <v-col
      :class="classes.leftMenu"
      class="pa-0"
      xs="12"
      sm="12"
      md="2"
    >
      <menu-left @navigationClick="changeNavButton" />
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
          <!-- A list of colleges -->
          <content-colleges
            ref="colleges"
            v-if="activeNavButton === 'Colleges'"
            :colleges="colleges"
            :activeSortButton="contentColleges.activeSortButton"
            :prevSortButton="contentColleges.prevSortButton"
            :checkboxFilters="contentColleges.checkboxFilters"
            :statesFilters="contentColleges.statesFilters"
            :rangeFilters="contentColleges.rangeFilters"
            :reset="contentColleges.reset"
          />
          <!-- A map with colleges -->
          <content-map
            ref="map"
            v-if="activeNavButton === 'Map'"
            :colleges="colleges"
            :checkboxFilters="contentMap.checkboxFilters"
            :statesFilters="contentMap.statesFilters"
            :rangeFilters="contentMap.rangeFilters"
            :reset="contentMap.reset"
          />
        </v-container>
      </v-content>
    </v-col>
    <!--  Right Menu  -->
    <v-col
      :class="classes.rightMenu"
      xs="12"
      sm="12"
      md="2"
    >
      <!--  Right Sort/Filter Menu for Colleges  -->
      <menu-right-colleges
        v-if="activeNavButton === 'Colleges'"
        :colleges="colleges"
        @sortClick="changeSortButton('contentColleges', 'colleges-sort-click', $event)"
        @checkboxFilterChanged=
          "updateFilters('contentColleges', 'checkboxFilters', 'colleges-checkbox-click', $event)"
        @statesFilterChanged=
          "updateFilters('contentColleges', 'statesFilters', 'colleges-state-click', $event)"
        @rangeFilterChanged=
          "updateFilters('contentColleges', 'rangeFilters', 'colleges-range-input', $event)"
        @reset="resetFilters('contentColleges')"
      />
      <!--  Right Filter Menu for Map  -->
      <menu-right-map
        v-if="activeNavButton === 'Map'"
        :colleges="colleges"
        @checkboxFilterChanged=
          "updateFilters('contentMap', 'checkboxFilters', 'map-checkbox-click', $event)"
        @statesFilterChanged=
          "updateFilters('contentMap', 'statesFilters', 'map-state-click', $event)"
        @rangeFilterChanged=
          "updateFilters('contentMap', 'rangeFilters', 'map-range-input', $event)"
        @reset="resetFilters('contentMap')"
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
        <v-icon @click="showMenu('rightMenu')">mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        color="indigo"
      >
        <v-icon @click="showMenu('leftMenu')">mdi-menu</v-icon>
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
import MenuLeft from '../components/menus/menu-left.vue';
import MenuRightColleges from '../components/menus/menu-right-colleges.vue';
import MenuRightMap from '../components/menus/menu-right-map.vue';
import ContentColleges from '../components/contents/content-colleges.vue';
import ContentMap from '../components/contents/content-map.vue';

export default {
  name: 'content-layout',
  components: {
    MenuLeft, MenuRightColleges, MenuRightMap, ContentColleges, ContentMap,
  },
  props: ['colleges'],
  data() {
    return {
      activeNavButton: 'Colleges',
      classes: {
        leftMenu: 'd-none d-md-block',
        rightMenu: 'd-none d-md-block',
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
        reset: false,
      },
      contentMap: {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        reset: false,
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
    updateFilters(page, filter, event, val) {
      this[page][filter] = val;
      this[page].reset = false;
      setTimeout(() => {
        this.$root.$emit(event);
      }, 0);
    },
    resetFilters(page) {
      this[page] = Object.assign({}, this[page], {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
        reset: true,
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
      this.classes.rightMenu = 'd-none d-md-block';
      this.classes.leftMenu = 'd-none d-md-block';
      this.mobileMenu = false;
      this.fab = false;
      this.fabClose = false;
    },
  },
};
</script>

<style scoped>
</style>