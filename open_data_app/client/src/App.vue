<template>
  <div>Hello world!</div>
</template>

<script>
export default {
  created() {
    fetch('/api/get_favourites')
      .then(response => response.json())
      .then(data => console.log(data));
  },
};
</script>

<style>
</style>
