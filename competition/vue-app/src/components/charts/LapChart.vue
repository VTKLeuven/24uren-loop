<template>
  <last-lap-list :runner-id="runnerId" :max="max">
    <template v-slot:full="{ laps }">
      <apexChart :class="classes" type="scatter" :height="height" :options="chartOptions(laps)" :series="series(laps)" />
    </template>
  </last-lap-list>
</template>

<script>
  import LastLapList from "../lists/LastLapList";
  export default {
    name: "LapChart",
    components: {LastLapList},
    props: {
      runnerId: {
        type: Number,
        default: -1,
      },
      height: {
        type: Number,
        default: 200,
      },
      max: {
        type: Number,
        default: 100
      },
      classes: {
        type: Array,
        default: function() {
          return [];
        },
      }
    },
    methods: {
      series: function(laps) {
        let data = laps.map(lap => [new Date(lap.start_time).getTime(), this.$options.filters.durationString(lap.duration)]);
        return [{
          name: 'Lap times',
          data: data,
        }];
      },
      chartOptions: function(laps) {
        let durations = laps.map(lap => this.$options.filters.durationString(lap.duration));
        let maxLapTime = laps.length === 0 ? 85*1000 : durations.reduce((acc, lap) => Math.max(acc, lap));
        let minLapTime = laps.length === 0 ? 60*1000 : durations.reduce((acc, lap) => Math.min(acc, lap));

        return {
          chart: {
            toolbar: {
              show: false,
              tools: {
                download: false,
                selection: false,
                zoom: true,
                zoomin: false,
                zoomout: false,
                pan: true,
                reset: true
              },
              autoselected: 'zoom'
            },
            foreColor: '#FFFFFF',
          },
          colors: ['#FFFFFF'],
          dataLabels: {
            enabled: false,
          },
          markers: {
            size: 4
          },
          grid: {
            xaxis: {
              showLines: true
            },
            yaxis: {
              showLines: true
            },
          },
          stroke: {
            show: false
          },
          xaxis: {
            tickPlacement: 'in',
            labels: {
              style: {
                colors: '#FFFFFF'
              },
              formatter: (millis) => {
                let date = new Date(millis);
                return `${date.getHours()}:${date.getMinutes()}`;
              }
            }
          },
          yaxis: {
            max: maxLapTime,
            min: minLapTime,
            tickAmount: 6,
            labels: {
              style: {
                color: '#FFFFFF'
              },
              formatter: (millis) => {
                return this.$options.filters.millisToMinSec(millis);
              }
            }
          },
          tooltip: {
            enabled: false
          }
        }
      },
    },
  }
</script>

<style scoped>
</style>