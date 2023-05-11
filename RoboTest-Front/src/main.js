import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import MyServerHttp from '@/plugins/http.js';


import '@/assets/css/reset.css'
import './assets/fonts/iconfont.css'
import VueCropper from 'vue-cropper'

Vue.use(VueCropper)
Vue.use(ElementUI);
Vue.use(MyServerHttp);

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
