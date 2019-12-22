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
      <!--   History content   -->
      <div v-if="showHistory">
        <!--   Progress     -->
        <div
          v-if="isFetching"
          :class="$style.progress"
        >
          <v-progress-circular
            :size="50"
            color="#CFD8DC"
            indeterminate />
        </div>
        <!--   Charts     -->
        <div v-if="!isFetching"></div>
      </div>
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
import { rangeFilters } from '../../utils/dictionaries';

export default {
  name: 'content-history',
  props: ['colleges', 'menu', 'header', 'credentials'],
  components: { CheckboxList },
  data() {
    return {
      selectedColleges: this.colleges,
      collegesToComparisonIds: [],
      isReverseSort: false,
      showHistory: false,
      isFetching: false,
      collegeParams: rangeFilters(),
      collegesApiData: [],
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
      this.fetchCollegesHistory();
    },
    fetchCollegesHistory() {
      this.isFetching = true;
      const urls = this.createApiCallUrls();
      Promise.all(
        urls.map(url => fetch(url)),
      ).then((response) => {
        response.forEach((r) => {
          const respObj = r.json();
          respObj.then((data) => {
            this.collegesApiData.push(data.results);
          });
        });
      }).catch((err) => {
        console.error(err);
      })
        .finally(() => {
          this.isFetching = false;
        });
    },
    createApiCallUrls() {
      // constructing id url parameter
      const ids = this.collegesToComparisonIds.join(',');
      const idParamString = `id=${ids}`;
      // constructing fields url parameter for each api method
      const fieldsParamStrings = [];
      Object.values(this.collegeParams).forEach((section) => {
        Object.values(section).forEach((param) => {
          const apiName = param.api;
          if (apiName) {
            if (typeof apiName === 'object') {
              apiName.forEach((name) => {
                fieldsParamStrings.push(this.createUrlParamFields(name));
              });
            } else {
              fieldsParamStrings.push(this.createUrlParamFields(apiName));
            }
          }
        });
      });
      const queryUrls = fieldsParamStrings.map(str => `${this.credentials.api_url}?${idParamString}&fields=${str}&api_key=${this.credentials.api_key}`);
      return queryUrls;
    },
    createUrlParamFields(apiName) {
      // the first and the last years which contain data
      let currentYear = 1996;
      const endYear = 2017;
      // resulting query string
      let queryString = '';
      while (currentYear <= endYear) {
        queryString += `,${currentYear}.${apiName}`;
        currentYear += 1;
      }
      // delete trailing comma
      queryString = queryString.slice(1);
      return queryString;
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

<style lang="stylus" module>
  .progress
    text-align center
</style>