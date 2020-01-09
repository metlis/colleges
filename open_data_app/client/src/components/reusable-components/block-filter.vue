<template>
  <v-expansion-panels
    accordion
    class="mx-0 px-0"
    v-model="panels"
  >
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
            :items="states"
            dense
            multiple
            flat
            color="blue-grey darken-4"
            item-color="blue-grey darken-4"
          />
        </v-list-item-action>
      </v-list-item>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <!--  Range filters  -->
      <v-expansion-panel
        v-for="(value, key) in rangeFilters"
        :key="key"
        :class="$style.panel"
        class="mt-0"
      >
        <v-expansion-panel-header class="px-3">
          {{key}}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <template v-for="(filter, name) in value">
            <v-subheader
              inset
              class="pl-0"
              :class="$style.subheader"
              :key="filter.title"
            >
              {{filter.title}}
            </v-subheader>
            <v-list-item
              :key="name"
              class="px-0"
            >
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-list-item-icon>
                    <v-icon v-on="on">
                      {{filter.icon}}
                    </v-icon>
                  </v-list-item-icon>
                </template>
                <span>{{filter.title}}</span>
              </v-tooltip>
              <v-list-item-action
                class="d-flex flex-row align-center ml-0 mt-1 mb-0"
              >
                <v-text-field
                  v-model="filter.min"
                  @input="emitRangeInputEvent"
                  dense
                  flat
                  type="number"
                  min="0"
                  color="blue-grey darken-4"
                />
                <div class="mr-1">-</div>
                <v-text-field
                  v-model="filter.max"
                  @input="emitRangeInputEvent"
                  dense
                  flat
                  type="number"
                  min="0"
                  color="blue-grey darken-4"
                />
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
            v-for="(filter, key) in checkboxFilters"
            :key="key"
             class="mx-0 px-0"
          >
        <template v-slot:default="{ active, toggle }">
          <v-list-item-action class="mt-1 mb-0">
            <v-checkbox
              @change="$emit('checkboxFilterChanged', checkboxFilters)"
              v-model="filter.value"
              color="blue-grey darken-4"
            />
          </v-list-item-action>
          <v-list-item-content
            @click="emitCheckboxEvent(key)">
            <v-list-item-title>
              {{filter.title}}
            </v-list-item-title>
          </v-list-item-content>
        </template>
      </v-list-item>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-list-item-group>
  </v-expansion-panels>
</template>

<script>
import { rangeFilters, checkboxFilters } from '../../utils/dictionaries';

export default {
  name: 'block-filter',
  props: ['states', 'restore'],
  data() {
    return {
      checkboxFilters: checkboxFilters(),
      rangeFilters: rangeFilters(),
      statesSelected: [],
      toggleFilter: false,
      panels: [],
    };
  },
  methods: {
    emitCheckboxEvent(filter) {
      this.checkboxFilters[filter].value = !this.checkboxFilters[filter].value;
      this.$emit('checkboxFilterChanged', this.checkboxFilters);
    },
    emitRangeInputEvent() {
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
    // We use this method if we need to calculate a value for binary properties.
    // For example, we don't have a separate property for the percent of male students,
    // so we calculate its value by using the percent of female students.
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
    clearFilters() {
      this.panels = [];
      this.statesSelected = [];
      Object.keys(this.checkboxFilters).forEach((key) => {
        this.checkboxFilters[key].value = false;
      });
      Object.keys(this.rangeFilters).forEach((key) => {
        Object.keys(this.rangeFilters[key]).forEach((key2) => {
          Object.assign(this.rangeFilters[key][key2], { min: '', max: '' });
        });
      });
    },
  },
  watch: {
    restore(val) {
      this.toggleFilter = !val;
      if (!this.toggleFilter) this.clearFilters();
    },
  },
};
</script>

<style lang="stylus" module>
  .panel
    border 2px solid white
  .subheader
    font-size 12px
</style>