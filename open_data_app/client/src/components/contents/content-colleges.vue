<template>
  <v-row>
    <v-col
      cols="12"
      v-if="filteredColleges.length === 0"
    >
      <v-alert
        type="info"
        border="left"
      >
        There are no colleges that match these filters
      </v-alert>
    </v-col>
    <v-col
      cols="4"
      v-if="filteredColleges.length > 0"
      v-for="college in filteredColleges"
      :key="college.id"
    >
      <v-card>
        <v-card-title style="word-break: normal !important">{{college.name}}</v-card-title>
        <v-card-text>
          <span @click="openCollegeUrl(college.url)" style="cursor: pointer">
            {{college.url}}
          </span>
          <!-- Sort values -->
          <div
             v-for="i in Object.keys(sortVals)"
             :key="i"
             class="text--primary"
             v-if="college[sortVals[i].prop]
             && activeSortButton === sortVals[i].activeBtn && isSorted
             && !filtersApplied.rangeFilters.some(filter => filter.name === sortVals[i].prop)">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-chip
                  v-on="on"
                  outlined
                >
                  <template v-if="sortVals[i].prop === 'admission_rate'">
                    {{college.admission_rate * 100}}%
                  </template>
                  <template v-else>
                    {{addCommas(Math.floor(college[sortVals[i].prop]))}}$
                  </template>
                </v-chip>
              </template>
              <span>
                {{sortVals[i].tooltip}}
              </span>
            </v-tooltip>
          </div>
          <!-- Range filter values -->
          <div
             v-for="filter in filtersApplied.rangeFilters"
             v-if="college[filter.name]"
             :key="filter"
             class="text--primary">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-chip
                  v-on="on"
                  class="ma-1"
                  outlined
                >
                  <template v-if="filter.title.indexOf('%') > -1">
                    {{Math.round(college[filter.name] * 100)}}%
                  </template>
                  <template v-else>
                    {{addCommas(Math.floor(college[filter.name]))}}<span
                      v-if="filter.title.indexOf('$') > -1">$</span>
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
             v-if="college[filter.name]"
             :key="filter"
             class="text--primary">
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
             v-for="filter in statesFilters"
             v-if="statesFilters && college.state__name === filter"
             :key="filter"
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
        </v-card-text>
        <v-card-actions>
          <v-btn icon>
            <v-icon color="amber" @click="removeCollege(college.id)">mdi-heart</v-icon>
          </v-btn>
          <v-btn outlined text @click="openCollegePage(college.id, college.slug)">
            Page
          </v-btn>
          <div class="flex-grow-1"></div>
          <v-btn
            icon
            @click="handleChevronClick(college.id)"
          >
            <v-icon>
              {{ cardsStates[college.id] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
            </v-icon>
          </v-btn>
        </v-card-actions>
        <v-expand-transition>
          <div v-show="cardsStates[college.id]">
            <v-card-text>
              <v-divider />
              <div
                v-for="i in Object.keys(items)"
                v-if="college[items[i].props[0]]"
                :key="i"
              >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span
                      :class="$style.container"
                      v-on="on"
                    >
                      <v-icon>{{items[i].icon}}
                    </v-icon></span>
                  </template>
                  <span>{{items[i].title}}</span>
                </v-tooltip>
                <span :class="$style.description"> {{college[items[i].props[0]]}}
                  <template v-if="college[items[i].props[1]]">
                    , {{college[items[i].props[1]]}}
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
export default {
  name: 'content-colleges',
  props: ['colleges', 'activeSortButton', 'prevSortButton', 'checkboxFilters', 'statesFilters', 'rangeFilters'],
  data() {
    return {
      filteredColleges: '',
      cardsStates: {},
      reverseSort: false,
      isSorted: false,
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
      sortVals: {
        cost: {
          tooltip: 'Average cost',
          prop: 'average_price',
          activeBtn: 'cost',
        },
        payments: {
          tooltip: 'Monthly payments',
          prop: 'monthly_payments',
          activeBtn: 'payments',
        },
        admission: {
          tooltip: 'Admission rate',
          prop: 'admission_rate',
          activeBtn: 'admission',
        },
        earnings: {
          tooltip: 'Earnings after graduation',
          prop: 'median_earnings',
          activeBtn: 'earnings',
        },
      },
    };
  },
  methods: {
    getColleges() {
      if (this.checkboxFilters || this.statesFilters || this.rangeFilters) {
        const filteredColleges = this.colleges.filter((college) => {
          let isFiltered = true;
          if (this.checkboxFilters) {
            Object.values(this.checkboxFilters).forEach((filter) => {
              if (filter.value && college[filter.name] === 0) isFiltered = false;
            });
          }
          if (this.statesFilters && this.statesFilters.length > 0
             && !this.statesFilters.some(state => state === college.state__name)) {
            isFiltered = false;
          }
          if (this.rangeFilters) {
            if (!Object.prototype.hasOwnProperty.call(college, 'average_price')) {
              this.createUnifiedPriceParam();
            }
            Object.values(this.rangeFilters).forEach((filter) => {
              if ((+filter.min && !college[filter.name])
                  || (+filter.min && college[filter.name] < +filter.min)) {
                isFiltered = false;
              }
              if ((+filter.max && !college[filter.name])
                  || (+filter.max && college[filter.name] > +filter.max)) {
                isFiltered = false;
              }
            });
          }
          return isFiltered;
        });
        return filteredColleges;
      }
      return this.colleges;
    },
    removeCollege(id) {
      fetch(`/api/modify_favourites/?college_id=${id}`)
        .then(response => response.text())
        .then((data) => {
          if (data === 'Removed') {
            this.localColleges.forEach((col, index, obj) => {
              if (col.id === id) {
                obj.splice(index, 1);
                const favBadge = document.getElementById('favourite-badge');
                favBadge.innerText = String(Number(favBadge.innerText) - 1);
              }
            });
          }
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
    handleChevronClick(id) {
      if (!this.cardsStates[id]) {
        this.$set(this.cardsStates, id, true);
      } else {
        this.cardsStates[id] = !this.cardsStates[id];
      }
    },
    sortColleges() {
      // set reverse sort variable upon the same button click
      if (this.prevSortButton === this.activeSortButton) {
        this.reverseSort = !this.reverseSort;
      } else {
        this.reverseSort = false;
      }
      switch (this.activeSortButton) {
      case 'name':
        this.sortAlphabetically();
        break;
      case 'cost':
        this.sortCost();
        break;
      case 'payments':
        this.sortNumeric(this.sortVals.payments.prop);
        break;
      case 'admission':
        this.sortNumeric(this.sortVals.admission.prop);
        break;
      case 'earnings':
        this.sortNumeric(this.sortVals.earnings.prop);
        break;
      default:
        break;
      }
    },
    // https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
    addCommas(num) {
      try {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      } catch (e) {
        return '';
      }
    },
    sortAlphabetically() {
      this.filteredColleges.sort((a, b) => {
        if (a.name.toLowerCase() < b.name.toLowerCase()) {
          if (!this.reverseSort) return -1;
          return 1;
        }
        if (a.name.toLowerCase() > b.name.toLowerCase()) {
          if (!this.reverseSort) return 1;
          return -1;
        }
        return 0;
      });
    },
    sortCost() {
      this.createUnifiedPriceParam();
      this.sortNumeric(this.sortVals.cost.prop);
    },
    createUnifiedPriceParam() {
      this.filteredColleges.forEach((college) => {
        if (!college.average_net_price_public) {
          // eslint-disable-next-line no-param-reassign
          college.average_price = college.average_net_price_private;
        }
        if (!college.average_net_price_private) {
          // eslint-disable-next-line no-param-reassign
          college.average_price = college.average_net_price_public;
        }
      });
    },
    sortNumeric(param) {
      this.filteredColleges.sort((a, b) => {
        const [first, second] = [a[param], b[param]];
        if (first === null || first === '') return 1;
        if (second === null || second === '') return -1;
        if (!this.reverseSort) return Number(first) - Number(second);
        return Number(second) - Number(first);
      });
    },
    updateFilteredCollegesList() {
      this.filteredColleges = this.getColleges();
      this.isSorted = false;
    },
  },
  computed: {
    filtersApplied() {
      const rangeFilters = [];
      const checkboxFilters = [];
      if (this.rangeFilters) {
        Object.values(this.rangeFilters).forEach((filter) => {
          if (filter.min || filter.max) rangeFilters.push(filter);
        });
      }
      if (this.checkboxFilters) {
        Object.values(this.checkboxFilters).forEach((filter) => {
          if (filter.value) checkboxFilters.push(filter);
        });
      }
      return { rangeFilters, checkboxFilters };
    },
  },
  created() {
    this.filteredColleges = this.getColleges();
    this.$root.$on('sort-click', () => {
      this.sortColleges();
      this.isSorted = true;
    });
    this.$root.$on('checkbox-click', () => {
      this.updateFilteredCollegesList();
    });
    this.$root.$on('state-click', () => {
      this.updateFilteredCollegesList();
    });
    this.$root.$on('range-input', () => {
      this.updateFilteredCollegesList();
    });
    this.$root.$on('reset-filters', () => {
      this.reverseSort = false;
      this.updateFilteredCollegesList();
      this.sortAlphabetically();
    });
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
</style>