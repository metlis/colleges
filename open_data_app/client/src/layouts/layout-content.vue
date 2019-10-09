<template>
  <v-content>
    <v-container fluid style="padding: 0px">
      <v-row>
        <v-col cols="2" style="padding: 0px">
          <menu-left @buttonClick="changeView" />
        </v-col>
        <v-col cols="7">
          <content-colleges
            :colleges="colleges"
             v-if="activeButton === 'mdi-school'"
          />
        </v-col>
        <v-col cols="2" offset="1" style="padding: 0px">
          <menu-right-colleges
            v-if="activeButton === 'mdi-school'"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import MenuLeft from '../components/menus/menu-left.vue';
import MenuRightColleges from '../components/menus/menu-right-colleges.vue';
import ContentColleges from '../components/contents/content-colleges.vue';

export default {
  name: 'content-layout',
  components: { MenuLeft, MenuRightColleges, ContentColleges },
  props: ['colleges'],
  data() {
    return {
      activeButton: 'mdi-school',
    };
  },
  methods: {
    changeView(val) {
      this.activeButton = val;
    },
  },
};
</script>

<style scoped>
</style>