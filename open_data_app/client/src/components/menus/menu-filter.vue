<template>
  <v-navigation-drawer
    right
    dense
    absolute
    :class="$style.filterMenu"
    width="100%"
  >
    <v-list nav dense flat>
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
import BlockFilter from '../reusable-components/block-filter.vue';
import ButtonReset from '../reusable-components/button-reset.vue';
import { getCollegesStatesNames } from '../../utils/helpers';

export default {
  name: 'menu-filter',
  props: ['colleges', 'name'],
  components: { BlockFilter, ButtonReset },
  data() {
    return {
      toggleFilter: false,
    };
  },
  methods: {
    restoreInitialCollegesList() {
      this.toggleFilter = true;
      this.$emit('restore');
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