<template>
  <v-navigation-drawer
    right
    dense
    absolute
    :class="$style.filterMenu"
    width="100%"
  >
    <v-list nav dense flat>
      <!-- Sort block -->
      <v-subheader>Sort</v-subheader>
      <block-sort
        :restore="toggleSort"
        @sortClick="emitSortEvent"
      />
      <v-divider />
      <!-- Filter block -->
      <v-subheader>Filter</v-subheader>
      <block-filter
        :states="collegesStatesNames"
        :restore="toggleFilter"
        @statesFilterChanged="emitFilterEvent('statesFilterChanged', 'statesFilters', $event)"
        @rangeFilterChanged="emitFilterEvent('rangeFilterChanged', 'rangeFilters', $event)"
        @checkboxFilterChanged="emitFilterEvent('checkboxFilterChanged', 'checkboxFilters', $event)"
      />
      <br>
      <!--  Reset button  -->
      <button-reset @reset="restoreInitialCollegesList" />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import BlockSort from '../reusable-components/block-sort.vue';
import BlockFilter from '../reusable-components/block-filter.vue';
import ButtonReset from '../reusable-components/button-reset.vue';
import { getCollegesStatesNames } from '../../utils/helpers';

export default {
  name: 'menu-filter-and-sort',
  components: { BlockSort, BlockFilter, ButtonReset },
  props: ['colleges', 'name'],
  data() {
    return {
      toggleSort: false,
      toggleFilter: false,
    };
  },
  methods: {
    restoreInitialCollegesList() {
      this.toggleSort = true;
      this.toggleFilter = true;
      this.$emit('restore');
    },
    emitSortEvent(payload) {
      this.$emit('sortClick', { value: payload, menu: this.name });
      this.toggleSort = false;
    },
    emitFilterEvent(eventName, filters, payload) {
      this.$emit(eventName, { value: payload, menu: this.name, filters });
      this.toggleFilter = false;
    },
  },
  computed: {
    collegesStatesNames() {
      return getCollegesStatesNames(this.colleges);
    },
  },
};
</script>

<style lang="stylus" module>
  .filterMenu
    transform translateX(0%) !important
    left 0px
    top 0px
    ::-webkit-scrollbar
      display none
</style>