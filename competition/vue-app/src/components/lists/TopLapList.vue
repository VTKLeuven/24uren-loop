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
                              {{ lap.duration | durationFilter }} - {{ lap.runner | fullName }}
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
    name: "TopLapList",
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
        default: null,
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
      max: function() {
        this.fill();
      },
      runnerId: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.lap}/`, {
            params: {
              'duration__isnull': false,
              'ordering': 'duration',
              'limit': this.max,
              'runner': this.runnerId,
            }
          });
          this.laps = resp.data.map((e) => {e.key = this.keys++; return e});
        } catch (e) {
          this.$emit('error', 'Unable to get top laps');
        }
      },
      async last() {
        if (this.max) {
          /* Fetch the last item that belongs in the list */
          try {
            let last = await this.axios.get(`${this.$store.state.urls.lap}/`, {
              params: {
                'duration__isnull': false,
                'ordering': 'duration',
                'offset': this.max-1,
                'limit': this.max,
                'runner': this.runnerId,
              }
            });
            return last.data.length >= 1 ? last.data[0] : null
          } catch (e) {
            this.$emit('error', 'Unable to get last lap from top list');
          }
        }

        /* If no limit, we already have all laps so no need to fetch any more */
        return null;
      },
      async onLapUpdate(resp) {
        let update = JSON.parse(resp.data);

        /* Find index of updated lap */
        let i = this.laps.findIndex((lap) => {return lap.id === update.data.id});

        if (i !== -1) {
          /* The lap is found */

          /* Set the correct key for the change */
          update.data.key = this.laps[i].key;

          /* Top lap is updated */
          if (this.laps[i].duration === update.data.duration) {
            /* Duration is not updated, so only simple data update */
            this.laps.splice(i, 1, update.data);
          } else {
            /* The lap drops off the list */
            if (update.data.duration > this.laps[this.laps.length-1].duration) {
              /* Remove the updated lap from the list */
              this.laps.splice(i, 1);
              /* Get the last lap */
              let lastLap = await this.last();
              /* If there is another lap, push it on the laps */
              if (lastLap) {
                lastLap.key = this.keys++;
                this.laps.push(lastLap);
              }
            } else {
              /* Adjust the data */
              this.laps.splice(i, 1, update.data);
              /* Re-sort the data */
              this.laps.sort((a, b) => {a.duration - b.duration});
            }
          }
        } else {
          /* Lap not found */
          /* The updated lap has a better lap time and belongs in the list */
          if (this.max === null || (update.data.duration !== null && update.data.duration < this.laps[this.laps.length-1].duration)) {
            /* Remove last lap from the list */
            if (this.laps.length === this.max) this.laps.splice(this.laps.length-1, 1);
            /* Insert the new lap at the correct spot */
            update.data.key = this.keys++;
            this.laps.push(update.data);

            /* Sort the laps */
            this.laps.sort((a, b) => {a.duration - b.duration});
          }
          /* Otherwise ignore the update */
        }
      },
      async onLapDelete(resp) {
        let update = JSON.parse(resp.data);
        /* Find the index of the deleted lap */
        let i = this.laps.findIndex((lap) => {return lap.id === update.data.id});
        /* If not in the list, ignore */
        if (i === -1) return;

        /* Remove it from the list */
        this.laps.splice(i, 1);
        /* Retrieve the last lap from the top-list */
        let lastLap = await this.last();
        /* If there is another lap, push it on the laps */
        if (lastLap) {
          lastLap.key = this.keys++;
          this.laps.push(lastLap);
        }
      }
    },
    async mounted() {
      await this.fill();
      this.loading = false;
      await this.$store.dispatch('subscribe_sse', {event: 'lap_update', handler: this.onLapUpdate});
      await this.$store.dispatch('subscribe_sse', {event: 'lap_delete', handler: this.onLapDelete});
    },
    beforeDestroy() {
      this.$store.dispatch('unsubscribe_sse', {event: 'lap_update', handler: this.onLapUpdate});
      this.$store.dispatch('unsubscribe_sse', {event: 'lap_delete', handler: this.onLapDelete});
    }
  }
</script>

<style scoped>

</style>