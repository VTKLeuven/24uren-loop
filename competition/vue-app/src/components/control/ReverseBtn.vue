<template>
    <v-btn @click="undo" v-bind="$attrs">Undo</v-btn>
</template>

<script>
  export default {
    name: "ReverseBtn",
    events: ['success', 'fail'],
    methods: {
      async undo() {
        try {
          await this.axios.post(`${this.$store.state.urls.reverse}/`, {});
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