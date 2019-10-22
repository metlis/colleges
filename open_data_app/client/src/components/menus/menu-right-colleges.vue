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
      <block-sort
        :reset="resetSort"
        @sortClick="handleSort"
      />
      <v-divider />
      <!-- State filter block -->
      <v-subheader>Filter</v-subheader>
      <block-filter
        :states="collegesStates"
        :reset="resetFilter"
        @statesFilterChanged="handleStateFilter"
        @rangeFilterChanged="handleRangeFilter"
        @checkboxFilterChanged="handleCheckboxFilter"
      />
      <br>
      <!--  Reset button  -->
      <div class="my-2 text-center">
        <v-btn
         text
         @click="reset"
        >
          Reset
        </v-btn>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import BlockSort from '../reusable-components/block-sort.vue';
import BlockFilter from '../reusable-components/block-filter.vue';

export default {
  name: 'menu-right-colleges',
  components: { BlockSort, BlockFilter },
  props: ['colleges'],
  data() {
    return {
      resetSort: false,
      resetFilter: false,
    };
  },
  methods: {
    reset() {
      this.resetSort = true;
      this.resetFilter = true;
      this.$emit('reset');
    },
    handleSort(payload) {
      this.$emit('sortClick', payload);
      this.resetSort = false;
    },
    handleStateFilter(payload) {
      this.$emit('statesFilterChanged', payload);
      this.resetFilter = false;
    },
    handleRangeFilter(payload) {
      this.$emit('rangeFilterChanged', payload);
      this.resetFilter = false;
    },
    handleCheckboxFilter(payload) {
      this.$emit('checkboxFilterChanged', payload);
      this.resetFilter = false;
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
  .rightMenu
    transform translateX(0%) !important
    left 0px
    top 0px
</style>