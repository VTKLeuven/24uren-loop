<template>
  <span>
    <slot name="full" :runners="runners" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="(runner, i) in runners" :key="i" class="ma-0 pa-0">
              <slot :runner="runner">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="text-center" :class="[{'py-0': dense}, textColorComp]">
                              <span class="text-subtitle-1">{{ runner | fullName }}</span>
                              <br/>
                              <span class="text-body-1">{{ runner.identification }}</span>
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
  name: "RunnersWithoutUpcomingShifts",
  events: ['error'],
  props: {
    dense: {
      type: Boolean,
      default: false,
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
    runners: [],
    loading: true,
  }),
  computed: {
    textColorComp: function() {
      return `${this.textColor}--text`;
    }
  },
  methods: {
    async fill() {
      try {
        let resp = await this.axios.get(`${this.$store.state.urls.query.shift_runners_without_upcoming_shifts}/`);
        this.runners = resp.data;
      } catch (e) {
        this.$emit('error');
      }
    },
    async refresh() {
      this.loading = true;
      await this.fill();
      this.loading = false;
    }
  },
  async mounted() {
    await this.fill();
    this.loading = false;
  },
}
</script>

<style scoped>

</style>