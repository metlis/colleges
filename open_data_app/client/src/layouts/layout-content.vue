<template>
  <v-content>
    <v-container fluid style="padding: 0px">
      <v-row>
        <v-col cols="2" style="padding: 0px">
          <menu-left @navigationClick="changeNavButton" />
        </v-col>
        <v-col cols="7">
          <content-colleges
             v-if="activeNavButton === 'Colleges'"
            :colleges="colleges"
            :activeSortButton="activeSortButton"
            :prevSortButton="prevSortButton"
            :checkboxFilters="checkboxFilters"
            :statesFilters="statesFilters"
            :rangeFilters="rangeFilters"
          />
        </v-col>
        <v-col cols="2" offset="1" style="padding: 0px">
          <menu-right-colleges
            v-if="activeNavButton === 'Colleges'"
            @sortClick="changeSortButton"
            @checkboxFilterChanged="updateCheckboxFilters"
            @statesFilterChanged="updateStatesFilters"
            @rangeFilterChanged="updateRangeFilters"
            :colleges="colleges"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
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
  },
};
</script>

<style scoped>
</style>