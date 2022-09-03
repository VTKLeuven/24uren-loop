<template>
  <span>
    <slot name="full" :loading="loading" :lap="currentLap">
      <v-progress-circular v-show="loading" indeterminate color="primary" />
      <span v-show="!loading">
        <template v-if="currentLap">{{ currentLap.runner | fullName }}</template>
        <template v-else>Nobody</template>
      </span>
    </slot>
  </span>
</template>

<script>
  export default {
    name: "ActiveRunner",
    events: ['error', 'change'],
    data: () => ({
      currentLap: null,
      loading: true,

      advanceBuffer: {
        current: {
          set: false,
        },
        next: {
          value: null,
          set: false,
        },
        timer: null,
        timeout: 1000,
      },
      reverseBuffer: {
        current: {
          set: false,
        },
        previous: {
          value: null,
          set: false,
        },
        timer: null,
        timeout: 1000,
      }
    }),
    methods: {
      setCurrentLap(lap) {
        this.currentLap = lap;
        this.$emit('change', lap);
      },
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.lap}/`, {
            params: {
              'duration__isnull': true,
            }
          });
          this.setCurrentLap(resp.data.length >= 1 ? resp.data[0] : null);
        } catch(e) {
            this.$emit('error', 'Cannot get current lap');
        }
      },

      onLapUpdate(resp) {
        let update = JSON.parse(resp.data);

        if (this.currentLap !== null) {
          /* There is a current lap */
          if (update.data.id === this.currentLap.id) {
            /* If the current lap is changed */
            if (update.data.duration !== null) {
              /* The lap is finished, no active runner */
              this.setCurrentLap(null);
            } else {
              /* Simple data adjustment */
              this.setCurrentLap(update.data);
            }
          }
        } else if (update.data.duration === null) {
          /* If the duration is not null and there is no current lap, this must be the current lap */
          this.setCurrentLap(update.data);
        }
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);

        /* The current lap has been deleted */
        if (this.currentLap !== null && update.data.id === this.currentLap.id) {
          /* Re-synchronise with the server */
          this.fill();
        } /* Ignore the deletion otherwise */
      }
    },
    watch: {
      currentLap: function(val) {
        this.$emit('change', val);
      }
    },
    async mounted() {
      await this.fill();
      this.loading = false;

      await this.$store.dispatch('subscribe_sse', {event: 'lap_update', handler:this.onLapUpdate});
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