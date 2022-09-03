<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col class="text-center">
        <span class="text-h4 tertiary-text--text">Queue</span>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12">
        <v-alert dense type="error" v-model="alerts.error.status">
              {{ alerts.error.msg }}
        </v-alert>
        <Queue :draggable="draggable" :add-info="add_info" :actions="actions" @error="onError"/>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
  import Queue from "../components/lists/RunnerQueue";
  export default {
    name: "QueueView",
    components: {Queue},
    data: () => ({
      alerts: {
        error: {
          status: false,
          msg: ''
        }
      }
    }),
    computed: {
      add_info() {
        return this.$store.getters.is_admin;
      },
      draggable() {
        return this.$store.getters.is_admin;
      },
      actions() {
        if (this.$store.getters.is_admin) {
          return ['remove']
        } else {
          return []
        }
      }
    },
    methods: {
      onError(msg) {
        this.alerts.error.status = true;
        this.alerts.error.msg = msg;
      }
    }
  }
</script>

<style scoped>

</style>