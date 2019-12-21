<template>
  <v-row dense>
    <!--  Header  -->
    <v-col cols="12">
      <h3>{{header}}</h3>
    </v-col>
    <!--  Empty set message  -->
    <v-col cols="12" v-if="selectedColleges.length === 0">
      <v-alert
        type="info"
        border="left"
        color="#FFAB91"
      >
        Nothing to show
      </v-alert>
    </v-col>
    <!--  Content  -->
    <v-col cols="12">
      <!--  Checkbox list    -->
      <checkbox-list
        v-if="!showHistory"
        :collegesData="selectedColleges"
        :selectedIds.sync="collegesToComparisonIds"
        :minItems="1"
        @action="displayHistory"
        actionButton="View"
      />
    </v-col>
  </v-row>
</template>

<script>
import CheckboxList from '../reusable-components/checkbox-list.vue';
import {
  addUnifiedPriceParam,
  selectColleges,
  sortByNumValue,
  sortColleges,
  sortСollegesAlphabetically,
} from '../../utils/helpers';

export default {
  name: 'content-history',
  props: ['colleges', 'menu', 'header'],
  components: { CheckboxList },
  data() {
    return {
      selectedColleges: this.colleges,
      collegesToComparisonIds: [],
      isReverseSort: false,
      showHistory: false,
    };
  },
  methods: {
    getCollegesList() {
      return selectColleges(this.colleges, {
        checkboxFilters: this.menu.checkboxFilters,
        statesFilters: this.menu.statesFilters,
        rangeFilters: this.menu.rangeFilters,
      });
    },
    sortColleges() {
      sortColleges(this);
    },
    sortByCost() {
      addUnifiedPriceParam(this.selectedColleges);
      sortByNumValue(this.selectedColleges, this.menu.activeSortButton.name, this.isReverseSort);
    },
    updateFilteredCollegesList() {
      this.selectedColleges = this.getCollegesList();
    },
    hideHistory() {
      this.showHistory = false;
    },
    displayHistory() {
      this.showHistory = true;
    },
  },
  computed: {
    collegesToComparison() {
      const collegesToComparison = this.selectedColleges
        .filter(c => this.collegesToComparisonIds.find(id => id === c.id));
      return collegesToComparison;
    },
  },
  watch: {
    colleges() {
      this.updateFilteredCollegesList();
      this.sortColleges();
      this.hideHistory();
    },
    'menu.restore': function (val) {
      if (val) {
        this.hideHistory();
        this.isReverseSort = false;
        this.selectedColleges = this.colleges;
        sortСollegesAlphabetically(this.selectedColleges, this.isReverseSort);
      }
    },
    'menu.activeSortButton': function () {
      this.hideHistory();
      this.sortColleges();
    },
    'menu.prevSortButton': function () {
      this.hideHistory();
      this.sortColleges();
    },
    'menu.checkboxFilters': function () {
      this.hideHistory();
      this.updateFilteredCollegesList();
    },
    'menu.statesFilters': function () {
      this.hideHistory();
      this.updateFilteredCollegesList();
    },
    'menu.rangeFilters': function () {
      this.hideHistory();
      this.updateFilteredCollegesList();
    },
    selectedColleges(val) {
      if (!val) this.collegesToComparisonIds = [];
      const selectedCollegesIds = val.map(col => col.id);
      this.collegesToComparisonIds = this.collegesToComparisonIds
        .filter(c => selectedCollegesIds.includes(c));
    },
  },
  mounted() {
    addUnifiedPriceParam(this.selectedColleges);
  },
};
</script>

<style scoped>

</style>