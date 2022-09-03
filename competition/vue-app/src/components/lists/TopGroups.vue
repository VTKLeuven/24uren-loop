<template>
  <span>
    <slot name="full" :groups="groups" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="group in groups" :key="group.key" class="ma-0 pa-0">
              <slot :group="group">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="text-center text-body-2" :class="[{'py-0': dense}, textColorComp]">
                              {{ group.name }} - {{ group.score }}
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card>
                  </v-col>
                </v-row>
              </slot>
            </v-list-item>
          </v-scroll-x-transition>
        </v-list>
      </v-container>
    </slot>
  </span>
</template>

<script>
  export default {
    name: "TopGroups",
    events: ['error'],
    props: {
      max: {
        type: Number,
        default: null,
      },
      dense: {
        type: Boolean,
        default: false,
      },
      color: {
        default: 'tertiary'
      },
      textColor: {
        default: 'tertiary-text'
      },
      cardColor: {
        default: 'tertiary'
      }
    },
    data: () => ({
      groups: [],
      keys: 0,
      loading: true,
    }),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      }
    },
    watch: {
      max: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.top_groups}/`, {
            params: {
              'limit': this.max,
            }
          });

          if (this.groups.length > 0) {
            this.groups = resp.data.map((group) => {
              let g = this.groups.find((g) => {return group.id === g.id});
              group.key = g ? g.key : this.keys++;
              return group;
            })
          } else {
            this.groups = resp.data.map((group) => {group.key = this.keys++; return group;});
          }
        } catch (e) {
          this.$emit('error');
        }
      },
      onGroupScoreUpdate() {
        // TODO: make this method update correctly
        this.fill();
      },
    },
    async mounted() {
      await this.fill();
      this.loading = false;

      this.$store.dispatch('subscribe_sse', {event: 'group_score_update', handler: this.onGroupScoreUpdate});
    },
    beforeDestroy() {
      this.$store.dispatch('unsubscribe_sse', {event: 'group_score_update', handler: this.onGroupScoreUpdate});
    }
  }
</script>

<style scoped>

</style>