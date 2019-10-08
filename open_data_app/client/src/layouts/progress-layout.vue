<template>
  <v-content>
    <v-container fluid>
      <v-row
        align="center"
        justify="center"
      >
        <v-col cols="12">
          <div style="text-align: center">
            <v-progress-circular
              :size="50"
              color="primary"
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