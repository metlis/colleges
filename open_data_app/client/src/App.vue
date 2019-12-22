<template>
  <v-app>
    <layout-content
      v-if="hasColleges && !isFetching"
      :favourites="favouriteColleges"
      :visited="visitedColleges"
      :recommended="recommendedColleges"
      :page="activePage"
      :credentials="scorecardApiCredentials"
      @fetchRecommendedColleges="fetchRecommendedColleges"
      @fetchScorecardApiCredentials="fetchScorecardApiCredentials"
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
      recommendedColleges: [],
      activePage: 'Favourite',
      scorecardApiCredentials: '',
    };
  },
  methods: {
    fetchRecommendedColleges() {
      this.isFetching = true;
      fetch('/api/request_similar_colleges/')
        .then(response => response.json())
        .then((data) => {
          this.recommendedColleges = data.data;
        }).catch((err) => {
          console.error(err);
        })
        .finally(() => {
          this.isFetching = false;
          this.activePage = 'Recommended';
        });
    },
    fetchUserColleges() {
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
    fetchScorecardApiCredentials() {
      this.isFetching = true;
      fetch('/api/request_scorecard_api_credentials/')
        .then(response => response.json())
        .then((data) => {
          this.scorecardApiCredentials = data.data;
        }).catch((err) => {
          console.error(err);
        })
        .finally(() => {
          this.isFetching = false;
          this.activePage = 'History';
        });
    },
  },
  computed: {
    hasColleges() {
      return this.favouriteColleges.length > 0 || this.visitedColleges.length > 0;
    },
  },
  created() {
    this.fetchUserColleges();
  },
};
</script>

<style>
</style>
