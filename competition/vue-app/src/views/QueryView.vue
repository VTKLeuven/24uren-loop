<template>
  <v-container>
    <v-row justify="center" v-show="show !== null">
      <v-btn class="tertiary tertiary-text--text" @click="show = null"><v-icon>undo</v-icon>Queries overview</v-btn>
    </v-row>
    <v-row justify="center">
      <v-list color="tertiary">
        <v-list-item v-show="show === null">
          <v-col>
            <v-card class="rounded" :elevation="5" color="tertiary">
              <v-card-title class="justify-center text-h4 tertiary-text--text">Query</v-card-title>
              <v-divider />
              <v-card-actions>
                <v-container>
                  <v-row justify="center" v-for="(query, i) in queries.shift" :key="i">
                    <v-btn class="ma-5 text-button tertiary tertiary-text--text" @click="show=query.name">{{ query.title }}</v-btn>
                  </v-row>
                </v-container>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-list-item>
      </v-list>
    </v-row>
    <v-list color="tertiary">
      <v-list-item v-for="(query, i) in queries.shift" :key="i" v-show="show === query.name">
        <v-row justify="center" v-if="show === query.name">
          <v-col cols=12>
            <v-card class="rounded" :elevation="5" color="tertiary">
              <v-card-title class="justify-center text-h6 tertiary-text--text">
                Query - {{ query.title }}
              </v-card-title>
              <v-divider />
              <v-card-text class="tertiary-text--text">
                <template v-if="query.form !== undefined">
                  <component :is="query.form" @input="query.params = $event" :params="query.params"/>
                  <v-divider />
                </template>
                <component :is="query.list" :params="query.params" dense/>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import RunnersWithoutUpcomingShifts from "../components/lists/query/RunnersWithoutUpcomingShifts";
import ListRunnersInShift from "../components/lists/query/ListRunnersInShift";
import ListRunnersInShiftForm from "../components/forms/query/ListRunnersInShiftForm";
import RunnersQuery from '../components/lists/query/RunnersQuery.vue';
import RunnerQueryForm from '../components/forms/query/RunnerQueryForm.vue';
export default {
  name: "QueryView",
  components: {RunnersWithoutUpcomingShifts, ListRunnersInShift, RunnersQuery},
  data: () => ({
    show: null,
    queries: {
      shift: [
        {
          name: 'runners-without-upcoming-shifts',
          title: 'Runners without upcoming shifts',
          list: RunnersWithoutUpcomingShifts,
        },
        {
          name: 'runners-in-shift',
          title: 'List runners in shift',
          list: ListRunnersInShift,
          form: ListRunnersInShiftForm,
          params: {shiftId: null, filter_queue: false}
        },
        {
          name: 'runners-query',
          title: 'Runners',
          list: RunnersQuery,
          form: RunnerQueryForm,
          params: {runner_name_filter: null}
        },
      ]
    }
  }),
}
</script>

<style scoped>

</style>