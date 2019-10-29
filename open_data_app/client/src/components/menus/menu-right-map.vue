<template>
  <v-navigation-drawer
    right
    dense
    absolute
    :class="$style.rightMenu"
    width="100%"
  >
    <v-list nav dense flat>
      <!-- Filter block -->
      <v-subheader>Filter</v-subheader>
      <block-filter
        :states="collegesStates"
        :reset="resetFilter"
        @statesFilterChanged="handleFilter('statesFilterChanged', $event)"
        @rangeFilterChanged="handleFilter('rangeFilterChanged', $event)"
        @checkboxFilterChanged="handleFilter('checkboxFilterChanged', $event)"
      />
      <br>
      <!--  Reset button  -->
      <button-reset @reset="reset" />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import BlockFilter from '../reusable-components/block-filter.vue';
import ButtonReset from '../reusable-components/button-reset.vue';
import getCollegesStates from '../../utils/helpers';

export default {
  name: 'menu-right-map',
  props: ['colleges'],
  components: { BlockFilter, ButtonReset },
  data() {
    return {
      resetFilter: false,
    };
  },
  methods: {
    reset() {
      this.resetFilter = true;
      this.$emit('reset');
    },
    handleFilter(eventName, payload) {
      this.$emit(eventName, payload);
      this.resetFilter = false;
    },
  },
  computed: {
    collegesStates() {
      return getCollegesStates(this.colleges);
    },
  },
};
</script>

<style lang="stylus" module>
  .rightMenu
    transform translateX(0%) !important
    left 0px
    top 0px
</style>