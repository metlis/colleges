<template>
  <div>
    <!--   Chips     -->
    <div
      v-if="collegesToComparisonIds.length > 0"
      ref="checkbox"
    >
      <p>
        <v-chip
          v-for="c in collegesToComparisonIds"
          :key="c"
          @click:close="removeCollegeFromComparison(c)"
          class="ma-2"
          close
        >
          {{getCollegeName(c)}}
        </v-chip>
      </p>
    </div>
    <!--   Selection buttons     -->
    <div :class="$style.buttons">
      <v-btn
        v-if="collegesToComparisonIds.length !== colleges.length"
        @click="selectAllColleges"
        depressed
        small
      >
        Select all
      </v-btn>
      <v-btn
        v-if="collegesToComparisonIds.length > 1"
        @click="commitAction"
        depressed
        small
      >
        {{actionButton}}
      </v-btn>
      <v-btn
        v-if="collegesToComparisonIds.length > 0"
        @click="collegesToComparisonIds = []"
        depressed
        small
      >
        Clear
      </v-btn>
    </div>
    <!--  Checkbox list  -->
    <div>
      <v-checkbox
        v-for="c in colleges"
        :label="c.name"
        :value="c.id"
        :key="c.id"
        :class="$style.college"
        v-model="collegesToComparisonIds"
        color="blue-grey darken-3"
        hide-details
      />
    </div>
    <div
      v-if="showActionButton"
      :class="$style.buttonContainer"
    >
      <v-btn
        @click="commitAction"
        depressed
        medium
      >
        {{actionButton}}
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'checkbox-list',
  props: ['collegesData', 'selectedIds', 'actionButton'],
  data() {
    return {
      collegesToComparisonIds: this.selectedIds,
      colleges: this.collegesData,
    };
  },
  methods: {
    removeCollegeFromComparison(id) {
      this.collegesToComparisonIds = this.collegesToComparisonIds.filter(c => c !== id);
    },
    getCollegeName(id) {
      const college = this.colleges.find(c => c.id === id);
      if (college) return college.name;
      return '';
    },
    selectAllColleges() {
      this.collegesToComparisonIds = [];
      this.colleges.forEach((c) => {
        this.collegesToComparisonIds.push(c.id);
      });
    },
    showActionButton() {
      if (this.collegesToComparisonIds.length < 2) return false;
      return true;
    },
    commitAction() {
      this.$emit('update:selectedIds', this.collegesToComparisonIds);
      this.$emit('action');
    },
  },
};
</script>

<style lang="stylus" module>
  .college
    label
      margin-bottom 0px !important
  .buttonContainer
    display flex
    justify-content flex-end
    margin-top 20px
    width 100%
  .buttons
    display flex
    justify-content flex-end
    button
      margin-right 5px !important
</style>