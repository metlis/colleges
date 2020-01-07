<template>
  <v-row
    :class="$style.content"
    dense
  >
    <!--  Header  -->
    <v-col cols="12">
      <h3>{{header}}</h3>
    </v-col>
    <!-- A message for no results   -->
    <v-col
      cols="12"
      v-if="selectedColleges.length === 0"
    >
      <v-alert
        type="info"
        border="left"
        color="#FFAB91"
      >
        There are no colleges to display.
        You can start your search <a href="/main/" :class="$style.link">here</a>
      </v-alert>
    </v-col>
    <!--  Result content  -->
    <template v-if="selectedColleges.length > 0">
      <v-col
        cols="12"
        xs="12"
        sm="12"
        md="4"
        class="pr-0"
        v-for="college in collegesRenderList"
        :key="college.id"
      >
      <!-- College's card -->
      <v-card>
        <v-card-title :class="$style.title">
          {{college.name}}
        </v-card-title>
        <v-card-text>
          <span
            @click="openCollegeUrl(college.url)"
            :class="$style.url"
          >
            {{college.url}}
          </span>
          <div>
            <!-- Sort value -->
            <div
               class="text--primary"
               :class="$style.chip"
               v-if="isSortValueVisible(college)"
            >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-chip
                    v-on="on"
                    color="grey lighten-3"
                  >
                    <v-icon size="1rem">
                      {{menu.activeSortButton.icon}}
                    </v-icon>
                    <!-- Percent sort value badge -->
                    <template v-if="isPercentSortValueBadge">
                      <span class="pl-1">
                        {{getSortPercentValue(college)}}%
                      </span>
                    </template>
                    <!-- Money amount sort value badge -->
                    <template v-else-if="isMoneyAmountSortValueBadge">
                      <span class="pl-1">
                        {{getSortMoneyAmountValue(college)}}$
                      </span>
                    </template>
                    <!-- A raw number value badge -->
                    <template v-else>
                      <span class="pl-1">
                        {{getSortRawNumberValueString(college)}}
                      </span>
                    </template>
                  </v-chip>
                </template>
                <!-- Tooltip text -->
                <span>
                  {{menu.activeSortButton.tooltip}}
                </span>
              </v-tooltip>
            </div>
            <!-- Range filter values -->
            <template v-for="filter in filtersApplied.rangeFilters">
              <div
               v-if="collegeFilterValueExists(filter, college)"
               :key="filter.title"
               :class="$style.chip"
               class="text--primary"
              >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-chip
                    v-on="on"
                    class="ma-1"
                    outlined
                  >
                    <v-icon size="1rem">
                      {{filter.icon}}
                    </v-icon>
                    <!-- Filter's reversed-percent value badge -->
                    <template v-if="filterReversedParamValueExists(filter)">
                      <span class="pl-1">
                        {{getFilterReversedParamValue(college, filter)}}%
                      </span>
                    </template>
                    <!-- Filter's percent value badge -->
                    <template v-else-if="filterPercentParamValueExists(filter)">
                      <span class="pl-1">
                        {{getFilterPercentParamValue(college, filter)}}%
                      </span>
                    </template>
                    <!-- Filter's money-amount value badge -->
                    <template v-else-if="filterMoneyAmountParamValueExists(filter)">
                      <span class="pl-1">
                        {{getFilterRawDataParamValue(college, filter)}}$
                      </span>
                    </template>
                    <!-- Filter's raw-number value badge -->
                    <template v-else>
                      <span class="pl-1">
                        {{getFilterRawDataParamValue(college, filter)}}
                      </span>
                    </template>
                  </v-chip>
                </template>
                <!-- Tooltip text -->
                <span>
                  {{filter.title}}
                </span>
              </v-tooltip>
            </div>
            </template>
            <!-- Checkbox filter values -->
            <template v-for="filter in filtersApplied.checkboxFilters">
              <div
               v-if="collegeFilterValueExists(filter, college)"
               :key="filter.title"
               :class="$style.chip"
               class="d-inline"
              >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-chip
                    v-on="on"
                    class="ma-1"
                    outlined
                  >
                    {{filter.title}}
                  </v-chip>
                </template>
                <span>
                  {{filter.title}}
                </span>
              </v-tooltip>
              </div>
            </template>
            <!-- State filter values -->
            <template v-for="filter in menu.statesFilters">
              <div
               v-if="getFilterStateValue(college, filter)"
               :key="filter"
               :class="$style.chip"
               class="text--primary">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-chip
                    v-on="on"
                    class="ma-1"
                    outlined
                  >
                    {{filter}}
                  </v-chip>
                </template>
                <!-- Tooltip text -->
                <span>
                  State
                </span>
              </v-tooltip>
              </div>
            </template>
          </div>
        </v-card-text>
        <!-- Action icons -->
        <v-card-actions>
          <v-btn icon>
            <v-icon
              :color="getCollegeColor(college.id)"
              @click="toggleFavourite(college.id)"
            >
              mdi-heart
            </v-icon>
          </v-btn>
          <v-icon @click="openCollegePage(college.id, college.slug)">
            mdi-link-variant
          </v-icon>
          <div class="flex-grow-1"></div>
          <v-btn
            icon
            @click="toggleChevron(college.id)"
          >
            <v-icon>
              {{getChevron(college.id)}}
            </v-icon>
          </v-btn>
        </v-card-actions>
        <!-- Expanded college info -->
        <v-expand-transition>
          <div v-show="cardsExpanded[college.id]">
            <v-card-text>
              <v-divider />
              <template v-for="(item, name) in items">
                <div
                  v-if="college[item.props[0]]"
                  :key="name"
                >
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <span
                        :class="$style.container"
                        v-on="on"
                      >
                        <v-icon>
                          {{item.icon}}
                        </v-icon>
                      </span>
                    </template>
                    <span>
                      {{item.title}}
                    </span>
                  </v-tooltip>
                  <span :class="$style.description">
                    {{college[item.props[0]]}}
                    <template v-if="college[item.props[1]]">
                      , {{college[item.props[1]]}}
                    </template>
                  </span>
                  <br>
                </div>
              </template>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>
    </v-col>
    </template>
    <!-- Show more button -->
    <v-col cols="12">
      <div :class="$style.expand">
        <v-btn
          v-if="isShowButtonVisible"
          @click="incrementCollegesToDisplay"
          depressed
          medium
        >
          Show more
        </v-btn>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import {
  selectColleges,
  addCommas,
  addUnifiedPriceParam,
  sortByNumValue,
  sortСollegesAlphabetically,
  sortColleges,
} from '../../utils/helpers';
import { collegeInfoItems } from '../../utils/dictionaries';

export default {
  name: 'content-colleges-list',
  props: ['colleges', 'favourites', 'menu', 'header', 'limit'],
  data() {
    return {
      selectedColleges: this.colleges,
      favouriteColleges: this.favourites,
      cardsExpanded: {},
      isReverseSort: false,
      collegesToDisplay: this.limit,
      items: collegeInfoItems(),
      collegesSectionLength: 12,
    };
  },
  methods: {
    getCollegesList() {
      return selectColleges(this.colleges, this.menu);
    },
    toggleFavourite(id) {
      fetch(`/api/toggle_favourite/?college_id=${id}`)
        .then(response => response.text())
        .then((data) => {
          if (data === 'Removed') {
            this.favouriteColleges.forEach((col, index, obj) => {
              if (col.id === id) {
                obj.splice(index, 1);
                // updating the menu badge
                this.decrementFavBadgeCounter();
              }
            });
          } else if (data === 'Added') {
            const college = this.selectedColleges.find(c => c.id === id);
            if (college) {
              this.favouriteColleges.push(college);
              // update the menu badge
              this.incrementFavBadgeCounter();
            }
          }
          // update the list of favourite colleges in the parent component
          this.$emit('update:favourites', this.favouriteColleges);
        }).catch((err) => {
          console.error(err);
        });
    },
    openCollegePage(id, slug) {
      const url = `/institution/${id}/${slug}`;
      window.open(url, '_self');
    },
    openCollegeUrl(url) {
      window.open(`//${url}`, '_self');
    },
    toggleChevron(id) {
      if (!this.cardsExpanded[id]) {
        this.$set(this.cardsExpanded, id, true);
      } else {
        this.cardsExpanded[id] = !this.cardsExpanded[id];
      }
    },
    sortColleges() {
      sortColleges(this);
    },
    addCommas(num) {
      return addCommas(num);
    },
    sortByCost() {
      addUnifiedPriceParam(this.selectedColleges);
      sortByNumValue(this.selectedColleges, this.menu.activeSortButton.name, this.isReverseSort);
    },
    updateFilteredCollegesList() {
      this.selectedColleges = this.getCollegesList();
    },
    collegeSortValueExists(college) {
      const sortButton = this.menu.activeSortButton;
      return college[sortButton.name] !== ''
             && college[sortButton.name] !== null
             && sortButton.name !== 'name';
    },
    collegeFilterValueExists(filter, college) {
      return college[filter.name] !== ''
             && college[filter.name] !== null
             && filter.name !== this.menu.activeSortButton.name;
    },
    isFavourite(id) {
      if (!this.favouriteColleges) return false;
      return this.favouriteColleges.some(college => college.id === id);
    },
    incrementFavBadgeCounter() {
      const counter = document.getElementById('favourite-badge');
      counter.innerText = +counter.innerText + 1;
    },
    decrementFavBadgeCounter() {
      const counter = document.getElementById('favourite-badge');
      counter.innerText -= 1;
    },
    incrementCollegesToDisplay() {
      this.collegesToDisplay = Number(this.collegesToDisplay) + this.collegesSectionLength;
    },
    getCollegeColor(id) {
      return this.isFavourite(id) ? 'amber' : 'grey';
    },
    getChevron(id) {
      return this.cardsExpanded[id] ? 'mdi-chevron-up' : 'mdi-chevron-down';
    },
    // filter values methods
    filterReversedParamValueExists(filter) {
      return filter.title.indexOf('Full-time') > -1 || filter.title.indexOf('Male') > -1;
    },
    filterPercentParamValueExists(filter) {
      return filter.title.indexOf('%') > -1;
    },
    filterMoneyAmountParamValueExists(filter) {
      return filter.title.indexOf('$') > -1;
    },
    getFilterReversedParamValue(college, filter) {
      return 100 - Math.round(college[filter.name] * 100);
    },
    getFilterPercentParamValue(college, filter) {
      return Math.round(college[filter.name] * 100);
    },
    getFilterRawDataParamValue(college, filter) {
      return addCommas(Math.floor(college[filter.name]));
    },
    getFilterStateValue(college, filter) {
      return this.menu.statesFilters && college.state__name === filter;
    },
    // sort values methods
    isSortValueVisible(college) {
      return this.menu.activeSortButton && this.collegeSortValueExists(college);
    },
    getSortPercentValue(college) {
      return Math.round(college[this.menu.activeSortButton.name] * 100);
    },
    getSortRawNumberValueString(college) {
      return addCommas(college[this.menu.activeSortButton.name]);
    },
    getSortMoneyAmountValue(college) {
      return addCommas(Math.round(college[this.menu.activeSortButton.name]));
    },
  },
  computed: {
    filtersApplied() {
      const rangeFilters = [];
      const checkboxFilters = [];
      if (this.menu.rangeFilters) {
        Object.values(this.menu.rangeFilters).forEach((filter) => {
          if (filter.min || filter.max) rangeFilters.push(filter);
        });
      }
      if (this.menu.checkboxFilters) {
        Object.values(this.menu.checkboxFilters).forEach((filter) => {
          if (filter.value) checkboxFilters.push(filter);
        });
      }
      return { rangeFilters, checkboxFilters };
    },
    collegesRenderList() {
      if (!this.limit) return this.selectedColleges;
      return this.selectedColleges.slice(0, this.collegesToDisplay);
    },
    isShowButtonVisible() {
      return this.limit && this.collegesRenderList.length < this.selectedColleges.length;
    },
    isPercentSortValueBadge() {
      return this.menu.activeSortButton.title.indexOf('%') > -1;
    },
    isMoneyAmountSortValueBadge() {
      return this.menu.activeSortButton.title.indexOf('$') > -1;
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
  },
};
</script>

<style lang="stylus" module>
  .container
    display inline-block
    width 25px
    float left
    margin-right 5px
  .description
    display block
    overflow hidden
  .chip
    display inline
  .content
    min-height 120vh
    align-content flex-start
  .expand
    display flex
    justify-content center
  .link
    color white !important
    font-weight bold
  .title
    word-break normal !important
  .url
    cursor pointer
</style>