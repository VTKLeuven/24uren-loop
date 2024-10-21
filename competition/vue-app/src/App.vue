<template>
  <v-app>
    <v-navigation-drawer color="primary lighten-1" v-model="drawer" app>
      <v-list>
        <router-link :to="{name: 'index'}" v-if="router_permissions.index">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">bar_chart</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Statistics</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <router-link :to="{name: 'queueUp'}" v-if="router_permissions.queueUp">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">person_add</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Queue up</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <router-link :to="{name: 'liverunners'}" v-if="router_permissions.liverunners">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">live_tv</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Live runners</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <router-link :to="{name: 'queue'}" v-if="router_permissions.queue">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">people</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Queue</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <router-link :to="{name: 'control'}" v-if="router_permissions.control">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">skip_next</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Controls</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <router-link :to="{name: 'query'}" v-if="router_permissions.query">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">search</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Query</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>

        <router-link :to="{name: 'group'}" v-if="router_permissions.queueUp">
          <v-list-item link>
            <v-list-item-icon>
              <v-icon class="primary-text--text">people</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary-text--text text-body-1">Groups</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>
      </v-list>
    </v-navigation-drawer>

    <router-link :to="{name: 'group'}" v-if="router_permissions.queueUp">
      <v-list-item link>
        <v-list-item-icon>
          <v-icon class="primary-text--text">people</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="primary-text--text text-body-1">Groups</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </router-link>

    <v-app-bar app color="primary">
      <v-app-bar-nav-icon class="primary-text--text" @click.stop="drawer = !drawer" />
      <router-link to="/index">
        <v-toolbar-title class="primary-text--text text-h6 text-sm-h4">24h Run Dashboard</v-toolbar-title>
      </router-link>
      <v-spacer />
      <v-btn color="secondary" class="secondary-text--text text-sm-button text-caption"
             v-if="!$store.getters.isAuthenticated" @click="login()">Login</v-btn>
      <v-btn color="secondary" class="secondary-text--text text-sm-button text-caption" v-else @click="logout()">Logout</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-alert dense type="error" v-model="alerts.error.status">
          {{ alerts.error.msg }}
        </v-alert>
        <v-alert dense type="success" v-model="alerts.success.status">
          {{ alerts.success.msg }}
        </v-alert>
        <v-alert dense type="info" v-model="alerts.info.status">
          {{ alerts.info.msg }}
        </v-alert>
        <v-alert dense type="warning" v-model="alerts.warn.status">
          {{ alerts.warn.msg }}
        </v-alert>
        <router-view @global-alert="alert" />
      </v-container>
    </v-main>

    <v-footer color="primary" app>
      <v-container>
        <v-row>
          <v-col align="left" class="white--text text-caption">
            <credits />
          </v-col>
          <v-col align="center" class="white--text text-caption">
            {{ datetime.toString().split('GMT')[0] }}
          </v-col>
          <v-col align="right">
            <synchronisation-info class="text-caption" synchronized-color="white" error-color="red" />
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>

import SynchronisationInfo from "./components/info/SynchronisationInfo";
import Credits from "./components/info/CreditsData";
export default {
  name: 'App',
  components: {
    Credits,
    SynchronisationInfo
  },
  data: () => ({
    drawer: false,
    alerts: {
      error: {
        msg: '',
        status: false,
      },
      success: {
        msg: '',
        status: false,
      },
      info: {
        msg: '',
        status: false,
      },
      warn: {
        msg: '',
        status: false,
      }
    },
    authWatcher: null,
    router_permissions: {},
    datetime: new Date(),
  }),
  methods: {
    alert({type, msg, timeout=null}) {
      /* Check the type of the alert */
      switch (type) {
        case 'info': {
          this.alerts.info.msg = msg;
          this.alerts.info.status = !!msg;
          break;
        }
        case 'error': {
          this.alerts.error.msg = msg;
          this.alerts.error.status = !!msg;
          break;
        }
        case 'success': {
          this.alerts.success.msg = msg;
          this.alerts.success.status = !!msg;
          break;
        }
        case 'warn': {
          this.alerts.warn.msg = msg;
          this.alerts.warn.status = !!msg;
          break;
        }
        default: {
          console.error(`Unknown alert type: ${type}`);
        }
      }

      /* Set an interval to remove the alert after a while */
      if (timeout !== null && !isNaN(timeout))
        setTimeout(() => {
          this.alert({type: type, msg: null});
        }, timeout)
    },
    disableAlerts() {
      this.alerts.error = false;
      this.alerts.info = false;
      this.alerts.success = false;
      this.alerts.warn = false;
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push({name: 'login'});
      this.alert({type: 'success', msg:'Successfully logged out', timeout: 1000});
    },
    login() {
      if (this.$router.currentRoute.name !== 'login') {
        this.$router.push({name: 'login'});
      }
    },
    mapRouterPermissions() {
      this.$router.options.routes.forEach((route) => {
        this.$set(this.router_permissions, route.name, route.meta.hasPermission());
      });
    },
    updateDatetime() {
      this.datetime = new Date();
      setTimeout(() => {
        this.updateDatetime();
      }, 1000);
    }
  },
  async mounted() {
    /* Update the datetime */
    this.updateDatetime();

    /* Connect to the eventstream */
    if (this.$store.state.sse === null)
      this.alert({type: 'error', msg: 'Cannot connect to the server, please refresh later'});

    /* Manage errors on the eventstream */
    this.$store.state.sse?.on('error', (e) => {
      /* Manage sudden server close */
      if (e!== undefined && e.target.readyState === 2) {
        this.alert({type: 'error', msg: 'Server connection failed, please refresh later'});
      }
      console.log('SSE error: ', e);
    });

    /* Manage route permissions */
    this.mapRouterPermissions();
    this.authWatcher = this.$store.watch(
      (state) => state.auth_info,
      this.mapRouterPermissions,
      {deep: true}
    );
  },
  beforeDestroy() {
    this.$store.dispatch('close_sse');
    this.authWatcher();
  },
  watch: {
    '$route' (to) {
      document.title = to.meta.title || process.env.VUE_APP_TITLE
    }
  },
};
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>
