<template>
  <v-row class="mx-0">
    <v-col
      v-if="!rightMobileMenu"
      :class="classes.leftMenu"
      xs="12"
      sm="12"
      md="2"
      style="padding: 0px"
    >
      <menu-left @navigationClick="changeNavButton" />
    </v-col>
    <v-col
      v-show="!rightMobileMenu"
      xs="12"
      sm="12"
      md="7"
    >
      <v-content>
        <v-container fluid style="padding: 0px">
          <content-colleges
            v-if="activeNavButton === 'Colleges'"
            :colleges="colleges"
            :activeSortButton="activeSortButton"
            :prevSortButton="prevSortButton"
            :checkboxFilters="checkboxFilters"
            :statesFilters="statesFilters"
            :rangeFilters="rangeFilters"
            ref="colleges"
          />
        </v-container>
      </v-content>
    </v-col>
    <v-col
      :class="classes.rightMenu"
      xs="12"
      sm="12"
      offset-md="1"
      md="2"
      ref="rightMenu"
    >
      <menu-right-colleges
        v-if="activeNavButton === 'Colleges'"
        @sortClick="changeSortButton"
        @checkboxFilterChanged="updateCheckboxFilters"
        @statesFilterChanged="updateStatesFilters"
        @rangeFilterChanged="updateRangeFilters"
        @resetFilters="resetFilters"
        :colleges="colleges"
      />
    </v-col>
    <!--  Filter button  -->
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
          color="blue darken-2"
          dark
          fab
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
        <v-icon @click="showRightMenu">mdi-filter</v-icon>
      </v-btn>
      <v-btn
        fab
        dark
        small
        color="indigo"
      >
        <v-icon>mdi-menu</v-icon>
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
      <v-icon @click="showRightMenu">mdi-close</v-icon>
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
      activeSortButton: '',
      prevSortButton: '',
      checkboxFilters: '',
      statesFilters: '',
      rangeFilters: '',
      classes: {
        leftMenu: 'd-none d-md-block',
        rightMenu: 'd-none d-md-block',
      },
      rightMobileMenu: false,
      fab: false,
      fabClose: false,
    };
  },
  methods: {
    changeNavButton(val) {
      this.activeNavButton = val;
    },
    changeSortButton(val) {
      if (this.activeSortButton) this.prevSortButton = this.activeSortButton;
      this.activeSortButton = val;
      setTimeout(() => {
        this.$root.$emit('sort-click');
      }, 0);
    },
    updateCheckboxFilters(val) {
      this.checkboxFilters = val;
      setTimeout(() => {
        this.$root.$emit('checkbox-click');
      }, 0);
    },
    updateStatesFilters(val) {
      this.statesFilters = val;
      setTimeout(() => {
        this.$root.$emit('state-click');
      }, 0);
    },
    updateRangeFilters(val) {
      this.rangeFilters = val;
      setTimeout(() => {
        this.$root.$emit('range-input');
      }, 0);
    },
    resetFilters() {
      this.activeSortButton = '';
      this.prevSortButton = '';
      this.checkboxFilters = '';
      this.statesFilters = '';
      this.rangeFilters = '';
      goTo(this.$refs.colleges);
      setTimeout(() => {
        this.$root.$emit('reset-filters');
      }, 0);
    },
    showRightMenu() {
      if (this.classes.rightMenu.indexOf('d-none') > -1) {
        this.classes.rightMenu = 'd-block';
        this.rightMobileMenu = true;
        this.fabClose = true;
        goTo(this.$refs.rightMenu);
      } else {
        this.classes.rightMenu = 'd-none d-md-block';
        this.rightMobileMenu = false;
        this.fab = false;
        this.fabClose = false;
      }
    },
  },
};
</script>

<style scoped>
</style>