<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" sm="10" md="6" lg="3">
                <v-simple-table class="tertiary">
                <thead>
                    <tr>
                    <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Queue</th>
                    </tr>
                </thead>
                <tbody>
                    <queue :range-from="0" :range-to="25" dense :lg="11" :md="11" :sm="11"/>
                </tbody>
                </v-simple-table>
            </v-col>
            <v-col cols="12" sm="10" md="6" lg="3">
                <v-simple-table class="tertiary">
                    <thead>
                        <tr>
                        <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Top runners</th>
                        </tr>
                    </thead>
                    <tbody>
                        <top-runners :max="7" dense/>
                    </tbody>
                </v-simple-table>
                <v-simple-table class="tertiary">
                    <thead>
                        <tr>
                        <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Current runner</th>
                        </tr>
                    </thead>
                    <tbody>
                        <active-runner>
                        <template v-slot:full="{ loading, lap }">
                            <v-container v-show="loading">
                            <v-row justify="center">
                                <v-progress-circular indeterminate color="primary" />
                            </v-row>
                            </v-container>
                            <v-list v-show="!loading" color="tertiary">
                            <v-list-item>
                                <v-container>
                                <v-card class="d-flex" justify="center" color="tertiary">
                                    <v-row justify="center">
                                    <v-col>
                                        <v-card-text class="text-center py-0 tertiary-text--text">
                                        <template v-if="lap">{{ lap.runner | fullName }} - <timer :start="Date.parse(lap.start_time)" /></template>
                                        <template v-else>Nobody</template>
                                        </v-card-text>
                                    </v-col>
                                    </v-row>
                                </v-card>
                                </v-container>
                            </v-list-item>
                            </v-list>
                        </template>
                        </active-runner>
                    </tbody>
                </v-simple-table>
            </v-col>
            <v-col cols="12" sm="10" md="6" lg="3">
                <v-simple-table class="tertiary">
                    <thead>
                        <tr>
                        <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Top groups</th>
                        </tr>
                    </thead>
                    <tbody>
                        <top-groups :max="5" dense/>
                    </tbody>
                </v-simple-table>
                <v-simple-table class="tertiary">
                    <thead>
                        <tr>
                            <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Last laps</th>
                        </tr>
                    </thead>
                    <tbody>
                        <last-lap-list :max="7" dense />
                    </tbody>
                </v-simple-table>
            </v-col>
            <v-col cols="12" sm="10" md="6" lg="3">
                <v-simple-table class="tertiary">
                <thead>
                    <tr>
                    <th class="text-left text-subtitle-2 tertiary-text--text font-weight-bold">Most active runners</th>
                    </tr>
                </thead>
                <tbody>
                    <most-active-runners :max="7" dense/>
                </tbody>
                </v-simple-table>  
            </v-col>
            <v-col cols="12" sm="10" md="6" lg="3">
            </v-col>
        </v-row>
    </v-container>


</template>

<script>
  import Queue from "../components/lists/RunnerQueue";
  import TopRunners from "../components/lists/TopRunners";
  import TopGroups from "../components/lists/TopGroups";
  import MostActiveRunners from "../components/lists/MostActiveRunners";
  import ActiveRunner from "../components/info/ActiveRunner";
  import Timer from "../components/info/LiveTimer";
  import LastLapList from "../components/lists/LastLapList";
  // import LapChart from "../components/charts/LapChart";
  export default {
    name: "StatisticsView",
    components: {LastLapList, Timer, ActiveRunner, MostActiveRunners, TopGroups, TopRunners, Queue},
    data: () => ({
      start: 0,
    }),
    methods: {
      onLapChange(lap) {
        this.start = lap !== null ? Date.parse(lap.start_time) : 0;
      }
    }
  }
</script>

<style scoped>

</style>