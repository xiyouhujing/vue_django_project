import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import BaiduMap from 'vue-baidu-map'
import axios from "axios"
import VueParticles from 'vue-particles'

//Vue.use(axios)
Vue.config.productionTip = false
Vue.prototype.axios=axios
Vue.use(ElementUI)
Vue.use(VueParticles)
Vue.use(BaiduMap, {
  // ak 是在百度地图开发者平台申请的密钥 详见 http://lbsyun.baidu.com/apiconsole/key */
  ak: 'fHrNQj6DHTjZtfTvfqbsuvTzKc5V9SBl'
})


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
