<template>
  <v-content>
    <v-container fluid>
      <v-row
        style="height: 80vh"
        align="center"
        justify="center"
      >
        <v-col cols="12">
          <div style="text-align: center">
            <v-progress-circular
              :size="50"
              color="#CFD8DC"
              indeterminate />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
export default {
  name: 'progress',
};
</script>

<style scoped>

</style>