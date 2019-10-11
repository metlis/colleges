<template>
  <v-navigation-drawer right dense>
    <v-list nav dense flat>
      <v-subheader>Sort</v-subheader>
      <v-list-item-group>
        <v-list-item
          v-for="icon in Object.keys(iconsNames)"
          :key="icon"
          @click="$emit('sortClick', iconsNames[icon])"
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
      <v-subheader>Filter</v-subheader>
        <v-list-item-group>
          <v-list-item>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-list-item-icon>
                  <v-icon v-on="on">mdi-map</v-icon>
                </v-list-item-icon>
              </template>
              <span>State</span>
            </v-tooltip>
            <v-list-item-action class="ml-0">
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
            <v-list-item :key="filter"v-if="filter.indexOf('divider') === -1">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-list-item-icon>
                    <v-icon v-on="on">{{rangeFilters[filter].icon}}</v-icon>
                  </v-list-item-icon>
                </template>
                <span>{{filter}}</span>
              </v-tooltip>
              <v-list-item-action
                class="d-flex flex-row align-center ml-0"
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
          <v-subheader>Other</v-subheader>
          <v-list-item
            v-for="filter in Object.keys(checkboxFilters)"
            :key="filter"
          >
            <template v-slot:default="{ active, toggle }">
              <v-list-item-action>
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
        'Cost $': {
          min: '',
          max: '',
          icon: 'mdi-currency-usd',
          name: 'average_price',
        },
        'Monthly payments $': {
          min: '',
          max: '',
          icon: 'mdi-credit-card-outline',
          name: 'monthly_payments',
        },
        'Debt after completion $': {
          min: '',
          max: '',
          icon: 'mdi-sack-percent',
          name: 'debt_completed_median',
        },
        'Earnings after attending $': {
          min: '',
          max: '',
          icon: 'mdi-cash',
          name: 'median_earnings',
        },
        'divider-1': {
          subheader: 'Aid',
        },
        'Pell grant recipients %': {
          min: '',
          max: '',
          icon: 'mdi-cash-100',
          name: 'pell_grand',
        },
        'Federal loan recipients %': {
          min: '',
          max: '',
          icon: 'mdi-bank',
          name: 'federal_loan',
        },
        'divider-2': {
          subheader: 'Study',
        },
        'Admission rate %': {
          min: '',
          max: '',
          icon: 'mdi-school',
          name: 'admission_rate',
        },
        'Completion rate %': {
          min: '',
          max: '',
          icon: 'mdi-certificate',
          name: 'completion_rate_four_year_pooled',
        },
        'Retention rate %': {
          min: '',
          max: '',
          icon: 'mdi-account-heart',
          name: 'retention_rate_four_year_pooled',
        },
        'divider-3': {
          subheader: 'Tests',
        },
        'ACT cumulative': {
          min: '',
          max: '',
          icon: 'mdi-grease-pencil',
          name: 'act_cumulative',
        },
        'SAT average': {
          min: '',
          max: '',
          icon: 'mdi-lead-pencil',
          name: 'sat_average',
        },
        'divider-4': {
          subheader: 'Students',
        },
        'Number of undergraduates': {
          min: '',
          max: '',
          icon: 'mdi-account-multiple',
          name: 'undergrad_students',
        },
        'Full-time students %': {
          min: '',
          max: '',
          icon: 'mdi-account-clock',
          name: 'students_part_time',
        },
        'Female students %': {
          min: '',
          max: '',
          icon: 'mdi-human-female',
          name: 'students_female',
        },
        'Male students %': {
          min: '',
          max: '',
          icon: 'mdi-human-male',
          name: 'students_female',
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
      Object.assign(copy['Admission rate %'], this.calculatePercent(copy['Admission rate %']));
      Object.assign(copy['Completion rate %'], this.calculatePercent(copy['Completion rate %']));
      Object.assign(copy['Retention rate %'], this.calculatePercent(copy['Retention rate %']));
      Object.assign(copy['Pell grant recipients %'], this.calculatePercent(copy['Pell grant recipients %']));
      Object.assign(copy['Federal loan recipients %'], this.calculatePercent(copy['Federal loan recipients %']));
      Object.assign(copy['Female students %'], this.calculatePercent(copy['Female students %']));
      // calculating values of "mirrored" filters
      Object.assign(copy['Full-time students %'], this.calculateMirrorValues(copy['Full-time students %']));
      Object.assign(copy['Male students %'], this.calculateMirrorValues(copy['Male students %']));
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