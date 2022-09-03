<template>
  <span>
    <v-dialog v-model="dialog" max-width="290">
      <v-card>
        <v-card-title class="text-h5">
          Ticket removal
        </v-card-title>
        <v-card-text>Are you sure you want to remove this ticket from the queue?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click=onRemoveModalClick>
            Yes
          </v-btn>
          <v-btn color="green darken-1" text @click="dialog=false">
            No
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <slot name="full" :queue="rangedQueue" :loading="loading">
      <v-container v-show="loading">
        <v-row justify="center">
          <v-progress-circular indeterminate :color="textColor" />
        </v-row>
      </v-container>
      <v-container :class="{'py-0': dense}">
        <v-list v-show="!loading" :dense="dense" style="overflow: hidden" :color="color">
          <draggable @end="onEnd" :animation="200" :force-fallback="true" :scroll-sensitivity="scrollSensitivity" :disabled="!draggable">
            <v-scroll-x-transition group>
              <v-list-item v-for="(ticket, ticketIdx) in rangedQueue" :key="ticket.key" class="ma-0 pa-0">
                <slot :ticket="ticket">
                  <v-row justify="center">
                    <v-col cols="11" :sm="sm" :md="md" :lg="lg">
                      <v-card v-on="addInfo ? {click: () => {expand(ticket)}} : {}" :color="cardColor">
                        <v-container :class="{'py-0': dense}">
                          <v-row align="center">
                            <v-col cols="12">
                              <div class="text-center text-body-2" :class="[{'py-0': dense}, textColorComp]">{{ ticketIdx }} - {{ ticket.runner | fullName }}</div>
                              <div class="text-center text-lg-end mt-1 mt-lg-n7" :class="[{'py-0': dense}]"
                                   v-if="actions.includes('remove')">
                                <v-btn :color="btnColor" :class="btnTextColorComp" class="text-caption text-sm-button" @click.stop="onRemoveClick(ticket)">
                                  <slot>Remove</slot>
                                </v-btn>
                              </div>
                            </v-col>
                          </v-row>
                          <v-expand-transition v-if="addInfo">
                            <div v-if="ticket.expand">
                              <v-divider />
                              <slot name="info" :ticket="ticket">
                                <v-container>
                                  <v-row justify="center">
                                    <v-col cols="12" sm="10" md="6" lg="4">
                                      <v-alert dense type="error" v-model="alerts.runnerQuickInfo.error.status">
                                            {{ alerts.runnerQuickInfo.error.msg }}
                                      </v-alert>
                                      <runner-quick-info :runner="ticket.runner" @error="onRunnerQuickInfoError"/>
                                    </v-col>
                                    <v-col cols="12" sm="10" md="6" lg="4">
                                      <v-alert dense type="error" v-model="alerts.lastLapList.error.status">
                                            {{ alerts.lastLapList.error.msg }}
                                      </v-alert>
                                      <last-lap-list :runner-id="ticket.runner.id" :max="3" @error="onLastLapListError">
                                        <template v-slot:full="{ laps, loading }">
                                          <v-data-table :headers="lastLapTableHeaders" :items="getLastLapItems(laps)"
                                                      disable-pagination hide-default-footer :loading="loading" disable-sort
                                                      :class="[color, textColorComp]"/>
                                        </template>
                                      </last-lap-list>
                                    </v-col>
                                    <v-col cols="12">
                                      <v-sheet class="v-sheet--offset mx-auto" color="primary lighten-1 white--text" elevation="12">
                                        <lap-chart :runner-id="ticket.runner.id" :classes="['pr-3']"/>
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
          </draggable>
        </v-list>
      </v-container>
    </slot>
  </span>
</template>

<script>
  import draggable from 'vuedraggable'
  import {oneTimeEvent} from '../../utils';
  import {QueueSync} from "../../utils/queueSync";
  import RunnerQuickInfo from "../info/RunnerQuickInfo";
  import LastLapList from "./LastLapList";
  import LapChart from "../charts/LapChart";
  export default {
    name: "RunnerQueue",
    events: ['error'],
    props: {
      rangeFrom: {
        type: Number,
        default: 0,
        validator: function(value) {
          return value >= 0;
        }
      },
      rangeTo: {
        type: Number,
        default: Number.NaN,
        validator: function(value) {
          return isNaN(value) || value >= 0;
        }
      },
      draggable: {
        type: Boolean,
        default: false,
      },
      addInfo: {
        type: Boolean,
        default: false
      },
      actions: {
        type: Array,
        default: function() {return [];},
        validator: function(value) {
          return value.map((e) => ['remove'].includes(e)).reduce((res, e) => res && e, true);
        }
      },
      scrollSensitivityPercentage: {
        type: Number,
        default: 0.2,
        validator: function(value) {
          return 0 <= value && value <= 1;
        }
      },
      dense: {
        type: Boolean,
        default: false,
      },
      sm: {
        type: Number,
        default: 10
      },
      md: {
        type: Number,
        default: 9
      },
      lg: {
        type: Number,
        default: 8
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
      btnColor: {
        default: 'warning'
      },
      btnTextColor: {
        default: 'primary'
      }
    },
    data: () => ({
      queueSync: null,
      lastKey: 0,
      dragged: false,
      windowHeight: window.innerHeight,
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
      dialog: false,
      dialogTicket: null,
    }),
    computed: {
      scrollSensitivity() {
        return this.windowHeight * this.scrollSensitivityPercentage;
      },
      rangedQueue() {
        return this.queueSync?.queue.slice(this.rangeFrom, isNaN(this.rangeTo) ?  this.queueSync.queue.length : this.rangeTo);
      },
      textColorComp: function() {
        return `${this.textColor}--text`;
      },
      btnTextColorComp: function() {
        return `${this.btnTextColor}--text`;
      },
      lastLapTableHeaders: function() {
        return [{
              text: 'Last laps',
              value: 'name',
              align: 'center',
              class: this.textColorComp,
            }]
      },
      loading() {
        return this.queueSync?.loading;
      }
    },
    components: {
      LapChart,
      LastLapList,
      RunnerQuickInfo,
      draggable,
    },
    methods: {
      expand(ticket) {
        ticket.expand = !ticket.expand;
      },
      onQueueTicketCreate(ticket) {
        ticket.key = this.lastKey++;
        ticket.expand = false;
      },
      getLastLapItems(laps) {
        return laps.map((lap) => ({name: this.$options.filters.durationFilter(lap.duration)}));
      },
      onWindowResize() {
        this.windowHeight = window.innerHeight;
      },
      onEnd(evt) {
        if (evt.oldIndex === evt.newIndex) return;

        /* Prevent click after drag */
        oneTimeEvent(evt.item, 'click', (e) => {
          e.stopImmediatePropagation();
        }, 100);

        /* Report the update to the server */
        this.queueSync.sendUpdate('move', {pos_move: evt.oldIndex, pos_target: evt.newIndex}).then((success) => {
          if (!success) {
            this.$emit('error', 'Queue update failed, please try again or refresh');
          }
        })
      },
      onRemoveClick(ticket) {
        this.dialogTicket = ticket;
        this.dialog = true;
      },
      onRemoveModalClick() {
        this.queueSync.sendUpdate('delete', this.dialogTicket).then((success) => {
          if (!success) {
            this.$emit('error', 'Queue remove failed, please try again or refresh');
          }
        });
        this.dialog = false;
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
      /* Add a window height change event listener */
      window.addEventListener('resize', this.onWindowResize);

      /* Fill the queue */
      try {
        this.queueSync = new QueueSync(this.axios, this.$store, this.onQueueTicketCreate.bind(this));
        await this.queueSync.init();
      } catch (e) {
        this.$emit('error', 'Unable to initialize queue');
      }
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.onWindowResize);
      this.queueSync.destroy();
    }
  }
</script>

<style scoped>
.flip-list-move {
  transition: transform 1s;
}

.sortable-drag {
  visibility: hidden;
}
</style>