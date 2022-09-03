<template>
  <span>
    <slot name="full" :count="count" :loading="loading">
      {{ count }}
    </slot>
  </span>
</template>

<script>
  export default {
    name: "LapCount",
    events: ['error'],
    props: {
      runnerId: {
        type: Number,
        required: true,
      }
    },
    data: () => ({
      count: 0,
      loading: true,
    }),
    watch: {
      runnerId: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.lap_count}/`, {
            params: {
              id: this.runnerId
            }
          });
          this.count = parseInt(resp.data.lap_count, 10);
        } catch (e) {
          this.$emit('error', 'Could not get lap count');
        }
      },
      onLapUpdate(resp) {
        let update = JSON.parse(resp.data);
        /* Cannot distinguish between adding a new lap and updating an existing one */
        if (update.data.runner.id === this.runnerId) {
          this.fill();
        }
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);
        if (update.data.runner.id === this.runnerId && update.data.duration !== null) {
          --this.count;
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
    }
  }
</script>

<style scoped>

</style>