<template>
  <span>
    <slot name="full" :laps="laps" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="lap in laps" :key="lap.key" class="ma-0 pa-0">
              <slot :lap="lap">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="text-center text-body-2" :class="[{'py-0': dense}, textColorComp]">
                              {{ lap.runner | fullName }} - {{ lap.duration | durationFilter }}
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
    name: "LastLapList",
    events: ['error'],
    props: {
      max: {
        type: Number,
        default: null,
        validator: function(value) {
          return value === null || value > 0;
        }
      },
      runnerId: {
        type: Number,
        default: -1,
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
      laps: [],
      keys: 0,
      loading: true,
    }),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      }
    },
    watch: {
      runnerId: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.lap}/`, {
            params: {
              'ordering': '-start_time',
              'limit': this.max,
              'duration__isnull': false,
              'runner': this.runnerId === -1 ? null : this.runnerId,
            }
          });

          if (this.laps.length > 0) {
            this.laps = resp.data.map((lap) => {
              let l = this.laps.find((l) => {return lap.id === l.id});
              if (l) {
                lap.key = l.key;
              } else {
                lap.key = this.keys++;
              }
              lap.start_time = new Date(lap.start_time);
              return lap;
            });
          } else {
            this.laps = resp.data.map((lap) => {
              lap.key = this.keys++;
              lap.start_time = new Date(lap.start_time);
              return lap;
            });
          }
        } catch (e) {
          this.$emit('error', 'Could not get laps');
        }
      },

      onLapUpdate(resp) {
        let update = JSON.parse(resp.data);
        update.data.start_time = new Date(update.data.start_time);

        if (this.runnerId === -1 || update.data.runner.id === this.runnerId) {
          /* The current runner is updated or no specific runner is selected */

          /* Get the corresponding lap */
          let lapIndex = this.laps.findIndex(lap => lap.id === update.data.id);

          /* Lap is found */
          if (lapIndex !== -1) {
            if (update.data.duration !== null) {
              /* The lap is updated */
              if (this.max !== null && update.data.start_time < this.laps[this.laps.length-1].start_time) {
                /* Refresh if dropping of the list */
                this.fill();
              } else {
                /* Set the correct key */
                update.data.key = this.laps[lapIndex].key
                /* Update the data */
                this.laps.splice(lapIndex, 1, update.data);
                /* Sort the results */
                this.laps.sort((a, b) => b.start_time - a.start_time);
              }
            } else {
              /* The lap must be removed (becomes the current lap) */
              if (this.max === null) {
                /* Remove from the laps if becoming current */
                this.laps.splice(lapIndex, 1);
              } else {
                /* Refresh as a lap is removed from the list */
                this.fill();
              }
            }
          } else {
            /* The lap is not yet present */
            if (update.data.duration !== null) {
              if (this.max === null || update.data.start_time > this.laps[this.laps.length-1].start_time) {
                /* The lap should be added to the list */

                if (this.max === this.laps.length) {
                  /* If the maximum is reached, remove the last element */
                  this.laps.splice(this.laps.length - 1, 1);
                }

                /* Set a new key */
                update.data.key = this.keys++;
                /* Push the new lap */
                this.laps.push(update.data);

                /* Sort */
                this.laps.sort((a, b) => b.start_time - a.start_time);
              }
            }
            /* Otherwise ignore a new 'current lap' */
          }
        }
        /* The update does not concern us */
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);
        update.data.start_time = new Date(update.data.start_time);

        /* Refresh if lap is found */
        let lapIndex = this.laps.findIndex((lap) => {return lap.id === update.data.id});
        if (lapIndex !== -1) {
          if (this.max !== null) {
            /* If there is a maximum, refresh (TODO: only get last?) */
            this.fill();
          } else {
            /* If all stored, simply remove it from the laps */
            this.laps.splice(lapIndex, 1);
          }
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

</style>