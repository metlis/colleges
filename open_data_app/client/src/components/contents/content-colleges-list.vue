<template>
  <v-row
    :class="$style.content"
    dense
  >
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
        There are no colleges that match these filters.
        You can start your search <a href="/main/">here</a>
      </v-alert>
    </v-col>
    <!--  Result content  -->
    <v-col
      cols="12"
      xs="12"
      sm="12"
      md="4"
      v-if="selectedColleges.length > 0"
      v-for="college in selectedColleges"
      :key="college.id"
      class="pr-0"
    >
      <v-card>
        <v-card-title style="word-break: normal !important">
          {{college.name}}
        </v-card-title>
        <v-card-text>
          <span
            @click="openCollegeUrl(college.url)"
            style="cursor: pointer"
          >
            {{college.url}}
          </span>
          <div>
            <!-- Sort value -->
            <div
               class="text--primary"
               :class="$style.chip"
               v-if="menu.activeSortButton && collegeSortValueExists(college)"
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
                    <template v-if="menu.activeSortButton.name === 'admission_rate'
                    || menu.activeSortButton.name === 'federal_loan'">
                      <span class="pl-1">
                        {{Math.round(college[menu.activeSortButton.name] * 100)}}%
                      </span>
                    </template>
                    <template v-else-if="menu.activeSortButton.name === 'undergrad_students'">
                      <span class="pl-1">
                        {{addCommas(college[menu.activeSortButton.name])}}
                      </span>
                    </template>
                    <template v-else>
                      <span class="pl-1">
                        {{addCommas(Math.round(college[menu.activeSortButton.name]))}}$
                      </span>
                    </template>
                  </v-chip>
                </template>
                <span>
                  {{menu.activeSortButton.tooltip}}
                </span>
              </v-tooltip>
            </div>
            <!-- Range filter values -->
            <div
               v-for="filter in filtersApplied.rangeFilters"
               v-if="filtersApplied && collegeFilterValueExists(filter, college)"
               :key="filter.title"
               :class="$style.chip"
               class="text--primary">
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
                    <template v-if="filter.title.indexOf('%') > -1">
                      <span class="pl-1">
                        {{Math.round(college[filter.name] * 100)}}%
                      </span>
                    </template>
                    <template v-else>
                      <span class="pl-1">
                        {{addCommas(Math.floor(college[filter.name]))}}
                      </span>
                      <span v-if="filter.title.indexOf('$') > -1">$</span>
                    </template>
                  </v-chip>
                </template>
                <span>
                    {{filter.title}}
                </span>
              </v-tooltip>
            </div>
            <!-- Checkbox filter values -->
            <div
               v-for="filter in filtersApplied.checkboxFilters"
               v-if="filtersApplied && collegeFilterValueExists(filter, college)"
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
            <!-- State filter values -->
            <div
               v-for="filter in menu.statesFilters"
               v-if="menu.statesFilters && college.state__name === filter"
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
                <span>
                    State
                </span>
              </v-tooltip>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn icon>
            <v-icon
              :color="isFavourite(college.id) ? 'amber' : 'grey'"
              @click="toggleFavourite(college.id)"
            >
              mdi-heart
            </v-icon>
          </v-btn>
          <v-btn outlined text @click="openCollegePage(college.id, college.slug)">
            Page
          </v-btn>
          <div class="flex-grow-1"></div>
          <v-btn
            icon
            @click="toggleChevron(college.id)"
          >
            <v-icon>
              {{ cardsExpanded[college.id] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-actions>
        <v-expand-transition>
          <div v-show="cardsExpanded[college.id]">
            <v-card-text>
              <v-divider />
              <div
                v-for="(item, name) in items"
                v-if="college[item.props[0]]"
                :key="name"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span
                      :class="$style.container"
                      v-on="on"
                    >
                      <v-icon>{{item.icon}}
                    </v-icon></span>
                  </template>
                  <span>{{item.title}}</span>
                </v-tooltip>
                <span :class="$style.description"> {{college[item.props[0]]}}
                  <template v-if="college[item.props[1]]">
                    , {{college[item.props[1]]}}
                  </template>
                </span><br>
              </div>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import {
  selectColleges, addUnifiedPriceParam, sortByNumValue, addCommas, sortСollegesAlphabetically,
} from '../../utils/helpers';

export default {
  name: 'content-colleges-list',
  props: ['colleges', 'favourites', 'menu', 'restore'],
  data() {
    return {
      selectedColleges: this.colleges,
      favouriteColleges: this.favourites,
      cardsExpanded: {},
      isReverseSort: false,
      items: {
        location: {
          icon: 'mdi-map-marker',
          title: 'Location',
          props: ['city', 'state__name'],
        },
        locale: {
          icon: 'mdi-city',
          title: 'Locale',
          props: ['locale__description'],
        },
        carnegie: {
          icon: 'mdi-book-search',
          title: 'Carnegie classification',
          props: ['carnegie__description'],
        },
        religion: {
          icon: 'mdi-church',
          title: 'Religious affiliation',
          props: ['religion__name'],
        },
        ownership: {
          icon: 'mdi-briefcase',
          title: 'Ownership',
          props: ['ownership__description'],
        },
      },
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
      if (!this.selectedColleges) this.updateFilteredCollegesList();
      // set isReverseSort variable to true on the same button click
      if (this.menu.prevSortButton.name === this.menu.activeSortButton.name) {
        this.isReverseSort = !this.isReverseSort;
      } else {
        this.isReverseSort = false;
      }
      switch (this.menu.activeSortButton.name) {
      case 'name':
        sortСollegesAlphabetically(this.selectedColleges, this.isReverseSort);
        break;
      case 'average_price':
        this.sortByCost();
        break;
      case 'federal_loan':
      case 'admission_rate':
      case 'undergrad_students':
        sortByNumValue(this.selectedColleges, this.menu.activeSortButton.name, this.isReverseSort);
        break;
      default:
        break;
      }
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
  },
  watch: {
    colleges() {
      this.updateFilteredCollegesList();
      this.sortColleges();
    },
    restore(val) {
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
</style>