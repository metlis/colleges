<template>
  <v-content>
    <v-container fluid>
      <v-row
        align="center"
        justify="center"
        :class="$style.content"
      >
        <v-col cols="12">
          <div :class="$style.progress">
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

<style lang="stylus" module>
  .content
    height 80vh
  .progress
    text-align center
</style>