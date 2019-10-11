<template>
  <v-navigation-drawer right dense>
    <v-list nav dense flat>
      <!-- Sort block -->
      <v-subheader>Sort</v-subheader>
      <v-list-item-group class="mr-1">
        <v-list-item
          v-for="icon in Object.keys(iconsNames)"
          :key="icon"
          @click="$emit('sortClick', iconsNames[icon])"
          class="mt-1 mb-0"
        >
          <v-list-item-icon>
            <v-icon>{{icon}}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{iconsNames[icon]}}
          </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
      <v-divider />
      <!-- State filter block -->
      <v-subheader>Filter</v-subheader>
        <v-list-item-group class="mr-1">
          <v-list-item>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-list-item-icon>
                  <v-icon v-on="on">mdi-map</v-icon>
                </v-list-item-icon>
              </template>
              <span>State</span>
            </v-tooltip>
            <v-list-item-action class="ml-0 mt-1 mb-0">
              <v-select
                v-model="statesSelected"
                @change="$emit('statesFilterChanged', statesSelected)"
                label="State"
                :items="collegesStates"
                color="blue-grey darken-4"
                item-color="blue-grey darken-4"
                chips
                dense
                multiple
                flat
              ></v-select>
            </v-list-item-action>
          </v-list-item>
          <v-divider />
          <!-- Range filters block -->
          <v-subheader>Finance</v-subheader>
          <template
            v-for="filter in Object.keys(rangeFilters)"
          >
            <template v-if="filter.indexOf('divider') > -1">
              <v-divider />
              <v-subheader :key="filter">
                {{rangeFilters[filter].subheader}}
              </v-subheader>
            </template>
            <v-list-item :key="filter" v-if="filter.indexOf('divider') === -1">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-list-item-icon>
                    <v-icon v-on="on">{{rangeFilters[filter].icon}}</v-icon>
                  </v-list-item-icon>
                </template>
                <span>{{rangeFilters[filter].title}}</span>
              </v-tooltip>
              <v-list-item-action
                class="d-flex flex-row align-center ml-0 mt-1 mb-0"
              >
                <v-text-field
                  v-model="rangeFilters[filter].min"
                  @input="emitRangeInput"
                  type="number"
                  min="0"
                  class="mr-1"
                  color="blue-grey darken-4"
                  placeholder=" "
                  dense
                  flat
                ></v-text-field>
                <div class="mr-1">—</div>
                <v-text-field
                  v-model="rangeFilters[filter].max"
                  @input="emitRangeInput"
                  type="number"
                  min="0"
                  color="blue-grey darken-4"
                  placeholder=" "
                  dense
                  flat
                ></v-text-field>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-divider />
          <!-- Other filters block -->
          <v-subheader>Other</v-subheader>
          <v-list-item
            v-for="filter in Object.keys(checkboxFilters)"
            :key="filter"
             class="mr-1"
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
                <v-list-item-title>{{filter}}</v-list-item-title>
              </v-list-item-content>
            </template>
          </v-list-item>
        </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'menu-right-colleges',
  props: ['colleges'],
  data() {
    return {
      iconsNames: {
        'mdi-alphabetical': 'Name',
        'mdi-currency-usd': 'Cost',
        'mdi-credit-card-outline': 'Payments',
        'mdi-percent': 'Admission',
        'mdi-cash': 'Earnings',
      },
      checkboxFilters: {
        Operating: {
          value: false,
          name: 'cur_operating',
        },
        'Online-only': {
          value: false,
          name: 'online_only',
        },
        'Men-only': {
          value: false,
          name: 'men_only',
        },
        'Women-only': {
          value: false,
          name: 'women_only',
        },
        'Predominantly black': {
          value: false,
          name: 'predom_black',
        },
        'Predominantly hispanic': {
          value: false,
          name: 'hispanic',
        },
      },
      statesSelected: [],
      rangeFilters: {
        cost: {
          min: '',
          max: '',
          icon: 'mdi-currency-usd',
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
          icon: 'mdi-cash',
          name: 'median_earnings',
          title: 'Earnings after attending $',
        },
        'divider-1': {
          subheader: 'Aid',
        },
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
        'divider-2': {
          subheader: 'Study',
        },
        admission: {
          min: '',
          max: '',
          icon: 'mdi-school',
          name: 'admission_rate',
          title: 'Admission rate %',
        },
        completion: {
          min: '',
          max: '',
          icon: 'mdi-certificate',
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
        'divider-3': {
          subheader: 'Tests',
        },
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
        'divider-4': {
          subheader: 'Students',
        },
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
    };
  },
  methods: {
    tickCheckbox(filter) {
      this.checkboxFilters[filter].value = !this.checkboxFilters[filter].value;
      this.$emit('checkboxFilterChanged', this.checkboxFilters);
    },
    emitRangeInput() {
      const copy = JSON.parse(JSON.stringify(this.rangeFilters));
      Object.assign(copy.admission, this.calculatePercent(copy.admission));
      Object.assign(copy.completion, this.calculatePercent(copy.completion));
      Object.assign(copy.retention, this.calculatePercent(copy.retention));
      Object.assign(copy.pell, this.calculatePercent(copy.pell));
      Object.assign(copy.loan, this.calculatePercent(copy.loan));
      Object.assign(copy.female, this.calculatePercent(copy.female));
      // calculating values of "mirrored" filters
      Object.assign(copy.fullTime, this.calculateMirrorValues(copy.fullTime));
      Object.assign(copy.male, this.calculateMirrorValues(copy.male));
      // deleting dividers
      Object.keys(copy).forEach((key) => {
        if (key.indexOf('divider') > -1) delete copy[key];
      });
      this.$emit('rangeFilterChanged', copy);
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

<style scoped>

</style>