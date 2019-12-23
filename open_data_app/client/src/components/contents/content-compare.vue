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
        Nothing to compare
      </v-alert>
    </v-col>
    <!--  Content  -->
    <v-col cols="12">
      <!--  Checkbox list    -->
      <v-card v-if="!showComparison">
        <v-card-text>
          <checkbox-list
            :collegesData="selectedColleges"
            :selectedIds.sync="collegesToComparisonIds"
            minItems="2"
            @action="displayComparison"
            actionButton="Compare"
            ref="checkbox"
          />
        </v-card-text>
      </v-card>
      <!--  Comparison content  -->
      <div v-if="showComparison">
        <div :class="$style.overview" ref="overview">
          <v-divider />
          <h1>Top values disctribution</h1>
          <div
            v-for="(params, id) in collegesWinners"
            :key="id"
          >
            <span :class="$style.collegeOverview">{{getCollegeName(+id)}}: </span>
            <span :class="$style.starsOverview">
              <v-chip
                v-for="p in params"
                :key="p.title"
                :class="$style.chip"
                @click="scrollTo(p.title)"
                class="ma-1"
                small
              >
                {{p.title}}
              </v-chip>
            </span>
          </div>
          <div :class="$style.close">
            <v-btn
              @click="hideComparison"
              depressed
              small
            >
              Back
            </v-btn>
          </div>
        </div>
        <v-divider />
        <div
          v-for="(section, name) in comparisonParams"
          :key="name"
          :class="$style.section"
        >
          <h1>{{name}}</h1>
          <v-card
            v-for="param in section"
            :key="param.title"
            :ref="param.title"
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
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span v-on="on">
                      {{formatValue(c, param) === null ? 'No data' : formatValue(c, param)}}
                    </span>
                  </template>
                  <span>
                    {{c.name}}
                  </span>
                </v-tooltip>
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
            @click="hideComparison"
            depressed
            medium
          >
            Back
          </v-btn>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import goTo from 'vuetify/es5/services/goto';
import CheckboxList from '../reusable-components/checkbox-list.vue';
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
  props: ['colleges', 'menu', 'header'],
  components: { CheckboxList },
  data() {
    return {
      selectedColleges: this.colleges,
      collegesToComparisonIds: [],
      isReverseSort: false,
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
          return ((1 - college[name]) * 100).toPrecision(3);
        }
        return (college[name] * 100).toPrecision(3);
      }
      // integers
      return addCommas(Math.round(college[name]));
    },
    getBarStyles(college, param) {
      if (this.formatValue(college, param) === null) return 'backgroundColor: #f4f5f7';
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
    scrollTo(ref) {
      goTo(this.$refs[ref][0]);
    },
    hideComparison() {
      this.collegesWinners = '';
      this.showComparison = false;
    },
    displayComparison() {
      this.showComparison = true;
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
      this.hideComparison();
    },
    'menu.restore': function (val) {
      if (val) {
        this.hideComparison();
        this.isReverseSort = false;
        this.selectedColleges = this.colleges;
        sortСollegesAlphabetically(this.selectedColleges, this.isReverseSort);
      }
    },
    'menu.activeSortButton': function () {
      this.hideComparison();
      this.sortColleges();
    },
    'menu.prevSortButton': function () {
      this.hideComparison();
      this.sortColleges();
    },
    'menu.checkboxFilters': function () {
      this.hideComparison();
      this.updateFilteredCollegesList();
    },
    'menu.statesFilters': function () {
      this.hideComparison();
      this.updateFilteredCollegesList();
    },
    'menu.rangeFilters': function () {
      this.hideComparison();
      this.updateFilteredCollegesList();
    },
    selectedColleges(val) {
      if (!val) this.collegesToComparisonIds = [];
      const selectedCollegesIds = val.map(col => col.id);
      this.collegesToComparisonIds = this.collegesToComparisonIds
        .filter(c => selectedCollegesIds.includes(c));
    },
    showComparison(val) {
      setTimeout(() => {
        if (val) {
          goTo(this.$refs.overview);
        } else {
          goTo(this.$refs.checkbox);
        }
      }, 0);
    },
  },
  mounted() {
    addUnifiedPriceParam(this.selectedColleges);
  },
};
</script>

<style lang="stylus" module>
  .paramCard
    margin-bottom 30px
  .bar
    border-radius 3px
    height 25px
    margin-bottom 5px
    padding 2px 0px 0px 10px
    display flex
    justify-content space-between
  .collegeBarName
    padding 0px 10px 0px 5px
  .close
    display flex
    justify-content flex-end
  .overview
    margin-bottom 25px
    div
      margin-bottom 5px
  .collegeOverview
    padding-right 5px
  .starsOverview
    padding-top 0px
  .chip
    cursor pointer
</style>