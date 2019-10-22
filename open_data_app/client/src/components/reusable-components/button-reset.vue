<template>
  <div class="my-2 text-center">
    <v-btn
     text
     @click="$emit('reset')"
    >
      Reset
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'button-reset',
};
</script>

<style scoped>

</style>