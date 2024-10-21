<template>
  <v-container>
    <v-row justify="center">
      <v-list min-width="100%" color="tertiary">
        <v-list-item>
          <v-container>
            <v-row justify="center">
              <v-col cols="11">
                <last-lap-list :max="1">
                  <template v-slot:full="{ laps, loading }">
                    <v-card :elevation="3" color="tertiary">
                      <v-row justify="center" v-show="loading">
                        <v-progress-circular indeterminate color="tertiary-text" />
                      </v-row>
                      <div v-show="!loading">
                        <v-fade-transition>
                          <v-card-title class="text-center justify-center text-h3 text-md-h2 tertiary-text--text base-font">
                            <template v-if="laps.length > 0">{{ laps[0].runner | fullName }}</template>
                            <template v-else>Nobody</template>
                          </v-card-title>
                        </v-fade-transition>
                        <v-card-subtitle class="text-center text-h6 tertiary-text--text text--lighten-2 base-font">Previous runner</v-card-subtitle>
                        <v-card-text class="text-center text-h5 text-md-h4 tertiary-text--text base-font" v-if="laps.length > 0">
                          {{ laps[0].duration | durationFilter }}
                        </v-card-text>
                      </div>
                    </v-card>
                  </template>
                </last-lap-list>
              </v-col>
            </v-row>
          </v-container>
        </v-list-item>
        <v-list-item>
          <v-container>
            <v-row justify="center">
              <v-col cols="12">
                <v-card :elevation="12" color="tertiary">
                  <v-card-title class="text-center justify-center text-h2 text-md-h1 tertiary-text--text base-font">
                    <active-runner @change="onLapChange"/>
                  </v-card-title>
                  <v-card-subtitle class="text-center text-h6 text-md-h5 tertiary-text--text text--lighten-2 base-font">Current runner</v-card-subtitle>
                  <v-card-text class="text-center text-h3 text-md-h3 tertiary-text--text base-font">
                    <timer :start="start"/>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-list-item>
        <v-list-item>
          <v-container>
            <v-row justify="center">
              <v-col cols="11">
                <runner-queue :range-from="0" :range-to="1">
                  <template v-slot:full="{ queue, loading }">
                    <v-card :elevation="3" color="tertiary">
                      <v-row justify="center" v-show="loading">
                        <v-progress-circular indeterminate color="tertiary-text" />
                      </v-row>
                      <span v-show="!loading">
                        <v-card-title class="text-center justify-center text-h3 text-md-h2 tertiary-text--text base-font">
                          <template v-if="queue !== undefined && queue.length > 0">{{ queue[0].runner | fullName }}</template>
                          <template v-else>Nobody</template>
                        </v-card-title>
                        <v-card-subtitle class="text-center text-h6 tertiary-text--text text--lighten-2 base-font">Next runner</v-card-subtitle>
                      </span>
                    </v-card>
                  </template>
                </runner-queue>
              </v-col>
            </v-row>
          </v-container>
        </v-list-item>
      </v-list>
    </v-row>
  </v-container>
</template>

<script>
  import Timer from "../components/info/LiveTimer";
  import LastLapList from "../components/lists/LastLapList";
  import ActiveRunner from "../components/info/ActiveRunner";
  import RunnerQueue from "../components/lists/RunnerQueue";
  export default {
    name: "LiveRunners",
    components: {RunnerQueue, ActiveRunner, LastLapList, Timer},
    data: () => ({
      start: 0,
    }),
    methods: {
      onLapChange(lap) {
        this.start = lap !== null ? Date.parse(lap.start_time) : 0;
      }
    },
  }
</script>

<style scoped lang="sass">
.v-card__text, .v-card__title
  word-break: normal

.base-font
  font-family: $body-font-family !important

.v-list-item, .v-container, .v-row, .v-col, .v-card
  margin: 0 !important
  padding: 0 !important

.v-list-item
  margin-bottom: 0 !important
  margin-top: 10px !important  // Adjust this value as needed

.v-list-item__content, .v-card__actions, .v-card__text, .v-card__title, .v-card__subtitle
  margin: 0 !important
  padding: 0 !important
</style>