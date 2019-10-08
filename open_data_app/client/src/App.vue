<template>
  <v-app>
    <content-layout v-if="colleges.length > 0 && !isFetching" :colleges="colleges" />
    <empty-layout v-if="colleges.length === 0 && !isFetching" />
    <progress-layout v-if="isFetching" />
  </v-app>
</template>

<script>
import ContentLayout from './layouts/content-layout.vue';
import EmptyLayout from './layouts/empty-layout.vue';
import ProgressLayout from './layouts/progress-layout.vue';

export default {
  components: { ContentLayout, EmptyLayout, ProgressLayout },
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
        console.log(data.data);
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
