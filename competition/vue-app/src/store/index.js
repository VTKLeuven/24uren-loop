import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const SERVER_URL = `${process.env.VUE_APP_HTTPS === '1' ? 'https' : 'http'}://${process.env.VUE_APP_SERVER_URL ? process.env.VUE_APP_SERVER_URL : window.location.hostname}${process.env.VUE_APP_SERVER_PORT ? ':' + process.env.VUE_APP_SERVER_PORT : ''}`;
const API_URL = `${SERVER_URL}/api`;
const API_AUTH_URL = `${SERVER_URL}/api-auth`;
const GROUP_NAME = 'competition';

export default new Vuex.Store({
  state: {
    urls: {
      server: SERVER_URL,
      events: `${SERVER_URL}/events`,

      login: `${API_AUTH_URL}/info`,
      auth_info: `${API_AUTH_URL}/info`,

      queue: `${API_URL}/queue`,
      queue_move: `${API_URL}/queue-ticket/move`,
      advance: `${API_URL}/lap/advance`,
      reverse: `${API_URL}/lap/reverse`,

      runner: `${API_URL}/runner`,
      lap: `${API_URL}/lap`,
      queue_ticket: `${API_URL}/queue-ticket`,
      university: `${API_URL}/university`,
      group: `${API_URL}/group`,
      shift: `${API_URL}/shift`,
      counter: `${API_URL}/counter`,
      rain_status: `${API_URL}/rain_status`,

      top_runners: `${API_URL}/runner/top_runners`,
      most_active: `${API_URL}/runner/most_active`,
      lap_count: `${API_URL}/lap/lap_count`,
      top_groups: `${API_URL}/group/top_groups`,

      query: {
        shift_runners_without_upcoming_shifts: `${API_URL}/shift/no_shift_after`,
        shift_list_runners: `${API_URL}/shift/list_runners`
      },
    },
    sse: null,
    auth: {
      username: localStorage.getItem('username') || '',
      password: localStorage.getItem('password') || '',
    },
    auth_info: {
      groups: [],
      is_staff: false,
    },
  },
  getters: {
    username: (state) => {return state.auth.username},
    isAuthenticated: (state) => {return !!state.auth.username && !!state.auth.password},
    hasAuthInfo: (state) => {return state.auth_info.set},
    is_group: (state) => {return state.auth_info.groups.includes(GROUP_NAME) || state.auth_info.is_staff},
    is_admin: (state) => {return state.auth_info.is_staff},
  },
  mutations: {
    /* Internal mutation for updating the sse server, should NOT be used */
    updateSSE(state, sse) {
      state.sse = sse;
    },
    /* Internal mutation for updating the auth details, should NOT be used */
    updateAuth(state, auth) {
      localStorage.setItem('username', auth.username);
      localStorage.setItem('password', auth.password);
      state.auth.username = auth.username;
      state.auth.password = auth.password;
      Vue.axios.defaults.auth = state.auth;
    },
    updateAuthInfo(state, auth_info) {
      state.auth_info.groups = auth_info.groups;
      state.auth_info.is_staff = auth_info.is_staff;
    }
  },
  actions: {
    /* Log the user in */
    async login(ctx, auth) {
      try {
        ctx.commit('updateAuth', auth);
        await Vue.axios.get(`${ctx.state.urls.login}/`);
        let resp = await Vue.axios.get(`${ctx.state.urls.auth_info}/`);
        ctx.commit('updateAuthInfo', {groups: resp.data.groups.map((group) => group.name), is_staff: resp.data.is_staff});
      } catch (e) {
        ctx.commit('updateAuth', {username: '', password: ''});
        ctx.commit('updateAuthInfo', {groups: [], is_staff: false});
        throw e;
      }
    },
    /* Log the user out */
    async logout(ctx) {
      ctx.commit('updateAuth', {username: '', password: ''});
      ctx.commit('updateAuthInfo', {groups: [], is_staff: false});
      Vue.axios.defaults.auth = undefined;
    },

    /* Load async info */
    async asyncLoad(ctx) {
      let resp = await Vue.axios.get(`${ctx.state.urls.auth_info}/`);
      ctx.commit('updateAuthInfo', {groups: resp.data.groups.map((group) => group.name), is_staff: resp.data.is_staff});
    },

    /* Open the sse connection */
    async open_sse(ctx) {
      const url = `${ctx.state.urls.events}/`;
      console.log(`Opening SSE on url: ${url}`);
      let sse = await Vue.$sse.create({
        format: 'plain',
        url: url
      }).connect().catch((e) => {
        console.log('SSE error');
        console.log(e);
      });
      ctx.commit('updateSSE', sse);
    },
    /* Close the sse connection */
    async close_sse(ctx) {
      ctx.state.sse.disconnect();
      ctx.commit('updateSSE', null);
      console.log('SSE closed');
    },
    subscribe_sse(ctx, {event, handler}) {
      ctx.state.sse?.source.addEventListener(event, handler);
    },
    unsubscribe_sse(ctx, {event, handler}) {
      ctx.state.sse?.source.removeEventListener(event, handler);
    }
  },
  modules: {},

})
