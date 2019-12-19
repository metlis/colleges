<template>
  <v-container fluid>
    <!--  Empty set message  -->
    <v-alert
      type="info"
      border="left"
      color="#FFAB91"
      v-if="selectedColleges.length === 0"
    >
      Nothing to compare
    </v-alert>
    <!--  Checkbox list  -->
    <div v-if="!showComparison">
      <div v-if="collegesToComparisonIds.length > 0">
        <p>
          <v-chip
            v-for="c in collegesToComparisonIds"
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
          v-model="collegesToComparisonIds"
          color="blue-grey darken-3"
          hide-details
        />
      </div>
      <div
        v-if="showCompareButton"
        :class="$style.buttonContainer"
      >
        <v-btn
          @click="showComparison = true"
          depressed
          medium
        >
          Compare
        </v-btn>
      </div>
    </div>
    <!--  Comparison content  -->
    <div v-if="showComparison">
      <div :class="$style.overview">
        <h1>Overview</h1>
        <div
          v-for="(params, id) in collegesWinners"
          :key="id"
        >
          <span :class="$style.collegeOverview">{{getCollegeName(+id)}}</span>
          <span :class="$style.starsOverview">
            <v-icon
              v-for="c in params"
              :key="params.title"
              color="amber lighten-1"
            >
              mdi-star
            </v-icon>
          </span>
        </div>
      </div>
      <hr :class="$style.divider">
      <div
        v-for="(section, name) in comparisonParams"
        :key="name"
        :class="$style.section"
      >
        <h1>{{name}}</h1>
        <v-card
          v-for="param in section"
          :key="param.title"
          :class="$style.paramCard"
        >
          <v-card-title>
            {{param.title}}
          </v-card-title>
          <v-card-text>
            <div
              v-for="c in collegesToComparison"
              :key="c.id"
              :class="$style.bar"
              :style="getBarStyles(c, param)"
            >
              {{formatValue(c, param) === null ? 'No data' : formatValue(c, param)}}
              <span
                :class="$style.collegeBarName"
                v-if="calculateBarWidth(c, param) === 100"
              >
                {{c.name}}
              </span>
            </div>
          </v-card-text>
        </v-card>
        <hr :class="$style.divider">
      </div>
      <div :class="$style.close">
        <v-btn
          @click="showComparison = false"
          depressed
          medium
        >
          Close
        </v-btn>
      </div>
    </div>
  </v-container>
</template>

<script>
import { rangeFilters } from '../../utils/dictionaries';
import {
  addUnifiedPriceParam,
  selectColleges,
  sortByNumValue,
  sortСollegesAlphabetically,
  sortColleges,
  addCommas,
} from '../../utils/helpers';

export default {
  name: 'content-compare',
  props: ['colleges', 'menu'],
  data() {
    return {
      selectedColleges: this.colleges,
      isReverseSort: false,
      collegesToComparisonIds: [],
      showComparison: false,
      comparisonParams: rangeFilters(),
      collegesWinners: '',
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
      this.collegesToComparisonIds = this.collegesToComparisonIds.filter(c => c !== id);
    },
    getCollegeName(id) {
      const college = this.selectedColleges.find(c => c.id === id);
      if (college) return college.name;
      return '';
    },
    formatValue(college, param) {
      const { name, title } = param;
      if (college[name] === undefined || college[name] === null) return null;
      // percent data
      if (title.indexOf('%') > -1) {
        if (title === 'Male students %' || title === 'Full-time students %') {
          return Math.round((1 - college[name]) * 100);
        }
        return Math.round(college[name] * 100);
      }
      // integers
      return addCommas(Math.round(college[name]));
    },
    getBarStyles(college, param) {
      if (this.formatValue(college, param) === null) return 'backgroundColor: #EEEEEE';
      const percent = this.calculateBarWidth(college, param);
      const fontWeight = this.isWinnerCollege(college, param, percent) ? 800 : 400;
      return `backgroundColor: ${param.color}; width: ${percent}%; fontWeight: ${fontWeight}`;
    },
    calculateBarWidth(college, param) {
      let value = college[param.name];
      if (!value) return 0;
      const values = this.collegesToComparison.map(c => c[param.name]);
      let maxValue = Math.max.apply(null, values);
      if (param.title === 'Male students %' || param.title === 'Full-time students %') {
        maxValue = 1 - Math.min.apply(null, values);
        value = 1 - value;
      }
      if (maxValue > 0) return (value / maxValue) * 100;
      return 0;
    },
    isWinnerCollege(college, param, percent) {
      const { id } = college;
      if (percent === 100) {
        if (!this.collegesWinners) this.collegesWinners = {};
        if (!this.collegesWinners[id]) this.collegesWinners[id] = [];
        this.collegesWinners[id].push(param);
        return true;
      }
      return false;
    },
  },
  computed: {
    showCompareButton() {
      if (this.collegesToComparisonIds.length < 2) return false;
      return true;
    },
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
      if (!val) this.collegesToComparisonIds = [];
      const selectedCollegesIds = val.map(col => col.id);
      this.collegesToComparisonIds = this.collegesToComparisonIds
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
    justify-content center
    margin-top 20px
    width 100%
  .paramCard
    margin-bottom 30px
  .divider
    margin-bottom 20px
  .bar
    border-radius 3px
    height 25px
    margin-bottom 10px
    padding 2px 0px 0px 10px
    display flex
    justify-content space-between
  .collegeBarName
    padding 0px 10px 0px 5px
  .close
    display flex
    justify-content center
  .overview
    margin-bottom 25px
    div
      margin-bottom 5px
  .collegeOverview
    padding-right 5px
  .starsOverview
    padding-top 0px
</style>