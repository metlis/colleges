<template>
  <v-row dense>
    <!--  Header  -->
    <v-col cols="12" v-if="!isFetching">
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
        <!--   Charts content   -->
        <div v-if="!isFetching">
          <div :class="$style.close">
            <v-btn
              @click="hideHistory"
              depressed
              small
            >
              Back
            </v-btn>
          </div>
          <v-divider />
          <div
            v-for="(section, name) in collegeParams"
            :key="name"
          >
            <h1>{{name}}</h1>
            <div
              v-for="param in section"
              v-if="param.apiResponse"
              :key="param.title"
              :ref="param.title"
            >
              <v-card>
                <v-card-title>{{param.title}}</v-card-title>
                <v-card-text>
                  <chart
                    :chartData="getChartData(param.apiResponse, param.title)"
                  />
                </v-card-text>
              </v-card>
              <br>
            </div>
            <v-divider />
          </div>
          <div :class="$style.close">
            <v-btn
              @click="hideHistory"
              depressed
              medium
            >
              Back
            </v-btn>
          </div>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import CheckboxList from '../reusable-components/checkbox-list.vue';
import Chart from '../reusable-components/chart.vue';

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
  components: { Chart, CheckboxList },
  data() {
    return {
      selectedColleges: this.colleges,
      collegesToComparisonIds: [],
      isReverseSort: false,
      showHistory: false,
      isFetching: false,
      collegeParams: rangeFilters(),
      chartColors: ['#90A4AE', '#A1887F', '#FF8A65', '#FFB74D', '#FFD54F', '#AFB42B', '#7CB342', '#43A047',
        '#4DB6AC', '#4DD0E1', '#4FC3F7', '#42A5F5', '#5C6BC0', '#7E57C2', '#CE93D8', '#F48FB1', '#EF9A9A',
        '#616161', '#FF9E80', '#6D4C41'],
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
            try {
              // getting param's api method name
              const apiCallMethodName = Object.keys(data.results[0])[0];
              const paramApiMethodName = apiCallMethodName.replace(/^[0-9]+\.(.*)/, '$1');
              // saving api response
              Object.values(this.collegeParams).forEach((section) => {
                Object.values(section).forEach((param) => {
                  if (typeof param.apiMethod === 'object' && param.apiMethod.some(m => m === paramApiMethodName)) {
                    // delete old data
                    // eslint-disable-next-line no-param-reassign
                    if (param.apiResponse.length === 2) param.apiResponse = [];
                    param.apiResponse.push(data.results);
                  } else if (param.apiMethod === paramApiMethodName) {
                    // eslint-disable-next-line no-param-reassign
                    param.apiResponse = data.results;
                  }
                });
              });
            } catch (e) {
              console.error(e);
            }
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
          const apiName = param.apiMethod;
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
    getChartData(apiResponse, paramTitle) {
      let paramData = [];
      // cost param's name depends on whether a college is private or public,
      // so we need a unified data about the cost of study
      if (paramTitle.indexOf('Cost') > -1) {
        paramData = this.createUnifiedCostDataset(apiResponse);
      } else {
        paramData = apiResponse;
      }
      if (!paramData) return '';
      // formatting data for chart props
      let labels;
      const datasets = [];
      paramData.forEach((data, index) => {
        // creating dictionary where the key is a year
        const normalizedDict = {};
        Object.keys(data).forEach((key) => {
          const year = parseInt(key, 10);
          let collegeData;
          if (data[key] === null) {
            collegeData = null;
          } else {
            // convert percent data
            // eslint-disable-next-line no-lonely-if
            if (paramTitle.indexOf('%') > -1) {
              // convert part-time data into full-time
              if (paramTitle === 'Full-time students %') {
                collegeData = ((1 - data[key]) * 100).toPrecision(3);
              } else {
                collegeData = (data[key] * 100).toPrecision(3);
              }
            } else {
              collegeData = Math.round(data[key]);
            }
          }
          normalizedDict[year] = collegeData;
        });
        if (!labels) labels = Object.keys(normalizedDict).sort((a, b) => a - b);
        const color = this.chartColors[index] ? this.chartColors[index] : '#B0BEC5';
        const dataset = {
          data: [],
          // the consequence of colleges ids and the consequence of colleges data is the same
          label: this.getCollegeName(this.collegesToComparisonIds[index]),
          fill: false,
          backgroundColor: color,
          borderColor: color,
        };
        labels.forEach((l) => {
          dataset.data.push(normalizedDict[l]);
        });
        datasets.push(dataset);
      });
      return { labels, datasets };
    },
    createUnifiedCostDataset(apiResponse) {
      const firstSet = apiResponse[0];
      const secondSet = apiResponse[1];
      const resultSet = [];
      if (firstSet) {
        // if all values of a dataset are null, get data from another dataset
        firstSet.forEach((data, i) => {
          if (Object.values(data).every(val => val === null)) {
            resultSet.push(secondSet[i]);
          } else {
            resultSet.push(data);
          }
        });
      }
      return resultSet;
    },
    getCollegeName(id) {
      const college = this.selectedColleges.find(c => c.id === id);
      if (college) return college.name;
      return '';
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
    collegesToComparisonIds(val) {
      Object.values(this.collegeParams).forEach((section) => {
        Object.values(section).forEach((param) => {
          if (param.apiMethod && typeof param.apiMethod === 'object') {
            // eslint-disable-next-line no-param-reassign
            param.apiResponse = [];
          } else {
            // eslint-disable-next-line no-param-reassign
            param.apiResponse = '';
          }
        });
      });
    },
  },
  mounted() {
    addUnifiedPriceParam(this.selectedColleges);
  },
};
</script>

<style lang="stylus" module>
  .progress
    height 80vh
    display flex
    align-items center
    justify-content center
  .close
    display flex
    justify-content flex-end
</style>