<template>
  <v-container>

    <v-alert dense type="success" v-model="alerts.startSuccess">
      Successfully started next lap.
    </v-alert>
    <v-alert dense type="success" v-model="alerts.undoSuccess">
      Successfully undid lap.
    </v-alert>
    <v-alert dense type="error" v-model="alerts.error">
      Something went wrong!
    </v-alert>

    <v-row>
      <v-container>
        <v-row justify="center">
          <v-col cols="12">
            <v-card :elevation="12" color="tertiary">
              <v-card-title class="text-center justify-center text-h2 text-md-h1 tertiary-text--text body-font">
                <active-runner @change="onLapChange"/>
              </v-card-title>
              <v-card-subtitle class="text-center text-h6 text-md-h5 tertiary-text--text text--lighten-2 body-font">
                Current runner
              </v-card-subtitle>
              <v-card-text class="text-center text-h4 text-md-h3 tertiary-text--text body-font">
                <timer :start="start"/>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <advance-btn @success="onAdvanceSuccess" @fail="onAdvanceFail" height="3em"
                     class="text-h5 text-sm-h4 primary-text--text body-font"
                     block color="primary"/>
      </v-col>
      <v-col cols="12" md="6">
          <reverse-btn @success="onReverseSuccess" @fail="onReverseFail" height="3em"
                       class="text-h5 text-sm-h4 tertiary-text--text body-font"
                       block color="warning"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AdvanceBtn from "../components/control/AdvanceBtn";
import ReverseBtn from "../components/control/ReverseBtn";
import ActiveRunner from "../components/info/ActiveRunner";
import Timer from "../components/info/LiveTimer";
export default {
  name: "ControlView",
  components: {Timer, ActiveRunner, ReverseBtn, AdvanceBtn},
  data: () => ({
      alerts: {
        startSuccess: false,
        undoSuccess: false,
        error: false,
      },
      start: 0,
    }),
    methods: {
      disableAlerts: function () {
        this.alerts.startSuccess = false;
        this.alerts.undoSuccess = false;
        this.alerts.error = false;
      },
      onAdvanceSuccess() {
        this.alerts.startSuccess = true;
        setTimeout(() => {
          this.alerts.startSuccess = false;
        }, 1000);
      },
      onAdvanceFail() {
        this.alerts.error = true;
      },
      onReverseSuccess() {
        this.alerts.undoSuccess = true;
        setTimeout(() => {
          this.alerts.undoSuccess = false;
        }, 1000);
      },
      onReverseFail() {
        this.alerts.error = true;
      },
      onActiveRunnerError() {
        this.alerts.error = true;
      },
      onLapChange(lap) {
        this.start = lap !== null ? Date.parse(lap.start_time) : 0;
      }
    }
}
</script>

<style scoped lang="sass">
.body-font
  font-family: $body-font-family !important

</style>