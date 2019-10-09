<template>
  <v-navigation-drawer expand-on-hover permanent>
    <v-list nav dense>
      <v-list-item-group v-model="activeItem">
        <v-list-item
          v-for="icon in Object.keys(iconsNames)"
          :key="icon"
          @click="$emit('buttonClick', icon)"
          link
        >
          <v-list-item-icon>
            <v-icon>
              {{icon}}
            </v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{iconsNames[icon]}}
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
        'mdi-school': 'My colleges',
        'mdi-google-maps': 'Map',
        'mdi-compare': 'Compare',
        'mdi-history': 'Analyze history',
        'mdi-eye-plus': 'Similar colleges',
        'mdi-file-search': 'Search history',
      },
      activeItem: 0,
    };
  },
};
</script>

<style scoped>

</style>