import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import App from './App.vue'
import router from './router'

// Importar els fitxers CSS de Bootstrap i BootstrapVue (l'ordre és important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

// Fem que el Boostrap estigui disponible a tot el projecte
Vue.use(BootstrapVue)
// Opcionalment també podem instal·lar les icones
Vue.use(IconsPlugin)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
