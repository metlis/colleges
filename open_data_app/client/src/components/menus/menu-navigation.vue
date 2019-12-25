<template>
  <v-navigation-drawer
    dense
    :class="$style.navigationMenu"
    width="100%"
  >
    <v-list nav dense>
      <v-list-item-group v-model="activeItem">
        <v-list-item
          v-for="(icon, name) in iconsNames"
          :key="name"
          :ref="icon"
          @click="$emit('navigationClick', icon)"
          link
        >
          <v-list-item-icon>
            <v-icon>
              {{name}}
            </v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{icon}}
          </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'menu-left',
  props: ['initial'],
  data() {
    return {
      iconsNames: {
        'mdi-star': 'Favourite',
        'mdi-compare': 'Compare',
        'mdi-google-maps': 'Map',
        'mdi-history': 'History',
        'mdi-file-search': 'Visited',
        'mdi-eye-plus': 'Recommended',
      },
      activeItem: 0,
    };
  },
  mounted() {
    // programmatically set initial active item. the first item is active by default
    try {
      this.$refs[this.initial][0].isActive = true;
      if (this.initial !== 'Favourite') this.$refs.Favourite[0].isActive = false;
    } catch (e) {
      console.error(e);
    }
  },
};
</script>

<style lang="stylus" module>
  .navigationMenu
    transform translateX(0%) !important
</style>