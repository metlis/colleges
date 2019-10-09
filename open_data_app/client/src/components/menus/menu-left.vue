<template>
  <v-navigation-drawer expand-on-hover permanent>
    <v-list nav dense>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-school</v-icon>
        </v-list-item-icon>
        <v-list-item-title>My colleges</v-list-item-title>
      </v-list-item>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-google-maps</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Map</v-list-item-title>
      </v-list-item>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-compare</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Compare</v-list-item-title>
      </v-list-item>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-history</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Analyze history</v-list-item-title>
      </v-list-item>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-eye-plus</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Similar colleges</v-list-item-title>
      </v-list-item>
      <v-list-item link>
        <v-list-item-icon>
          <v-icon>mdi-file-search</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Search history</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'menu-left',
};
</script>

<style scoped>

</style>