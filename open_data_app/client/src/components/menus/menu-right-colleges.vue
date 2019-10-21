<template>
  <v-navigation-drawer
    right
    dense
    absolute
    :class="$style.rightMenu"
    width="100%"
  >
    <v-list nav dense flat>
      <!-- Sort block -->
      <v-subheader>Sort</v-subheader>
      <v-list-item-group class="mr-1">
        <v-list-item
          v-for="item in Object.keys(sortNames)"
          :key="sortNames[item].title"
          @click="$emit('sortClick', sortNames[item])"
          class="mt-1 mb-0"
        >
          <v-list-item-icon>
            <v-icon>{{sortNames[item].icon}}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{sortNames[item].title}}
          </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
      <v-divider />
      <!-- State filter block -->
      <v-subheader>Filter</v-subheader>
      <v-expansion-panels accordion class="mx-0 px-0">
        <v-list-item-group
          style="width: 100%;"
          class="mr-2 ml-0"
        >
          <v-expansion-panel
            class="mt-0"
            :class="$style.panel"
          >
            <v-expansion-panel-header class="px-3">
              State
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-list-item class="px-0">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-list-item-icon class="mr-4">
                  <v-icon v-on="on">mdi-map</v-icon>
                </v-list-item-icon>
              </template>
              <span>State</span>
            </v-tooltip>
            <v-list-item-action class="ml-0 mt-1 mb-0">
              <v-select
                v-model="statesSelected"
                @change="$emit('statesFilterChanged', statesSelected)"
                :items="collegesStates"
                dense
                multiple
                flat
                color="blue-grey darken-4"
                item-color="blue-grey darken-4"
              ></v-select>
            </v-list-item-action>
          </v-list-item>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <!--  Range filters  -->
          <v-expansion-panel
            v-for="key in Object.keys(rangeFilters)"
            :key="key"
            class="mt-0"
            :class="$style.panel"
          >
            <v-expansion-panel-header class="px-3">
              {{key}}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <template v-for="filter in Object.keys(rangeFilters[key])">
                <v-subheader
                  inset
                  :class="$style.subheader"
                  :key="rangeFilters[key][filter].title"
                >{{rangeFilters[key][filter].title}}
                </v-subheader>
                <v-list-item
                  :key="filter"
                  class="px-0"
                >
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                      <v-list-item-icon>
                        <v-icon v-on="on">
                          {{rangeFilters[key][filter].icon}}
                        </v-icon>
                      </v-list-item-icon>
                    </template>
                    <span>{{rangeFilters[key][filter].title}}</span>
                  </v-tooltip>
                  <v-list-item-action
                    class="d-flex flex-row align-center ml-0 mt-1 mb-0"
                  >
                    <v-text-field
                      v-model="rangeFilters[key][filter].min"
                      @input="emitRangeInput"
                      dense
                      flat
                      type="number"
                      min="0"
                      color="blue-grey darken-4"
                      placeholder=" "
                    ></v-text-field>
                    <div class="mr-1">-</div>
                    <v-text-field
                      v-model="rangeFilters[key][filter].max"
                      @input="emitRangeInput"
                      dense
                      flat
                      type="number"
                      min="0"
                      color="blue-grey darken-4"
                    ></v-text-field>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <!--  Checkbox filters  -->
          <v-expansion-panel
            class="mt-0"
            :class="$style.panel"
          >
            <v-expansion-panel-header class="px-3">
              Other
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-list-item
                v-for="filter in Object.keys(checkboxFilters)"
                :key="filter"
                 class="mx-0 px-0"
              >
            <template v-slot:default="{ active, toggle }">
              <v-list-item-action class="mt-1 mb-0">
                <v-checkbox
                  @change="$emit('checkboxFilterChanged', checkboxFilters)"
                  v-model="checkboxFilters[filter].value"
                  color="blue-grey darken-4"
                ></v-checkbox>
              </v-list-item-action>
              <v-list-item-content
                @click="tickCheckbox(filter)">
                <v-list-item-title>{{checkboxFilters[filter].title}}</v-list-item-title>
              </v-list-item-content>
            </template>
          </v-list-item>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-list-item-group>
      </v-expansion-panels>
      <br>
      <!--  Reset button  -->
      <div class="my-2 text-center">
        <v-btn
         text
         @click="resetFilters"
        >
          Reset
        </v-btn>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'menu-right-colleges',
  props: ['colleges'],
  data() {
    return {
      sortNames: {
        name: {
          icon: 'mdi-alphabetical',
          title: 'Name',
          tooltip: 'Name',
          name: 'name',
        },
        cost: {
          icon: 'mdi-cash',
          title: 'Cost',
          tooltip: 'Average cost $',
          name: 'average_price',
        },
        loan: {
          icon: 'mdi-bank',
          title: 'Loan',
          tooltip: 'Federal loan recipients %',
          name: 'federal_loan',
        },
        admission: {
          icon: 'mdi-certificate',
          title: 'Admission',
          tooltip: 'Admission rate %',
          name: 'admission_rate',
        },
        undergraduates: {
          icon: 'mdi-account-multiple',
          title: 'Undergraduates',
          tooltip: 'Number of undergraduate students',
          name: 'undergrad_students',
        },
      },
      checkboxFilters: {
        operating: {
          value: false,
          name: 'cur_operating',
          title: 'Operating',
        },
        online: {
          value: false,
          name: 'online_only',
          title: 'Online-only',
        },
        men: {
          value: false,
          name: 'men_only',
          title: 'Men-only',
        },
        women: {
          value: false,
          name: 'women_only',
          title: 'Women-only',
        },
        black: {
          value: false,
          name: 'predom_black',
          title: 'Black',
        },
        hispanic: {
          value: false,
          name: 'hispanic',
          title: 'Hispanic',
        },
      },
      statesSelected: [],
      rangeFilters: {
        Finance: {
          cost: {
            min: '',
            max: '',
            icon: 'mdi-cash',
            name: 'average_price',
            title: 'Cost $',
          },
          payments: {
            min: '',
            max: '',
            icon: 'mdi-credit-card-outline',
            name: 'monthly_payments',
            title: 'Monthly payments $',
          },
          debt: {
            min: '',
            max: '',
            icon: 'mdi-sack-percent',
            name: 'debt_completed_median',
            title: 'Debt after completion $',
          },
          earnings: {
            min: '',
            max: '',
            icon: 'mdi-currency-usd',
            name: 'median_earnings',
            title: 'Earnings after attending $',
          },
        },
        Aid: {
          pell: {
            min: '',
            max: '',
            icon: 'mdi-cash-100',
            name: 'pell_grand',
            title: 'Pell grant recipients %',
          },
          loan: {
            min: '',
            max: '',
            icon: 'mdi-bank',
            name: 'federal_loan',
            title: 'Federal loan recipients %',
          },
        },
        Study: {
          admission: {
            min: '',
            max: '',
            icon: 'mdi-certificate',
            name: 'admission_rate',
            title: 'Admission rate %',
          },
          completion: {
            min: '',
            max: '',
            icon: 'mdi-school',
            name: 'completion_rate_four_year_pooled',
            title: 'Completion rate %',
          },
          retention: {
            min: '',
            max: '',
            icon: 'mdi-account-heart',
            name: 'retention_rate_four_year_pooled',
            title: 'Retention rate %',
          },
        },
        Tests: {
          act: {
            min: '',
            max: '',
            icon: 'mdi-grease-pencil',
            name: 'act_cumulative',
            title: 'ACT cumulative',
          },
          sat: {
            min: '',
            max: '',
            icon: 'mdi-lead-pencil',
            name: 'sat_average',
            title: 'SAT average',
          },
        },
        Students: {
          undergraduates: {
            min: '',
            max: '',
            icon: 'mdi-account-multiple',
            name: 'undergrad_students',
            title: 'Number of undergraduates',
          },
          fullTime: {
            min: '',
            max: '',
            icon: 'mdi-account-clock',
            name: 'students_part_time',
            title: 'Full-time students %',
          },
          female: {
            min: '',
            max: '',
            icon: 'mdi-human-female',
            name: 'students_female',
            title: 'Female students %',
          },
          male: {
            min: '',
            max: '',
            icon: 'mdi-human-male',
            name: 'students_female',
            title: 'Male students %',
          },
        },
      },
    };
  },
  methods: {
    tickCheckbox(filter) {
      this.checkboxFilters[filter].value = !this.checkboxFilters[filter].value;
      this.$emit('checkboxFilterChanged', this.checkboxFilters);
    },
    emitRangeInput() {
      const copy = JSON.parse(JSON.stringify(this.rangeFilters));
      Object.assign(copy.Study.admission, this.calculatePercent(copy.Study.admission));
      Object.assign(copy.Study.completion, this.calculatePercent(copy.Study.completion));
      Object.assign(copy.Study.retention, this.calculatePercent(copy.Study.retention));
      Object.assign(copy.Aid.pell, this.calculatePercent(copy.Aid.pell));
      Object.assign(copy.Aid.loan, this.calculatePercent(copy.Aid.loan));
      Object.assign(copy.Students.female, this.calculatePercent(copy.Students.female));
      // calculating values of "mirrored" filters
      Object.assign(copy.Students.fullTime, this.calculateMirrorValues(copy.Students.fullTime));
      Object.assign(copy.Students.male, this.calculateMirrorValues(copy.Students.male));
      // flattened object
      const flattened = {};
      Object.keys(copy).forEach((key) => {
        Object.keys(copy[key]).forEach((key2) => {
          flattened[key2] = copy[key][key2];
        });
      });
      this.$emit('rangeFilterChanged', flattened);
    },
    calculateMirrorValues(obj) {
      const propMin = +obj.max ? 1 - obj.max / 100 : 0;
      const propMax = +obj.min ? 1 - obj.min / 100 : 0;
      return {
        min: propMin,
        max: propMax,
      };
    },
    calculatePercent(obj) {
      return {
        min: obj.min / 100,
        max: obj.max / 100,
      };
    },
    resetFilters() {
      this.statesSelected = [];
      Object.keys(this.checkboxFilters).forEach((key) => {
        this.checkboxFilters[key].value = false;
      });
      Object.keys(this.rangeFilters).forEach((key) => {
        Object.keys(this.rangeFilters[key]).forEach((key2) => {
          Object.assign(this.rangeFilters[key][key2], { min: '', max: '' });
        });
      });
      this.$emit('resetFilters');
    },
  },
  computed: {
    collegesStates() {
      const states = [];
      this.colleges.forEach((college) => {
        if (!states.some(state => state === college.state__name)) states.push(college.state__name);
        states.sort((a, b) => {
          if (a.toLowerCase() < b.toLowerCase()) return -1;
          if (a.toLowerCase() > b.toLowerCase()) return 1;
          return 0;
        });
      });
      return states;
    },
  },
};
</script>

<style lang="stylus" module>
  .panel
    border 2px solid white
  .subheader
    font-size 12px
  .rightMenu
    transform translateX(0%) !important
    left 0px
    top 0px
</style>