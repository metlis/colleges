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
  data() {
    return {
      iconsNames: {
        'mdi-star': 'Favourite',
        'mdi-google-maps': 'Map',
        'mdi-file-search': 'Visited',
        'mdi-compare': 'Compare',
        // 'mdi-history': 'Analyze history',
        // 'mdi-eye-plus': 'Similar colleges',
      },
      activeItem: 0,
    };
  },
};
</script>

<style lang="stylus" module>
  .navigationMenu
    transform translateX(0%) !important
</style>