<template>
  <v-app>
    <layout-content
      v-if="hasColleges && !isFetching"
      :favourites="favouriteColleges"
      :visited="visitedColleges"
    />
    <layout-empty v-if="!hasColleges && !isFetching" />
    <layout-progress v-if="isFetching" />
  </v-app>
</template>

<script>
import LayoutContent from './layouts/layout-content.vue';
import LayoutEmpty from './layouts/layout-empty.vue';
import LayoutProgress from './layouts/layout-progress.vue';

export default {
  components: { LayoutContent, LayoutEmpty, LayoutProgress },
  data() {
    return {
      isFetching: true,
      favouriteColleges: [],
      visitedColleges: [],
    };
  },
  computed: {
    hasColleges() {
      return this.favouriteColleges.length > 0 || this.visitedColleges.length > 0;
    },
  },
  created() {
    fetch('/api/request_user_colleges/')
      .then(response => response.json())
      .then((data) => {
        const colleges = data.data;
        this.favouriteColleges = colleges.favourite;
        this.visitedColleges = colleges.visited;
      }).catch((err) => {
        console.error(err);
      })
      .finally(() => {
        this.isFetching = false;
      });
  },
};
</script>

<style>
</style>
