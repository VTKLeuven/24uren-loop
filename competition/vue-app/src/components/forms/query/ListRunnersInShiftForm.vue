<template>
  <v-form>
    <v-select :value="params.shiftId" required @input="change($event,'shiftId')"
              :items="shiftChoices" item-value="id" item-text="name"
              :label="loading ? 'Loading...' : 'Shift'" :disabled="loading"/>
    <v-checkbox :value="params.filter_queue" label="Filter queue" @change="change($event,'filter_queue')"/>
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
        shiftId: null,
        filter_queue: false,
      })
    }
  },
  data: () => ({
    shiftChoices: [],
    loading: true,
  }),
  methods: {
    async fill() {
      try {
        let resp = await this.axios.get(`${this.$store.state.urls.shift}/`);
        this.shiftChoices = resp.data;
      } catch (e) {
        this.$emit('error');
      }
    },
    change(value, param) {
      let params = this.getParams(false);
      params[param] = value;
      this.$emit('input', params);
    },
    getParams(nullify) {
      return {
        shiftId: nullify ? null : this.params.shiftId,
        filter_queue: nullify ? false : this.params.filter_queue,
      }
    }
  },
  async mounted() {
    await this.fill();
    this.loading = false;
  },
  beforeDestroy() {
    this.$emit('input', this.getParams(true))
  }
}
</script>

<style scoped>

</style>