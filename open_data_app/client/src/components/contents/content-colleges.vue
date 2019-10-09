<template>
  <v-row>
    <v-col cols="4" v-for="college in localColleges" :key="college.id">
      <v-card>
        <v-card-title style="word-break: normal !important">{{college.name}}</v-card-title>
        <v-card-text>
          <span @click="openCollegeUrl(college.url)" style="cursor: pointer">
            {{college.url}}
          </span>
          <!-- Sort values -->
          <div class="text--primary" v-if="activeSortButton === 'Cost'">
            <v-chip>
              {{addCommas(college.average_sort)}}$
            </v-chip>
          </div>
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
              <v-divider />
              <div>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span :class="$style.container" v-on="on"><v-icon>mdi-map-marker
                    </v-icon></span>
                  </template>
                  <span>Location</span>
                </v-tooltip>
                <span :class="$style.description"> {{college.city}}, {{college.state__name}}
                </span><br>
              </div>
              <div v-if="college.carnegie__description">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span :class="$style.container" v-on="on"><v-icon>mdi-city
                    </v-icon></span>
                  </template>
                  <span>Locale</span>
                </v-tooltip>
                <span :class="$style.description"> {{college.locale__description}}</span>
                <br>
              </div>
              <div v-if="college.undergrad_students">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span :class="$style.container" v-on="on"><v-icon>mdi-account-multiple
                    </v-icon></span>
                  </template>
                  <span>Undergraduate students</span>
                </v-tooltip>
                <span :class="$style.description"> {{addCommas(college.undergrad_students)}}</span>
                <br>
              </div>
              <div v-if="college.religion__name">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span :class="$style.container" v-on="on"><v-icon>mdi-church
                    </v-icon></span>
                  </template>
                  <span>Religious affiliation</span>
                </v-tooltip>
                <span :class="$style.description"> {{college.religion__name}}</span><br>
              </div>
              <div v-if="college.ownership__description">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <span :class="$style.container" v-on="on"><v-icon>mdi-cash
                    </v-icon></span>
                  </template>
                  <span>Ownership</span>
                </v-tooltip>
                <span :class="$style.description"> {{college.ownership__description}}</span>
                <br>
              </div>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'content-colleges',
  props: ['colleges', 'activeSortButton', 'prevSortButton'],
  data() {
    return {
      localColleges: [],
      cardsStates: {},
      reverseSort: false,
    };
  },
  methods: {
    removeCollege(id) {
      fetch(`/api/modify_favourites/?college_id=${id}`)
        .then(response => response.text())
        .then((data) => {
          if (data === 'Removed') {
            this.localColleges.forEach((col, index, obj) => {
              if (col.id === id) {
                obj.splice(index, 1);
                const favBadge = document.getElementById('favourite-badge');
                favBadge.innerText = String(Number(favBadge.innerText) - 1);
              }
            });
          }
        }).catch((err) => {
          console.error(err);
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
    sortColleges() {
      // set reverse sort variable upon the same button click
      if (this.prevSortButton === this.activeSortButton) {
        this.reverseSort = !this.reverseSort;
      } else {
        this.reverseSort = false;
      }
      switch (this.activeSortButton) {
      case 'Name':
        this.sortAlphabetically();
        break;
      case 'Cost':
        this.sortCost();
        break;
      default:
        break;
      }
    },
    // https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
    addCommas(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    sortAlphabetically() {
      this.localColleges.sort((a, b) => {
        if (a.name.toLowerCase() < b.name.toLowerCase()) {
          if (!this.reverseSort) return -1;
          return 1;
        }
        if (a.name.toLowerCase() > b.name.toLowerCase()) {
          if (!this.reverseSort) return 1;
          return -1;
        }
        return 0;
      });
    },
    sortCost() {
      this.localColleges.forEach((college) => {
        if (!college.average_net_price_public) {
          // eslint-disable-next-line no-param-reassign
          college.average_sort = college.average_net_price_private;
        }
        if (!college.average_net_price_private) {
          // eslint-disable-next-line no-param-reassign
          college.average_sort = college.average_net_price_public;
        }
      });
      this.localColleges.sort((a, b) => {
        if (!this.reverseSort) return Number(a.average_sort) - Number(b.average_sort);
        return Number(b.average_sort) - Number(a.average_sort);
      });
    },
  },
  created() {
    this.localColleges = this.colleges;
    this.$root.$on('sort-click', () => {
      this.sortColleges();
    });
  },
};
</script>

<style lang="stylus" module>
  .container
    display inline-block
    width 25px
    float left
    margin-right 5px
  .description
    display block
    overflow hidden
</style>