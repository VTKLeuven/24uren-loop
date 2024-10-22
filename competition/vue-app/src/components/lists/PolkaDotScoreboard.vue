<template>
  <span>
    <slot name="full" :polkaDotScoreboard="polkaDotScoreboard" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" style="overflow: hidden" :dense="dense" :color="color">
          <v-scroll-x-transition group>
            <v-list-item v-for="(runner, index) in polkaDotScoreboard" :key="index" class="ma-0 pa-0">
              <slot :runner="runner">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor">
                      <v-container :class="{'py-0': dense}">
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="d-flex align-center text-body-2" :class="[{'py-0': dense}, textColorComp]">
                              <img v-if="index === 0" src="/jerseys/bolletjestrui.png" alt="Polka Dot Jersey"
                                   class="fit-image"/>
                              {{ runner }}
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
    name: "PolkaDotScoreboard",
    events: ['error'],
    props: {
      max: {
        type: Number,
        default: null,
        validator: function(value) {
          return value === null || value > 0;
        }
      },
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
      polkaDotScoreboard: [],
      keys: 0,
      loading: true,
    }),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      },
    },
    watch: {
      max: function() {
        this.fill();
      }
    },
    methods: {
      async fill() {
        try {
          let resp = await this.axios.get(`${this.$store.state.urls.polkadot_scoreboard}/`, {
            params: {
              'limit': this.max,
            }
          });
          this.polkaDotScoreboard = resp.data
          console.log(this.polkaDotScoreboard)
        } catch (e) {
          this.$emit('error', 'Unable to get polka dot scoreboard');
        }
      },
      onLapUpdate() {
        this.fill();
      },
      onLapDelete(resp) {
        let update = JSON.parse(resp.data);
        let i = this.polkaDotScoreboard.findIndex((runner) => {return update.data.runner.id === runner.id;});
        if (i === -1) return;
        if (i === this.polkaDotScoreboard.length - 1) {
          this.fill();
        } else {
          this.polkaDotScoreboard[i].runner.lapcount--;
          this.polkaDotScoreboard.sort((a, b) => a.runner.lapcount - b.runner.lapcount);
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
    },
  }
</script>

<style scoped>
.fit-image {
  height: 50px;
  width: auto;
  margin-bottom: 10px;
  margin-right: 10px;
}
</style>