<template>
  <span>
    <slot :diff="diff">
      <div v-show="!!diff">
        {{ diff | millisToMinSec }}
      </div>
    </slot>
  </span>
</template>

<script>
  export default {
    name: "LiveTimer",
    props: {
      start: {
        type: Number,
        required: true,
        validator: function(value) {
          return value >= 0;
        }
      },
      interval: {
        type: Number,
        default: 1000,
        validator: function(value) {
          return !!value && value > 0;
        }
      }
    },
    data: () => ({
      now: Date.now(),
    }),
    computed: {
      diff() {
        return this.start ? this.now - this.start : null;
      }
    },
    mounted() {
      setInterval(() => {
        this.now = Date.now();
      }, this.interval);
    }
  }
</script>

<style scoped>

</style>