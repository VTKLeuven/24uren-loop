<template>
  <span>
    <slot name="full" :mostActiveFirstYear="mostActiveFirstYear" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="(runner, index) in mostActiveFirstYear" :key="runner.key" class="ma-0 pa-0">
              <slot :runner="runner">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="d-flex align-center text-body-2" :class="[{'py-0': dense}, textColorComp]">
                              <img v-if="index === 0" src="/jerseys/wittetrui.png" alt="White Jersey"
                                   class="fit-image"/>

                              {{ runner | fullName }} - {{ runner.lapcount }}
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
    name: "mostActiveFirstYearRunners",
    events: ['error'],
    props: {
      max: {
        type: Number,
        default: null,
        validator: function(value) {
          return value === null || value > 0;
        }
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
      mostActiveFirstYear: [],
      keys: 0,
      loading: true,
    }),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      },
    },
    watch: {
      max: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.most_active}/`, {
            params: {
              'limit': this.max,
            }
          });
          if (this.mostActiveFirstYear.length > 0) {
            this.mostActiveFirstYear = resp.data
              .filter(runner => runner.group === 1)
              .map(runner => {
                let r = this.mostActiveFirstYear.find(r => runner.id === r.id);
                runner.key = r ? r.key : this.keys++;
                return runner;
              });
          } else {
            this.mostActiveFirstYear = resp.data.filter(runner => runner.group === 1).map((runner) => {runner.key = this.keys++; return runner;});
          }
        } catch (e) {
          this.$emit('error', 'Unable to get most active runners');
        }
      },
      onLapUpdate() {
        /* There is no distinction between object creation and update */
        /* Unable to tell if we need to add one to the count */
        this.fill();
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);

        /* Find the runner whose lap got deleted */
        let i = this.mostActiveFirstYear.findIndex((runner) => {return update.data.runner.id === runner.id;});

        /* Ignore if not from top runners */
        if (i === -1) return;

        /* If the last runner loses a lap */
        if (i === this.mostActiveFirstYear.length - 1) {
          /* Refresh data (TODO: only fetch last one?)*/
          this.fill();
        } else {
          /* Remove one from their lapcount */
          this.mostActiveFirstYear[i].runner.lapcount--;
          /* Re-sort the array */
          this.mostActiveFirstYear.sort((a, b) => a.runner.lapcount - b.runner.lapcount);
        }
      }
    },
    async mounted() {
      await this.fill();
      this.loading = false;

      this.$store.dispatch('subscribe_sse', {event: 'lap_update', handler: this.onLapUpdate});
      this.$store.dispatch('subscribe_sse', {event: 'lap_delete', handler: this.onLapDelete});
    },
    beforeDestroy() {
      this.$store.dispatch('unsubscribe_sse', {event: 'lap_update', handler: this.onLapUpdate});
      this.$store.dispatch('unsubscribe_sse', {event: 'lap_delete', handler: this.onLapDelete});
    },
  }
</script>

<style scoped>
.fit-image {
  height: 50px;
  width: auto;
  margin-bottom: 10px;
  margin-right: 10px;
}
</style>