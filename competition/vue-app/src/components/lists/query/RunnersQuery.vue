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
            <v-list-item v-for="runner in filteredRunners" :key="runner.key" class="ma-0 pa-0">
              <slot :runner="runner">
                <v-row justify="center">
                  <v-col cols="11">
                    <v-card :color="cardColor" @click="expand(runner)">
                      <v-container class='my-1'>
                        <v-row justify="center">
                          <v-col cols="12">
                            <div class="text-center" :class="[{'py-0': dense}, textColorComp]">
                              <span class="text-subtitle-1">{{ runner | fullName }}</span>
                              <br/>
                              <span class="text-body-1">{{ runner.identification }}</span>
                            </div>
                          </v-col>
                        </v-row>
                        <v-expand-transition>
                            <div v-if="runner.expand">
                              <v-divider />
                              <slot name="info" :runner="runner">
                                <v-container>
                                  <v-row justify="center">
                                    <v-col cols="12" sm="10" md="6" lg="4">
                                      <v-alert dense type="error" v-model="alerts.runnerQuickInfo.error.status">
                                            {{ alerts.runnerQuickInfo.error.msg }}
                                      </v-alert>
                                      <runner-quick-info :runner="runner" @error="onRunnerQuickInfoError"/>
                                    </v-col>
                                    <v-col cols="12" sm="10" md="6" lg="4">
                                      <v-alert dense type="error" v-model="alerts.lastLapList.error.status">
                                            {{ alerts.lastLapList.error.msg }}
                                      </v-alert>
                                      <last-lap-list :runner-id="runner.id" :max="3" @error="onLastLapListError">
                                        <template v-slot:full="{ laps, loading }">
                                          <v-data-table :headers="lastLapTableHeaders" :items="getLastLapItems(laps)"
                                                      disable-pagination hide-default-footer :loading="loading" disable-sort
                                                      :class="[color, textColorComp]"/>
                                        </template>
                                      </last-lap-list>
                                    </v-col>
                                    <v-col cols="12">
                                      <v-sheet class="v-sheet--offset mx-auto" color="primary lighten-1 white--text" elevation="12">
                                        <lap-chart :runner-id="runner.id" :classes="['pr-3']"/>
                                      </v-sheet>
                                    </v-col>
                                  </v-row>
                                </v-container>
                              </slot>
                            </div>
                          </v-expand-transition>
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
import RunnerQuickInfo from "../../info/RunnerQuickInfo";
import LastLapList from "../LastLapList";
import LapChart from "../../charts/LapChart";
export default {
  name: "RunnersQuery",
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
    },
    params: {
      type: Object,
      required: true,
    },
  },
  components: {
      LapChart,
      LastLapList,
      RunnerQuickInfo,
    },
  data: () => ({
    runners: [],
    loading: true,
    lastKey: 0,
    alerts: {
        runnerQuickInfo: {
          error: {
            status: false,
            msg: ''
          }
        },
        lastLapList: {
          error: {
            status: false,
            msg: '',
          }
        }
      },
  }),
  computed: {
    textColorComp: function() {
      return `${this.textColor}--text`;
    },
    filteredRunners: function() {
      return this.runners.filter((runner) => {
        return this.params.runner_name_filter === null 
                || runner.first_name.toLowerCase().indexOf(this.params.runner_name_filter.toLowerCase()) !== -1
                || runner.last_name.toLowerCase().indexOf(this.params.runner_name_filter.toLowerCase()) !== -1
      })
    },
    lastLapTableHeaders: function() {
      return [{
            text: 'Last laps',
            value: 'name',
            align: 'center',
            class: this.textColorComp,
          }]
    },
  },
  methods: {
    async fill() {
      try {
        let resp = await this.axios.get(`${this.$store.state.urls.runner}/`);
        this.runners = resp.data.map((runner) => {
          let r = this.runners.find((r) => {return r.id === runner.id});
          if (r) {
            runner.key = r.key;
          } else {
            runner.key = this.lastKey++;
          }
          runner.expand = false;
          return runner;
        });
        console.log(this.runners);
      } catch (e) {
        this.$emit('error');
      }
    },
    async refresh() {
      this.loading = true;
      await this.fill();
      this.loading = false;
    },
    expand(runner) {
      runner.expand = !runner.expand;
    },
    getLastLapItems(laps) {
      return laps.map((lap) => ({name: this.$options.filters.durationFilter(lap.duration)}));
    },
    onRunnerQuickInfoError(msg) {
      let alert = this.alerts.runnerQuickInfo.error;
      alert.status = true;
      alert.msg = msg;
    },
    onLastLapListError(msg) {
      let alert = this.alerts.lastLapList.error;
      alert.status = true;
      alert.msg = msg;
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