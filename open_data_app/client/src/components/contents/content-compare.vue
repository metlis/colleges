<template>
  <v-container fluid>
    <v-alert
      type="info"
      border="left"
      color="#FFAB91"
      v-if="selectedColleges.length === 0"
    >
      Nothing to compare
    </v-alert>
    <div>
      <div v-if="collegesToComparison.length > 1">
        <p>
          <v-chip
            v-for="c in collegesToComparison"
            :key="c"
            @click:close="removeCollegeFromComparison(c)"
            class="ma-2"
            close
          >
            {{getCollegeName(c)}}
          </v-chip>
        </p>
      </div>
      <div>
        <v-checkbox
          v-for="c in selectedColleges"
          :label="c.name"
          :value="c.id"
          :key="c.id"
          :class="$style.college"
          v-model="collegesToComparison"
          color="blue-grey darken-3"
          hide-details
        />
      </div>
      <div
        v-if="showCompareButton"
        :class="$style.buttonContainer"
      >
        <v-btn
          depressed
          small
        >
          Compare
        </v-btn>
      </div>
    </div>
  </v-container>
</template>

<script>
import {
  addUnifiedPriceParam,
  selectColleges,
  sortByNumValue,
  sortСollegesAlphabetically,
  sortColleges,
} from '../../utils/helpers';

export default {
  name: 'content-compare',
  props: ['colleges', 'menu'],
  data() {
    return {
      selectedColleges: this.colleges,
      isReverseSort: false,
      collegesToComparison: [],
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
    removeCollegeFromComparison(id) {
      this.collegesToComparison = this.collegesToComparison.filter(c => c !== id);
    },
    getCollegeName(id) {
      const college = this.selectedColleges.find(c => c.id === id);
      if (college) return college.name;
      return '';
    },
  },
  computed: {
    showCompareButton() {
      if (this.collegesToComparison.length < 2) return false;
      return true;
    },
  },
  watch: {
    colleges() {
      this.updateFilteredCollegesList();
      this.sortColleges();
    },
    'menu.restore': function (val) {
      if (val) {
        this.isReverseSort = false;
        this.selectedColleges = this.colleges;
        sortСollegesAlphabetically(this.selectedColleges, this.isReverseSort);
      }
    },
    'menu.activeSortButton': function () {
      this.sortColleges();
    },
    'menu.prevSortButton': function () {
      this.sortColleges();
    },
    'menu.checkboxFilters': function () {
      this.updateFilteredCollegesList();
    },
    'menu.statesFilters': function () {
      this.updateFilteredCollegesList();
    },
    'menu.rangeFilters': function () {
      this.updateFilteredCollegesList();
    },
    selectedColleges(val) {
      if (!val) this.collegesToComparison = [];
      const selectedCollegesIds = val.map(col => col.id);
      this.collegesToComparison = this.collegesToComparison
        .filter(c => selectedCollegesIds.includes(c));
    },
  },
};
</script>

<style lang="stylus" module>
  .college
    label
      margin-bottom 0px !important
  .buttonContainer
    display flex
    justify-content flex-end
    width 100%
</style>