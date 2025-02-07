import './assets/main.css'

import {createApp} from 'vue'
import Toast from "vue-toastification";
import App from './App.vue'
import "vue-toastification/dist/index.css";
import router from './router'
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';
import VueCookies from 'vue-cookies'

const app = createApp(App)

app.use(router)
app.use(Toast)
app.use(VCalendar, {})
app.use(VueCookies, {expires: '1h', secure:true, sameSite:'Strict'})


app.mount('#app')