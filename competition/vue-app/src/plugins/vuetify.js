import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue';
import Vuetify from 'vuetify/lib';

// import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: '#1A1F4A', // blue
        secondary: '#FFD400', // yellow
        tertiary: '#ECEAEE', // white
        'primary-text': '#FFD400',
        'secondary-text': '#1A1F4A',
        'tertiary-text': '#1A1F4A',
      },
    },
  },
});