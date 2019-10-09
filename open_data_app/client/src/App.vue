<template>
  <v-app>
    <layout-content v-if="colleges.length > 0 && !isFetching" :colleges="colleges" />
    <layout-empty v-if="colleges.length === 0 && !isFetching" />
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
      colleges: [],
    };
  },
  created() {
    fetch('/api/get_favourites')
      .then(response => response.json())
      .then((data) => {
        this.colleges = data.data;
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
