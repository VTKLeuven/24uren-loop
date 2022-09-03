import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './filters'
import vuetify from './plugins/vuetify';
import AsyncComputed from 'vue-async-computed'
import Sse from 'vue-sse'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueApexCharts from 'vue-apexcharts'

/* Creating the authentication */
let axiosInstance = axios.create({withCredentials: false});
if (store.getters.isAuthenticated) {
  axiosInstance.defaults.auth = store.state.auth;
}

/* Some global vue plugins */
Vue.use(Sse);
Vue.use(AsyncComputed);
Vue.use(VueAxios, axiosInstance);
Vue.component('apexChart', VueApexCharts)

Vue.config.productionTip = false;

store.dispatch('open_sse').then(() => {
  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App),
    created: () => {store.dispatch('asyncLoad')}
  }).$mount('#app');
});


