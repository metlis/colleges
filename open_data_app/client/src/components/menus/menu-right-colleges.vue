<template>
  <v-navigation-drawer right dense>
    <v-list nav dense flat>
      <v-subheader>Sort</v-subheader>
      <v-list-item-group>
        <v-list-item
          v-for="icon in Object.keys(iconsNames)"
          :key="icon"
          @click="$emit('sortClick', iconsNames[icon])"
        >
          <v-list-item-icon>
            <v-icon>{{icon}}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{iconsNames[icon]}}
          </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
      <v-subheader>Filter</v-subheader>
        <v-list-item-group>
          <v-list-item
            v-for="filter in Object.keys(checkboxFilters)"
            :key="filter"
          >
            <template v-slot:default="{ active, toggle }">
              <v-list-item-action>
                <v-checkbox
                  @change="$emit('checkboxFilterChanged', checkboxFilters)"
                  v-model="checkboxFilters[filter].value"
                  color="blue-grey darken-4"
                ></v-checkbox>
              </v-list-item-action>
              <v-list-item-content
                @click="tickCheckbox(filter)">
                <v-list-item-title>{{filter}}</v-list-item-title>
              </v-list-item-content>
            </template>
          </v-list-item>
          <v-list-item>
            <v-list-item-action>
              <v-select
                v-model="statesSelected"
                @change="$emit('statesFilterChanged', statesSelected)"
                label="State"
                :items="collegesStates"
                color="blue-grey darken-4"
                item-color="blue-grey darken-4"
                chips
                deletable-chips
                dense
                multiple
                flat
                outlined
              ></v-select>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>State</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

            <v-list-item>
                <v-list-item-action>
                  <v-text-field
                    v-model="slider"
                    placeholder="Tuition"
                    class="mt-0 pt-0"
                    single-line
                    type="number"
                    min="0"
                    dense
                  ></v-text-field>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>Tuition</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'menu-right-colleges',
  props: ['colleges'],
  data() {
    return {
      iconsNames: {
        'mdi-alphabetical': 'Name',
        'mdi-currency-usd': 'Cost',
        'mdi-credit-card-outline': 'Payments',
        'mdi-percent': 'Admission',
        'mdi-cash': 'Earnings',
      },
      checkboxFilters: {
        Operating: {
          value: false,
          name: 'cur_operating',
        },
        'Online-only': {
          value: false,
          name: 'online_only',
        },
        'Men-only': {
          value: false,
          name: 'men_only',
        },
        'Women-only': {
          value: false,
          name: 'women_only',
        },
        'Predominantly black': {
          value: false,
          name: 'predom_black',
        },
        'Predominantly hispanic': {
          value: false,
          name: 'hispanic',
        },
      },
      statesSelected: [],
      slider: '',
    };
  },
  methods: {
    tickCheckbox(filter) {
      this.checkboxFilters[filter].value = !this.checkboxFilters[filter].value;
      this.$emit('checkboxFilterChanged', this.checkboxFilters);
    },
  },
  computed: {
    collegesStates() {
      const states = [];
      this.colleges.forEach((college) => {
        if (!states.some(state => state === college.state__name)) states.push(college.state__name);
        states.sort((a, b) => {
          if (a.toLowerCase() < b.toLowerCase()) return -1;
          if (a.toLowerCase() > b.toLowerCase()) return 1;
          return 0;
        });
      });
      return states;
    },
  },
};
</script>

<style scoped>

</style>