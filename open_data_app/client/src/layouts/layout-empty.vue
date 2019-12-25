<template>
  <v-content>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-alert
            type="info"
            border="left"
            color="#FFAB91"
          >
            Add some colleges to favourites. You can start your search <a href="/main/">here</a>
          </v-alert>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
export default {
  name: 'empty-layout',
};
</script>

<style scoped  lang="stylus">
  a
    color white !important
    font-weight bold
</style>