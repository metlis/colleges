<template>
  <v-content>
    <v-container fluid>
      <v-row>
        <v-col cols="3"></v-col>
        <v-col cols="7">
          <v-row>
            <v-col cols="6" v-for="college in localColleges" :key="college.id">
              <v-card>
                <v-card-title>{{college.name}}</v-card-title>
                <v-card-text>
                  <span @click="openCollegeUrl(college.url)" style="cursor: pointer">
                    {{college.url}}
                  </span>
                </v-card-text>
                <v-card-actions>
                  <v-btn icon>
                    <v-icon color="amber" @click="removeCollege(college.id)">mdi-heart</v-icon>
                  </v-btn>
                  <v-btn outlined text @click="openCollegePage(college.id, college.slug)">
                    Page
                  </v-btn>
                  <div class="flex-grow-1"></div>
                  <v-btn
                    icon
                    @click="handleChevronClick(college.id)"
                  >
                    <v-icon>
                      {{ cardsStates[college.id] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                    </v-icon>
                  </v-btn>
                </v-card-actions>
                <v-expand-transition>
                  <div v-show="cardsStates[college.id]">
                    <v-card-text>
                      I'm a thing. But, like most politicians, he promised more.
                    </v-card-text>
                  </div>
                </v-expand-transition>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="2"></v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
export default {
  name: 'content-layout',
  props: ['colleges'],
  data() {
    return {
      localColleges: [],
      cardsStates: {},
    };
  },
  methods: {
    removeCollege(id) {
      this.localColleges.forEach((col, index, obj) => {
        if (col.id === id) {
          obj.splice(index, 1);
        }
      });
    },
    openCollegePage(id, slug) {
      const url = `/institution/${id}/${slug}`;
      window.open(url, '_self');
    },
    openCollegeUrl(url) {
      window.open(`//${url}`, '_self');
    },
    handleChevronClick(id) {
      if (!this.cardsStates[id]) {
        this.$set(this.cardsStates, id, true);
      } else {
        this.cardsStates[id] = !this.cardsStates[id];
      }
    },
  },
  created() {
    this.localColleges = this.colleges;
  },
};
</script>

<style scoped>

</style>