<template>
  <v-list-item-group class="mr-1">
    <v-list-item
      v-for="(item, name) in sortNames"
      :key="item.title"
      :ref="name"
      @click="handleSortClick(name)"
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
export default {
  name: 'block-sort',
  props: ['reset'],
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
      sortIsActive: false,
    };
  },
  methods: {
    handleSortClick(item) {
      this.sortIsActive = true;
      this.$emit('sortClick', this.sortNames[item]);
      setTimeout(() => {
        this.$refs[item][0].isActive = true;
        this.$refs[item][0].inactive = false;
      }, 0);
    },
    resetSort() {
      Object.keys(this.$refs).forEach((key) => {
        const item = this.$refs[key][0];
        if (item.isActive) item.isActive = false;
      });
    },
  },
  watch: {
    reset(val) {
      this.sortIsActive = !val;
    },
    sortIsActive(val) {
      if (!val) this.resetSort();
    },
  },
};
</script>

<style scoped>

</style>