<template>
    <last-lap-list :runner-id="runner.id" @error="onError">
      <template v-slot:full="{ laps, loading:lap_loading }">
        <lap-count :runner-id="runner.id" @error="onError">
          <template v-slot:full="{ count, loading:count_loading }">
            <v-data-table :headers="headers" :items="getItems(laps, count)" hide-default-footer
                        :loading="lap_loading || count_loading" disable-sort
                        :class="[color, textColorComp]"/>
          </template>
        </lap-count>
      </template>
    </last-lap-list>
</template>

<script>
  import LastLapList from "../lists/LastLapList";
  import LapCount from "./LapCount";
  export default {
    name: "RunnerQuickInfo",
    components: {LapCount, LastLapList},
    events: ['error'],
    props: {
      runner: {
        type: Object,
        required: true,
      },
      color: {
        default: 'tertiary'
      },
      textColor: {
        default: 'tertiary-text'
      },
    },
    data: () => ({}),
    computed: {
      textColorComp: function() {
        return `${this.textColor}--text`;
      },
      headers:function() {
        return [{
            text: 'Quick information',
            value: 'name',
            align: 'begin',
            class: this.textColorComp,
          }, {
            text: '',
            value: 'value'
          }]
      },
    },
    methods: {
      getItems(laps, count) {
        let items = [];

        console.log(this.runner.id, laps, count);

        /* Add test time */
        if (this.runner.test_time) {
          items.push({name: 'Test time', value: this.$options.filters.durationFilter(this.runner.test_time)});
        }

        /* Add last lap */
        if (laps.length !== 0) {
          items.push({name: 'Last lap', value: this.$options.filters.durationFilter(laps[0].duration)});
        }
        
        /* Add last lap time */
        if (laps.length !== 0) {
          items.push({name: 'Last Lap Start Time', value: laps[0].start_time.toLocaleTimeString()})
        }

        /* Add lap count */
        items.push({name: 'Lap count', value: count});

        return items;
      },
      onError(msg) {
        this.$emit('error', msg);
      }
    },
  }
</script>

<style scoped>

</style>