<template>
    <div :class="colorClasses">
        {{ timeSinceLastUpdate | synchronisationInfo }}
    </div>
</template>

<script>
  export default {
    name: "SynchronisationInfo",
    props: {
      synchronizedColor: {
        type: String,
        default: 'primary'
      },
      errorColor: {
        type: String,
        default: 'error'
      }
    },
    data: () => ({
      lastUpdate: null,
      now: Date.now()
    }),
    computed: {
      timeSinceLastUpdate() {
        return this.lastUpdate ? this.now - this.lastUpdate : null;
      },
      colorClasses() {
        let classes = {};
        classes[`${this.synchronizedColor}--text`] = this.timeSinceLastUpdate;
        classes[`${this.errorColor}--text`] = !this.timeSinceLastUpdate;
        return classes;
      }
    },
    filters: {
      synchronisationInfo: (timeSinceLastUpdate) => {
        if (!timeSinceLastUpdate) return 'Unable to synchronize with the server';
        if (timeSinceLastUpdate < 60000) {
          return 'Last synchronized seconds ago';
        } else {
          let minutes = Math.floor(timeSinceLastUpdate / 60000);
          return `Last synchronized ${minutes} minutes ago`;
        }
      }
    },
    methods: {
      updateNow() {
        this.lastUpdate = Date.now();
      }
    },
    async mounted() {
      /* Subscribe to open and keep-alive events */
      this.$store.dispatch('subscribe_sse', {event:'stream-open', handler: this.updateNow});
      this.$store.dispatch('subscribe_sse', {event:'keep-alive', handler: this.updateNow});

      /* Set the interval to update the synchronization information */
      setInterval(this.updateNow, 60*1000);
    },
    beforeDestroy() {
      /* Unsubscribe from events and close the connection */
      this.$store.dispatch('unsubscribe_sse', {event: 'stream-open', handler: this.updateNow});
      this.$store.dispatch('unsubscribe_sse', {event: 'keep-alive', handler: this.updateNow});
    }
  }
</script>

<style scoped>

</style>