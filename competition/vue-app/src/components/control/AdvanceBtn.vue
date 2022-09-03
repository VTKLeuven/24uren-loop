<template>
    <v-btn @click="advance" v-bind="$attrs">
      <slot><span>Start next lap</span></slot>
    </v-btn>
</template>

<script>
  export default {
    name: "AdvanceBtn",
    events: ['success', 'fail'],
    methods: {
      async advance() {
        try {
          await this.axios.post(`${this.$store.state.urls.advance}/`, {now: new Date()});
          this.$emit('success');
        } catch (e) {
          this.$emit('fail');
        }
      },
    }
  }
</script>

<style scoped>

</style>