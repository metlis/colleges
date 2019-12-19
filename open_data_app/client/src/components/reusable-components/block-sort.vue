<template>
  <v-list-item-group class="mr-1">
    <v-list-item
      v-for="(item, name) in sortNames"
      :key="item.title"
      :ref="name"
      @click="emitSortEvent(name)"
      class="mt-1 mb-0"
    >
      <v-list-item-icon>
        <v-icon>{{item.icon}}</v-icon>
      </v-list-item-icon>
      <v-list-item-title>
        {{item.title}}
      </v-list-item-title>
    </v-list-item>
  </v-list-item-group>
</template>

<script>
import { sortNames } from '../../utils/dictionaries';

export default {
  name: 'block-sort',
  props: ['restore'],
  data() {
    return {
      sortNames: sortNames(),
      toggleSort: false,
    };
  },
  methods: {
    emitSortEvent(item) {
      this.toggleSort = true;
      this.$emit('sortClick', this.sortNames[item]);
      setTimeout(() => {
        this.$refs[item][0].isActive = true;
        this.$refs[item][0].inactive = false;
      }, 0);
    },
    clearSort() {
      Object.keys(this.$refs).forEach((key) => {
        const item = this.$refs[key][0];
        if (item.isActive) item.isActive = false;
      });
    },
  },
  watch: {
    restore(val) {
      this.toggleSort = !val;
      if (!this.toggleSort) this.clearSort();
    },
  },
};
</script>

<style scoped>

</style>