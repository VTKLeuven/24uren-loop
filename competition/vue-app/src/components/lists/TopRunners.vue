<template>
  <span>
    <slot name="full" :runners="filteredRunners" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="(runner, index) in filteredRunners" :key="runner.key" class="ma-0 pa-0">
              <slot :runner="runner">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="d-flex align-center text-body-2" :class="[{'py-0': dense}, textColorComp]">
                              <img v-if="index === 0" src="/jerseys/groenetrui.png" alt="Green Jersey" class="fit-image"/>
                              {{ runner | fullName }} - {{ runner.fastest_lap.duration | durationFilter }}
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
    name: "TopRunners",
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
      runners: [],
      keys: 0,
      loading: true,
    }),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      },
      filteredRunners: function() {
        return this.runners.filter(runner => runner.fastest_lap);
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
          let resp = await this.axios.get(`${this.$store.state.urls.top_runners}/`, {
            params: {
            'limit': this.max,
            }
          });
          if (this.runners.length > 0) {
            /* Retrieve the correct key for each lap */
            this.runners = resp.data.map((runner) => {
              let r = this.runners.find((r) => {return r.id === runner.id});
              if (r) {
                runner.key = r.key;
              } else {
                runner.key = this.keys++;
              }
              return runner;
            });
          } else {
            /* Generate new keys for all laps */
            this.runners = resp.data.map((runner) => {runner.key = this.keys++; return runner});
          }
        } catch (e) {
          this.$emit('error', 'Unable to get top runners');
        }
      },
      onLapUpdate(resp) {
        let update = JSON.parse(resp.data);

        let i = this.runners.findIndex((runner) => {return runner.fastest_lap.id == update.data.id});
        if (i !== -1) {
          /* If a lap within the list is updated and duration is larger */
          let runner = this.runners[i];
          if (update.data.duration > runner.fastest_lap.duration) {
            this.fill();
          } else {
            delete update.data.runner;
            this.runners[i].fastest_lap = update.data;
            this.runners.sort((a, b) => {return (a.fastest_lap.duration < b.fastest_lap.duration) ? -1 :
                                                ((a.fastest_lap.duration > b.fastest_lap.duration) ? 1 : 0)});
          }
        } else if (this.runners[this.runners.length - 1].fastest_lap.duration > update.data.duration) {
          /* Else if lap duration is smaller than largest in list */
          let ri = this.runners.findIndex((runner) => {return runner.id == update.data.runner.id});
          if (ri !== -1) {
            /* If lap is from runner in the list */
            this.runners[ri].fastest_lap = update.data;
          } else {
            /* Else get runner from this lap and add duration */
            let runner = update.data.runner;
            runner.key = this.keys++;
            let lap = update.data;
            delete lap.runner
            runner.fastest_lap = lap;
            this.runners.splice(this.runners.length - 1, 1)
            this.runners.push(runner);
          }
          this.runners.sort((a, b) => {return (a.fastest_lap.duration < b.fastest_lap.duration) ? -1 :
                                              ((a.fastest_lap.duration > b.fastest_lap.duration) ? 1 : 0)});
        }

        return update;
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);

        if (this.runners.find((runner) => {return runner.fastest_lap.id === update.data.id}))
          this.fill();
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
    }
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