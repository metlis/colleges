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
        <v-container fluid style="padding: 0px">
          <!-- Colleges list -->
          <content-colleges
            ref="colleges"
            v-if="activeNavButton === 'Colleges'"
            :colleges="colleges"
            :activeSortButton="contentColleges.activeSortButton"
            :prevSortButton="contentColleges.prevSortButton"
            :checkboxFilters="contentColleges.checkboxFilters"
            :statesFilters="contentColleges.statesFilters"
            :rangeFilters="contentColleges.rangeFilters"
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
      <!--  Right Sort/Filter Menu  -->
      <menu-right-colleges
        v-if="activeNavButton === 'Colleges'"
        :colleges="colleges"
        @sortClick="changeCollegesSortButton"
        @checkboxFilterChanged="updateCollegesCheckboxFilters"
        @statesFilterChanged="updateCollegesStatesFilters"
        @rangeFilterChanged="updateCollegesRangeFilters"
        @reset="resetFilters"
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
import ContentColleges from '../components/contents/content-colleges.vue';

export default {
  name: 'content-layout',
  components: { MenuLeft, MenuRightColleges, ContentColleges },
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
      },
    };
  },
  methods: {
    changeNavButton(val) {
      this.activeNavButton = val;
    },
    changeCollegesSortButton(val) {
      if (this.contentColleges.activeSortButton) {
        this.contentColleges.prevSortButton = this.contentColleges.activeSortButton;
      }
      this.contentColleges.activeSortButton = val;
      setTimeout(() => {
        this.$root.$emit('sort-click');
      }, 0);
    },
    updateCollegesCheckboxFilters(val) {
      this.contentColleges.checkboxFilters = val;
      setTimeout(() => {
        this.$root.$emit('checkbox-click');
      }, 0);
    },
    updateCollegesStatesFilters(val) {
      this.contentColleges.statesFilters = val;
      setTimeout(() => {
        this.$root.$emit('state-click');
      }, 0);
    },
    updateCollegesRangeFilters(val) {
      this.contentColleges.rangeFilters = val;
      setTimeout(() => {
        this.$root.$emit('range-input');
      }, 0);
    },
    resetFilters() {
      this.contentColleges = Object.assign({}, this.contentColleges, {
        activeSortButton: '',
        prevSortButton: '',
        checkboxFilters: '',
        statesFilters: '',
        rangeFilters: '',
      });
      goTo(this.$refs.top);
      setTimeout(() => {
        this.$root.$emit('reset-filters');
      }, 0);
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