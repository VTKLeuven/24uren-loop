<template>
  <v-form>
    <v-text-field 
        :value=params.runner_name_filter 
        @input="change($event, 'runner_name_filter')"
        label="Name filter"></v-text-field>
  </v-form>
</template>

<script>
export default {
  name: "ListRunnersInShiftForm",
  events: ['error'],
  props: {
    params: {
      type: Object,
      default: () => ({
        runner_name_filter: null,
      })
    }
  },
  data: () => ({
  }),
  methods: {
    change(value, param) {
      let params = this.getParams(false);
      params[param] = value;
      this.$emit('input', params);
    },
    getParams(nullify) {
      return {
        runner_name_filter: nullify ? null : this.params.runner_name_filter,
      }
    }
  },
  beforeDestroy() {
    this.$emit('input', this.getParams(true))
  }
}
</script>

<style scoped>

</style>