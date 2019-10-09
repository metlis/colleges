<template>
  <v-content>
    <v-container fluid style="padding: 0px">
      <v-row>
        <v-col cols="2" style="padding: 0px">
          <menu-left @navigationClick="changeNavButton" />
        </v-col>
        <v-col cols="7">
          <content-colleges
             v-if="activeNavButton === 'Colleges'"
            :colleges="colleges"
            :activeSortButton="activeSortButton"
            :prevSortButton="prevSortButton"
          />
        </v-col>
        <v-col cols="2" offset="1" style="padding: 0px">
          <menu-right-colleges
            v-if="activeNavButton === 'Colleges'"
            @sortClick="changeSortButton"
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
      activeNavButton: 'Colleges',
      activeSortButton: '',
      prevSortButton: '',
    };
  },
  methods: {
    changeNavButton(val) {
      this.activeNavButton = val;
    },
    changeSortButton(val) {
      if (this.activeSortButton) this.prevSortButton = this.activeSortButton;
      this.activeSortButton = val;
      setTimeout(() => {
        this.$root.$emit('sort-click');
      }, 0);
    },
  },
};
</script>

<style scoped>
</style>